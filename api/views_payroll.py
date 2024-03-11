from worksegment.models import WorkSegment
from employee.models import Employee, EmployeeRate, EmployeeBenefit, PrevailingRate
from worksegment.models import WorkType 
from project.models import Project
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum
from django.forms.models import model_to_dict
from datetime import datetime
from django.db.models.functions import ExtractYear

# Constants
HOURS_IN_YEAR = 2080

def get_total_fringe_rate(employee_id, year) -> float:
    '''Get total fringe rate per hour'''
    total_fringe_rate = 0
    try:
        employee = Employee.objects.get(id=employee_id)
        rate_obj = EmployeeRate.objects.annotate(year=ExtractYear('effective_date')).filter(employee=employee, year=year).order_by('-effective_date').first()
        rate = rate_obj.rate if rate_obj else None
        if rate:
            total_benefits = sum(benefit.amount if benefit.employer_paid else -benefit.amount for benefit in EmployeeBenefit.objects.filter(employee=employee, effective_date__year=year)) * 12
            fringe_rate = ((employee.eligible_vacation_hours() * rate) + (employee.sick_hours * rate) + (employee.holiday_hours * rate) + total_benefits) / HOURS_IN_YEAR
            total_fringe_rate = fringe_rate.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    except ObjectDoesNotExist:
        rate = None
    return total_fringe_rate

@csrf_exempt
def total_fringe(request, employee_id, year):
    '''Get total fringe rate per hour for testing only'''
    if request.method == 'GET':
        total_fringe_rate = get_total_fringe_rate(employee_id, year)
        data = {'total_fringe_rate': total_fringe_rate}
        return JsonResponse(data)

def calculate_total_segment_cost(segment) -> dict:
    '''Calculate total cost for a segment'''
    if segment['hours']['prevailing_rate_regular'] or segment['hours']['prevailing_rate_overtime'] or segment['hours']['prevailing_rate_doubletime']:
        # Calculate prevailing rate regular, overtime, and doubletime cost
        regular_cost = Decimal(segment['hours']['prevailing_rate_regular']) * segment['pr_rates']['rate']
        overtime_cost = Decimal(segment['hours']['prevailing_rate_overtime']) * segment['pr_rates']['rate'] * Decimal('1.5')
        doubletime_cost = Decimal(segment['hours']['prevailing_rate_doubletime']) * segment['pr_rates']['rate'] * Decimal('2')
        # fringe_difference = Decimal(segment['fringe_difference']) * (Decimal(segment['hours']['prevailing_rate_regular']) + Decimal(segment['hours']['prevailing_rate_overtime']) + Decimal(segment['hours']['prevailing_rate_doubletime']))
        fringe_cost = (Decimal(segment['pr_rates']['fringe_rate'])-Decimal(segment['total_fringe_rate'])) * Decimal(segment['hours']['work_hours'])
        total_cost = regular_cost + overtime_cost + doubletime_cost + fringe_cost
    else:
        # Calculate regular, overtime, and doubletime cost
        regular_cost = Decimal(segment['hours']['regular']) * Decimal(segment['rate'])
        overtime_cost = Decimal(segment['hours']['overtime']) * Decimal(segment['rate']) * Decimal('1.5')
        doubletime_cost = Decimal(segment['hours']['doubletime']) * Decimal(segment['rate']) * Decimal('2')
        total_cost = regular_cost + overtime_cost + doubletime_cost

    # Calculate travel cost
    travel_cost = Decimal(segment['hours']['travel_duration']) * Decimal(segment['rate'])
    total_cost += travel_cost

    # Return a dictionary that contains total_cost and travel_cost
    return {'total_cost': round(total_cost, 2), 'travel_cost': round(travel_cost, 2)}

