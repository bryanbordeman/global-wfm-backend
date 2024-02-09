from worksegment.models import WorkSegment
from employee.models import Employee, EmployeeRate, EmployeeBenefit, PrevailingRate
from project.models import Project
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum
from django.forms.models import model_to_dict

# Constants
HOURS_IN_YEAR = 2080

def get_total_fringe_rate(employee_id, year) -> float:
    '''Get total fringe rate per hour'''
    total_fringe_rate = 0
    try:
        employee = Employee.objects.get(id=employee_id)
        rate_obj = EmployeeRate.objects.filter(employee=employee, effective_date__year=year).order_by('-effective_date').first()
        rate = rate_obj.rate if rate_obj else None
        if rate:
            total_benefits = sum(benefit.amount if benefit.employer_paid else -benefit.amount for benefit in EmployeeBenefit.objects.filter(employee=employee)) * 12
            fringe_rate = ((employee.vacation_hours * rate) + (employee.sick_hours * rate) + (employee.holiday_hours * rate) + total_benefits) / HOURS_IN_YEAR
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

def calculate_total_segment_cost(segment) -> float:
    '''Calculate total cost for a segment'''
    if segment['hours']['prevailing_rate_regular'] or segment['hours']['prevailing_rate_overtime'] or segment['hours']['prevailing_rate_doubletime']:
        # Calculate prevailing rate regular, overtime, and doubletime cost
        regular_cost = Decimal(segment['hours']['prevailing_rate_regular']) * segment['pr_rates']['rate']
        overtime_cost = Decimal(segment['hours']['prevailing_rate_overtime']) * segment['pr_rates']['rate'] * Decimal('1.5')
        doubletime_cost = Decimal(segment['hours']['prevailing_rate_doubletime']) * segment['pr_rates']['rate'] * Decimal('2')
        fringe_difference = Decimal(segment['fringe_difference']) * (Decimal(segment['hours']['prevailing_rate_regular']) + Decimal(segment['hours']['prevailing_rate_overtime']) + Decimal(segment['hours']['prevailing_rate_doubletime']))
        total_cost = regular_cost + overtime_cost + doubletime_cost + fringe_difference
    else:
        # Calculate regular, overtime, and doubletime cost
        regular_cost = Decimal(segment['hours']['regular']) * Decimal(segment['rate'])
        overtime_cost = Decimal(segment['hours']['overtime']) * Decimal(segment['rate']) * Decimal('1.5')
        doubletime_cost = Decimal(segment['hours']['doubletime']) * Decimal(segment['rate']) * Decimal('2')
        total_cost = regular_cost + overtime_cost + doubletime_cost

    # Calculate travel cost
    travel_cost = Decimal(segment['hours']['travel_duration']) * Decimal(segment['rate'])
    total_cost += travel_cost
    return round(total_cost, 2)

def get_rate(employee_id, year) -> float:
    '''Get employee rate per hour'''
    try:
        employee = Employee.objects.get(id=employee_id)
        rate_obj = EmployeeRate.objects.filter(employee=employee, effective_date__year=year).order_by('-effective_date').first()
        rate = rate_obj.rate if rate_obj else None
    except ObjectDoesNotExist:
        rate = None
    return rate