def get_rate(employee_id, year) -> float:
    '''Get employee rate per hour'''
    rate = Decimal('0.00')  # Initialize rate to 0.00
    try:
        employee = Employee.objects.get(id=employee_id)
        rate_obj = EmployeeRate.objects.filter(employee=employee, effective_date__year=year).order_by('-effective_date').first()
        if not rate_obj:  # If no rate is found for the current year, try to get the rate for the previous year
            rate_obj = EmployeeRate.objects.filter(employee=employee, effective_date__year=year-1).order_by('-effective_date').first()
        if rate_obj:
            rate = rate_obj.rate if rate_obj.rate else Decimal('0.00')  # If no rate is found, set it to 0.00
    except ObjectDoesNotExist:
        pass
    return rate

def get_pr_rates(project_id, is_foremen, year) -> dict:
    '''Get prevailing rate per hour'''
    pr_rates = {'rate': Decimal('0.00'), 'fringe_rate': Decimal('0.00')}  # Initialize rate and fringe_rate to 0.00
    try:
        pr_obj = PrevailingRate.objects.filter(project_id=project_id, is_foremen=is_foremen, effective_date__year=year).order_by('-effective_date').first()
        if not pr_obj:  # If no rate is found for the current year, try to get the rate for the previous year
            pr_obj = PrevailingRate.objects.filter(project_id=project_id, is_foremen=is_foremen, effective_date__year=year-1).order_by('-effective_date').first()
        if pr_obj:
            pr_rates['rate'] = pr_obj.rate if pr_obj.rate else Decimal('0.00')  # If no rate is found, set it to 0.00
            pr_rates['fringe_rate'] = pr_obj.fringe_rate if pr_obj.fringe_rate else Decimal('0.00')  # If no fringe_rate is found, set it to 0.00
    except ObjectDoesNotExist:
        pass
    return pr_rates

def round_to_quarter_hour(time):
    '''Round time to the nearest quarter hour'''
    minutes = (time % 1) * 60  # Get the decimal part of the time and convert it to minutes
    rounded_minutes = round(minutes / 15) * 15  # Round to the nearest quarter hour
    return int(time) + rounded_minutes / 60  # Convert the rounded minutes back to hours and add it to the integer part of the time

def get_segment_hours(segment, prevailing_rate, accumulated_hours) -> dict:
    '''return hours for segment based on prevailing rate and accumulated hours'''
    travel_duration = round_to_quarter_hour(float(segment.travel_duration)) if segment.travel_duration else 0.0
    regular = 0
    overtime = 0
    doubletime = 0
    prevailing_rate_regular = 0
    prevailing_rate_overtime = 0
    prevailing_rate_doubletime = 0

    # Calculate the total hours worked in the segment
    start_time = datetime.strptime(str(segment.start_time), '%H:%M:%S') # Convert string to datetime
    end_time = datetime.strptime(str(segment.end_time), '%H:%M:%S') # Convert string to datetime
    total_hours = round_to_quarter_hour((end_time - start_time).seconds / 3600) # Convert seconds to hours and round to the nearest quarter hour
    
    if segment.lunch:
        total_hours -= 0.5  # Subtract lunch time

    work_hours = round_to_quarter_hour(total_hours - travel_duration)  # Exclude travel time and round to the nearest quarter hour
    
    if prevailing_rate and segment.segment_type.id == 2: # Prevailing rate calculation. segment must be of type 2 which is field work.
        date = segment.date
        if date.weekday() == 5:  # Saturday
            prevailing_rate_overtime = work_hours
        elif date.weekday() == 6:  # Sunday
            prevailing_rate_doubletime = work_hours
        else:
            if work_hours > 8:
                prevailing_rate_overtime = work_hours - 8
                prevailing_rate_regular = 8
            elif accumulated_hours + work_hours > 40:
                prevailing_rate_overtime = (accumulated_hours + work_hours) - 40
                prevailing_rate_regular = work_hours - prevailing_rate_overtime
            else:
                prevailing_rate_regular = work_hours
    else:
        date = segment.date
        if date.weekday() == 5:  # Saturday
            overtime = work_hours
        elif date.weekday() == 6:  # Sunday
            doubletime = work_hours
        else:
            if accumulated_hours + work_hours > 40: # Overtime calculation. If accumulated hours plus work hours is greater than 40, then overtime is calculated.
                overtime = (accumulated_hours + work_hours) - 40
                regular = work_hours - overtime
                if regular < 0:
                    regular = 0
            else:
                regular = work_hours

    accumulated_hours += work_hours  # Add work hours to accumulated hours after overtime calculation
    
    return {
        'travel_duration': travel_duration,
        'regular': regular,
        'overtime': overtime,
        'doubletime': doubletime,
        'prevailing_rate_regular': prevailing_rate_regular,
        'prevailing_rate_overtime': prevailing_rate_overtime,
        'prevailing_rate_doubletime': prevailing_rate_doubletime,
        'work_hours': work_hours,  # Return work hours
        'accumulated_hours': accumulated_hours  # Return new accumulated hours
    }

def create_project_dict(item, item_type):
    return {
        'project_id': item.id if item_type == 'project' else None,
        'project_number': item.number if item_type == 'project' else None,
        'project_name': item.name if item_type == 'project' else None,
        'service_id': item.id if item_type == 'service' else None,
        'service_number': item.number if item_type == 'service' else None,
        'service_name': item.name if item_type == 'service' else None,
        'quote_id': item.id if item_type == 'quote' else None,
        'quote_number': item.number if item_type == 'quote' else None,
        'quote_name': item.name if item_type == 'quote' else None,
        'hse_id': item.id if item_type == 'hse' else None,
        'hse_number': item.number if item_type == 'hse' else None,
        'hse_name': item.name if item_type == 'hse' else None,
        'prevailing_rate': item.prevailing_rate if item_type != 'quote' else False,
        'segments': []
    }

def get_employee_hours(employee_id, isoweek) -> dict:
    '''Get total hours worked by employee for the week'''
    projects_dict = {}
    accumulated_hours = 0  # Initialize accumulated hours
    year = int(isoweek[:4]) # Get year from isoweek
    try:
        employee = Employee.objects.get(id=employee_id)
        user = employee.user
        queryset = WorkSegment.objects.filter(user=user, isoweek=isoweek, is_approved=True).order_by('date', 'project', 'service', 'quote', 'hse')
        for segment in queryset:
            prevailing_rate = False
            for item_type in ['project', 'service', 'hse']:
                item = getattr(segment, item_type)
                if item and hasattr(item, 'prevailing_rate'):
                    prevailing_rate = item.prevailing_rate
                    break
            rate = get_rate(employee_id, year) 
            total_fringe_rate = get_total_fringe_rate(employee_id, year)  # Get total fringe rate
            segment_hours = get_segment_hours(segment, prevailing_rate, accumulated_hours)  # Get hours for segment
            accumulated_hours = segment_hours['accumulated_hours']  # Update accumulated hours
            for item_type in ['project', 'service', 'quote', 'hse']:
                item = getattr(segment, item_type)
                if item:
                    project_key = f"{item.number} {item.name}"
                    if project_key not in projects_dict:
                        projects_dict[project_key] = create_project_dict(item, item_type)
                    segment_dict = model_to_dict(segment)  # Convert segment to dict
                    segment_dict['hours'] = segment_hours  # Add hours to segment dict
                    # Add is_foremen, shift_differential, compressed_work_week, and total_fringe_rate to segment_dict
                    segment_dict['is_foremen'] = segment.is_foremen
                    segment_dict['shift_differential'] = segment.shift_differential
                    segment_dict['compressed_work_week'] = segment.compressed_work_week
                    segment_dict['total_fringe_rate'] = total_fringe_rate
                    segment_dict['rate'] = rate
                    if prevailing_rate and segment.segment_type.id == 2:
                        pr_rates = get_pr_rates(segment.project.id, segment.is_foremen, year)
                        segment_dict['pr_rates'] = pr_rates
                        segment_dict['fringe_difference'] = pr_rates['fringe_rate'] - total_fringe_rate
                    segment_dict['total_cost'] = calculate_total_segment_cost(segment_dict)  # Calculate total cost for segment
                    projects_dict[project_key]['segments'].append(segment_dict)  # Add segment to project

    except ObjectDoesNotExist:
        queryset = None

    return projects_dict