def get_pr_rates(project_id, is_foremen, year) -> dict:
    '''Get prevailing rate per hour'''
    pr_rates = {'rate': None, 'fringe_rate': None}
    try:
        pr_obj = PrevailingRate.objects.filter(project_id=project_id, is_foremen=is_foremen, effective_date__year=year).order_by('-effective_date').first()
        if pr_obj:
            pr_rates['rate'] = pr_obj.rate
            pr_rates['fringe_rate'] = pr_obj.fringe_rate
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
    from datetime import datetime
    travel_duration = round_to_quarter_hour(float(segment.travel_duration))
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
        'segments': [],
        'prevailing_rate': item.prevailing_rate if item_type != 'quote' else False
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
                    if item.id not in projects_dict:
                        projects_dict[item.id] = create_project_dict(item, item_type)
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
                    projects_dict[item.id]['segments'].append(segment_dict)  # Add segment to project

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
def PayrollTotals(request, isoweek):
    '''Get total time for week'''
    if request.method == 'GET':
        try:
            projects_dict = {}
            user_hours = defaultdict(int)  # Dictionary to keep track of total hours worked by each user
            qs = WorkSegment.objects.filter(isoweek=isoweek, is_approved=True).order_by('user__last_name', 'date', 'user__id', 'project', 'service', 'quote', 'hse')

            for i in qs:
                if i.project:
                    if i.project.id not in projects_dict:
                        projects_dict[i.project.id] = {
                            'project_id': i.project.id,
                            'project_number': i.project.number,
                            'project_name': i.project.name,
                            'service_id': None,
                            'service_number': None,
                            'service_name': None,
                            'quote_id': None,
                            'quote_number': None,
                            'quote_name': None,
                            'hse_id': None,
                            'hse_number': None,
                            'hse_name': None,
                            'segments': [],
                            'prevailing_rate': i.project.prevailing_rate
                        }
                if i.service:
                    if i.service.id not in projects_dict:
                        projects_dict[i.service.id] = {
                            'project_id': None,
                            'project_number': None,
                            'project_name': None,
                            'service_id': i.service.id,
                            'service_number': i.service.number,
                            'service_name': i.service.name,
                            'quote_id': None,
                            'quote_number': None,
                            'quote_name': None,
                            'hse_id': None,
                            'hse_number': None,
                            'hse_name': None,
                            'segments': [],
                            'prevailing_rate': i.service.prevailing_rate
                        }
                if i.quote:
                    if i.quote.id not in projects_dict:
                        projects_dict[i.quote.id] = {
                            'project_id': None,
                            'project_number': None,
                            'project_name': None,
                            'service_id': None,
                            'service_number': None,
                            'service_name': None,
                            'quote_id': i.quote.id,
                            'quote_number': i.quote.number,
                            'quote_name': i.quote.name,
                            'hse_id': None,
                            'hse_number': None,
                            'hse_name': None,
                            'segments': [],
                            'prevailing_rate': False  # Update this as needed
                        }
                if i.hse:
                    if i.hse.id not in projects_dict:
                        projects_dict[i.hse.id] = {
                            'project_id': None,
                            'project_number': None,
                            'project_name': None,
                            'service_id': None,
                            'service_number': None,
                            'service_name': None,
                            'quote_id': None,
                            'quote_number': None,
                            'quote_name': None,
                            'hse_id': i.hse.id,
                            'hse_number': i.hse.number,
                            'hse_name': i.hse.name,
                            'segments': [],
                            'prevailing_rate': i.hse.prevailing_rate
                        }

                # Calculate total hours worked by the user excluding travel hour
                travel_duration = i.travel_duration if i.travel_duration is not None else 0
                work_hours = i.duration - travel_duration
                user_hours[i.user.id] += work_hours


                prevailing_rate = False
                if i.project:
                    prevailing_rate = i.project.prevailing_rate
                elif i.service:
                    prevailing_rate = i.service.prevailing_rate
                elif i.quote:
                    prevailing_rate = i.quote.prevailing_rate
                elif i.hse:
                    prevailing_rate = i.hse.prevailing_rate

                # Initialize doubletime
                doubletime = 0
                # Determine if the hours are regular, overtime, or doubletime
                day_of_week = i.date.weekday()
                if prevailing_rate and i.segment_type_id == 2:
                    if work_hours > 8:
                        regular = 8
                        overtime = work_hours - 8
                    else:
                        regular = work_hours
                        overtime = 0
                    accumulated_regular += regular
                elif day_of_week == 5:  # Saturday
                    regular = 0
                    overtime = work_hours
                    accumulated_regular += regular
                elif day_of_week == 6:  # Sunday
                    regular = 0
                    overtime = 0
                    doubletime = work_hours
                else:
                    if user_hours[i.user.id] <= 40:
                        regular = work_hours
                        overtime = 0
                        accumulated_regular = user_hours[i.user.id]
                    else:
                        if user_hours[i.user.id] - work_hours < 40:
                            regular = 40 - (user_hours[i.user.id] - work_hours)
                            overtime = work_hours - regular
                            accumulated_regular = 40
                        else:
                            regular = 0
                            overtime = work_hours
                            accumulated_regular = user_hours[i.user.id]
                
                try:
                    employee = Employee.objects.get(user_id=i.user.id)
                    rate_obj = EmployeeRate.objects.filter(employee=employee).order_by('-effective_date').first()
                    rate = rate_obj.rate if rate_obj else None
                except ObjectDoesNotExist:
                    rate = None

                segment = {
                    'segment_type_id': i.segment_type.id,
                    'segment_type_name': i.segment_type.name,
                    'user_id': i.user.id,
                    'employee': f'{i.user.last_name}, {i.user.first_name}',
                    'date': i.date,
                    'start_time': i.start_time,
                    'end_time': i.end_time,
                    'lunch': i.lunch,
                    'travel_duration': i.travel_duration,
                    'total_duration': i.duration,
                    'regular': regular,
                    'overtime': overtime,
                    'doubletime': doubletime,
                    'accumulated_regular': accumulated_regular,
                    'notes': i.notes,
                    'prevailing_rate': prevailing_rate,
                    'rate': rate 
                }

                if i.project and i.project.id in projects_dict:
                    projects_dict[i.project.id]['segments'].append(segment)
                if i.service and i.service.id in projects_dict:
                    projects_dict[i.service.id]['segments'].append(segment)
                if i.quote and i.quote.id in projects_dict:
                    projects_dict[i.quote.id]['segments'].append(segment)
                if i.hse and i.hse.id in projects_dict:
                    projects_dict[i.hse.id]['segments'].append(segment)

        except AttributeError:
            projects_dict = {}

        # Condense segments for each project
        for project in projects_dict.values():
            project['segments'] = condense_segments(project['segments'])

        # Calculate total costs for each project
        for project in projects_dict.values():
            project['total_regular_cost'] = sum(segment['regular_cost'] for segment in project['segments'])
            project['total_overtime_cost'] = sum(segment['overtime_cost'] for segment in project['segments'])
            project['total_doubletime_cost'] = sum(segment['doubletime_cost'] for segment in project['segments'])
            project['total_travel_cost'] = sum(segment['travel_cost'] for segment in project['segments'])

        return JsonResponse(list(projects_dict.values()), json_dumps_params={'indent': 2}, safe=False)