@csrf_exempt
def total_employee_hours(request, employee_id, isoweek):
    '''Get total fringe rate per hour for testing only'''
    if request.method == 'GET':
        total_employee_hours = get_employee_hours(employee_id, isoweek)
        data = {'total_employee_hours': total_employee_hours}
        return JsonResponse(data)

@csrf_exempt
def JobCosting(request, isoweek):
    '''Get total time for week'''
    if request.method == 'GET':
        try:
            projects_dict = {}
            qs = WorkSegment.objects.filter(isoweek=isoweek, is_approved=True).order_by('user__last_name', 'date', 'user__id', 'project', 'service', 'quote', 'hse')

            users_qs = qs.values('user__id', 'user__first_name', 'user__last_name', 'user__employee__id')
            users_list = list({d['user__id']: d for d in users_qs}.values())

            if not users_list:  # Check if the users_list is empty
                return JsonResponse(projects_dict)

            # Call get_employee_hours for each user and consolidate segments
            for user in users_list:
                employee_id = user['user__employee__id']
                employee_hours = get_employee_hours(employee_id, isoweek)
                consolidated_employee_hours = consolidate_segments(employee_hours)
                user['employee_hours'] = consolidated_employee_hours

            sorted_data = sort_segments_by_project(users_list)
            return JsonResponse(sorted_data, safe=False)

        except AttributeError:
            projects_dict = {}
            return JsonResponse(projects_dict)
        
def sort_segments_by_project(data):
    projects = []
    projects_dict = {}
    for employee in data:
        for project_name, project_data in employee['employee_hours'].items():
            if project_name not in projects_dict:
                project_data_copy = project_data.copy()  # Create a copy of the project data
                project_data_copy['segments'] = []
                projects_dict[project_name] = project_data_copy
                projects.append(project_data_copy)
            for segment in project_data['segments']:
                segment = segment.copy()  # Create a copy of the segment
                segment['employee_id'] = employee['user__id']
                segment['employee_name'] = f"{employee['user__first_name']} {employee['user__last_name']}"
                projects_dict[project_name]['segments'].append(segment)
    return projects


def worktype_to_dict(worktype):
    return {
        'id': worktype.id,
        'name': worktype.name,
    }

def consolidate_segments(employee_hours):
    consolidated = {}
    for project_key, project in employee_hours.items():
        consolidated[project_key] = project.copy()  # copy all project details
        consolidated_segments = {}  # will hold the consolidated segments
        for segment in project['segments']:
            segment_type_id = segment['segment_type']
            is_foremen = segment['is_foremen']
            key = (segment_type_id, is_foremen)  # create a composite key
            segment_type = worktype_to_dict(WorkType.objects.get(id=segment_type_id))  # fetch the WorkType object and convert it to a dictionary
            if key not in consolidated_segments:
                # if this key is not yet in consolidated_segments, copy it
                consolidated_segments[key] = {
                    'segment_type': segment_type,  # store the WorkType object instead of the id
                    'is_foremen': is_foremen,  # store is_foremen
                    'hours': {key: value for key, value in segment['hours'].items() if key not in ['work_hours', 'accumulated_hours']},
                    'total_cost': segment['total_cost'],  # total_cost is now a dictionary
                    'total_fringe_rate': segment['total_fringe_rate'],  # add total_fringe_rate
                    'rate': segment['rate'],  # add rate
                    'pr_rates': segment['pr_rates'] if 'pr_rates' in segment else None  # add pr_rates
                }
            else:
                # if this key is already in consolidated_segments, add the hours and total cost
                for hour_type, hours in segment['hours'].items():
                    if hour_type not in ['work_hours', 'accumulated_hours']:
                        consolidated_segments[key]['hours'][hour_type] += hours
                consolidated_segments[key]['total_cost']['total_cost'] += segment['total_cost']['total_cost']
                consolidated_segments[key]['total_cost']['travel_cost'] += segment['total_cost']['travel_cost']
        # replace the segments in the project with the consolidated segments
        consolidated[project_key]['segments'] = list(consolidated_segments.values())
    return consolidated