def condense_segments(segments):
    condensed_segments = defaultdict(lambda: {'user_id': None, 'segment_type_name': None, 'segment_type_id': None, 'employee': None, 'regular': 0, 'overtime': 0, 'doubletime': 0, 'travel_duration': 0})

    for segment in segments:
        user_id = segment['user_id']
        segment_type_id = segment['segment_type_id']
        segment_type_name = segment['segment_type_name']
        key = (user_id, segment_type_id)  # Group by both user_id and segment_type_id

        travel_duration = float(segment['travel_duration']) if segment['travel_duration'] is not None else 0.0
        rate = segment['rate'] if segment['rate'] is not None else 0.0

        travel_cost = (rate * Decimal(travel_duration)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        regular_cost = (rate * Decimal(segment['regular'])).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        overtime_cost = ((rate * Decimal(1.5)) * Decimal(segment['overtime'])).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        doubletime_cost = ((rate * Decimal(2)) * Decimal(segment['doubletime'])).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

        condensed_segments[key]['user_id'] = user_id
        condensed_segments[key]['segment_type_id'] = segment_type_id
        condensed_segments[key]['segment_type_name'] = segment_type_name
        condensed_segments[key]['employee'] = segment['employee']
        condensed_segments[key]['regular'] += float(segment['regular'])
        condensed_segments[key]['overtime'] += float(segment['overtime'])
        condensed_segments[key]['doubletime'] += float(segment['doubletime'])
        condensed_segments[key]['travel_duration'] += travel_duration
        condensed_segments[key]['prevailing_rate'] = segment_type_id == 2 and segment['prevailing_rate']
        condensed_segments[key]['base_rate'] = rate
        condensed_segments[key]['pr_rate'] = rate if segment_type_id == 2 and segment['prevailing_rate'] else None
        condensed_segments[key]['travel_cost'] = travel_cost 
        condensed_segments[key]['regular_cost'] = regular_cost
        condensed_segments[key]['overtime_cost'] = overtime_cost
        condensed_segments[key]['doubletime_cost'] = doubletime_cost

    return list(condensed_segments.values())
