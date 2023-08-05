from django.urls import path
from . import views_worksegment
from . import views_announcement
from . import views_project
from . import views_address
from . import views_contact
from . import views_phone
from . import views_company
from . import views_quote
from . import views_expense
from . import views_user
from . import views_task
from . import views_user
from . import views_stats
from . import views_vehicle
from . import views_uploader
from . import views_asset

urlpatterns = [
    path('asset/door/attributes', views_asset.DoorAttributesViewset.as_view()),
    path('asset/door/reports', views_asset.DoorReportViewset.as_view()),
    path('asset/create/door/report', views_asset.DoorReportCreate.as_view()),
    path('asset/door/report/<int:pk>', views_asset.DoorReportRetrieveUpdateDestroy.as_view()),

    path('asset/door/revs', views_asset.DoorRevViewset.as_view()),
    path('asset/create/door/rev', views_asset.DoorRevCreate.as_view()),
    path('asset/door/rev/<int:pk>', views_asset.DoorRevRetrieveUpdateDestroy.as_view()),

    path('asset/door/locksets', views_asset.DoorLocksetViewset.as_view()),
    path('asset/create/door/lockset', views_asset.DoorLocksetCreate.as_view()),
    path('asset/door/lockset/<int:pk>', views_asset.DoorLocksetRetrieveUpdateDestroy.as_view()),

    path('asset/door/types', views_asset.DoorTypeViewset.as_view()),
    path('asset/create/door/type', views_asset.DoorTypeCreate.as_view()),
    path('asset/door/type/<int:pk>', views_asset.DoorTypeRetrieveUpdateDestroy.as_view()),

    path('asset/door/sills', views_asset.DoorSillTypeViewset.as_view()),
    path('asset/create/door/sill', views_asset.DoorSillTypeCreate.as_view()),
    path('asset/door/sill/<int:pk>', views_asset.DoorSillTypeRetrieveUpdateDestroy.as_view()),

    path('asset/door/frames', views_asset.DoorFrameTypeViewset.as_view()),
    path('asset/create/door/frame', views_asset.DoorFrameTypeCreate.as_view()),
    path('asset/door/frame/<int:pk>', views_asset.DoorFrameTypeRetrieveUpdateDestroy.as_view()),

    path('asset/door/cores', views_asset.DoorCoreTypeViewset.as_view()),
    path('asset/create/door/core', views_asset.DoorCoreTypeCreate.as_view()),
    path('asset/door/core/<int:pk>', views_asset.DoorCoreTypeRetrieveUpdateDestroy.as_view()),

    path('asset/door/hinges', views_asset.DoorHingeTypeViewset.as_view()),
    path('asset/create/door/hinge', views_asset.DoorHingeTypeCreate.as_view()),
    path('asset/door/hinge/<int:pk>', views_asset.DoorHingeTypeRetrieveUpdateDestroy.as_view()),

    path('asset/door/options', views_asset.DoorOptionsViewset.as_view()),
    path('asset/create/door/option', views_asset.DoorOptionsCreate.as_view()),
    path('asset/door/option/<int:pk>', views_asset.DoorOptionsRetrieveUpdateDestroy.as_view()),

    path('asset/door/packaging', views_asset.DoorPackagingViewset.as_view()),
    path('asset/create/door/packaging', views_asset.DoorPackagingCreate.as_view()),
    path('asset/door/packaging/<int:pk>', views_asset.DoorPackagingRetrieveUpdateDestroy.as_view()),

    path('asset/doors', views_asset.DoorViewset.as_view()),
    path('asset/create/door', views_asset.DoorCreate.as_view()),
    path('asset/door/<int:pk>', views_asset.DoorRetrieveUpdateDestroy.as_view()),
    path('asset/portal/door/<int:pk>', views_asset.DoorRetrieve.as_view()),
    path('asset/complete/door/<int:pk>', views_asset.DoorToggleCompleted.as_view()),
    path('asset/door/project/<int:project>', views_asset.DoorProjectList.as_view()),
    path('asset/door/project/count/<int:project>', views_asset.DoorProjectCount.as_view()),

    path('drawings/', views_uploader.DrawingViewset.as_view()),
    path('drawings/project/<int:project_id>', views_uploader.DrawingProject.as_view()),
    path('drawings/service/<int:service_id>', views_uploader.DrawingService.as_view()),
    path('drawings/hse/<int:hse_id>', views_uploader.DrawingHSE.as_view()),
    path('create/drawing/', views_uploader.DrawingCreate.as_view()),
    path('drawing/<int:pk>', views_uploader.DrawingRetrieveUpdateDestroy.as_view()),

    path('drawing_types/', views_uploader.DrawingTypeView.as_view()),
    path('create/drawing_type/', views_uploader.DrawingTypeCreate.as_view()),
    path('drawing_type/<int:pk>', views_uploader.DrawingTypeRetrieveUpdateDestroy.as_view()),

    path('dropboxes/', views_uploader.DropBoxViewset.as_view()),
    path('create/dropbox/', views_uploader.DropBoxCreate.as_view()),
    path('dropbox/<int:pk>', views_uploader.DropBoxRetrieveUpdateDestroy.as_view()),

    path('stats/<int:year>', views_stats.Stats),
    path('worksegments/', views_worksegment.WorkSegments.as_view()),
    path('worktypes/', views_worksegment.WorkTypes.as_view()),
    path('create/worksegment/<int:user_id>/', views_worksegment.WorkSegmentCreate.as_view()),
    path('worksegment/<int:pk>', views_worksegment.WorkSegmentRetrieveUpdateDestroy.as_view()),
    path('worksegment/<int:pk>/approved/', views_worksegment.WorkSegmentToggleApproved.as_view()),
    path('worksegments/<str:isoweek>/', views_worksegment.WorkSegmentsWeek.as_view()),
    path('admin/worksegments/<str:isoweek>/', views_worksegment.AdminWorkSegmentsWeek.as_view()),
    path('worksegments/totals/<str:isoweek>/', views_worksegment.WorksegmentTotals),

    path('pto/', views_worksegment.PTOs.as_view()),
    path('create/pto/<int:user_id>/', views_worksegment.PTOCreate.as_view()),
    path('pto/<int:pk>', views_worksegment.PTORetrieveUpdateDestroy.as_view()),
    path('pto/<int:pk>/approved/', views_worksegment.PTOToggleApproved.as_view()),
    path('pto/<str:isoweek>/', views_worksegment.PTOWeek.as_view()),
    path('admin/pto/<str:isoweek>/', views_worksegment.AdminPTOWeek.as_view()),

    path('announcement/', views_announcement.Announcement.as_view()),
    path('create/announcement/', views_announcement.AnnouncementCreate.as_view()),
    path('announcement/<int:pk>', views_announcement.AnnouncementRetrieveUpdateDestroy.as_view()),

    path('addresses/', views_address.Address.as_view()),
    path('create/address/', views_address.AddressCreate.as_view()),
    path('address/<int:pk>', views_address.AddressRetrieveUpdateDestroy.as_view()),
    path('address/lookup/<str:place_id>', views_address.AddressLookup.as_view()),

    path('contacts/', views_contact.Contact.as_view()),
    path('create/contact/', views_contact.ContactCreate.as_view()),
    path('contact/<int:pk>', views_contact.ContactRetrieveUpdateDestroy.as_view()),
    path('contact/quote/<int:quote_id>', views_contact.ContactQuote.as_view()),
    path('contact/project/<int:project_id>', views_contact.ContactProject.as_view()),
    path('contact/service/<int:service_id>', views_contact.ContactService.as_view()),
    path('contact/hse/<int:hse_id>', views_contact.ContactHSE.as_view()),
    path('contact/company/<int:company_id>', views_contact.ContactCompany.as_view()),
    path('phone_numbers/', views_phone.Phone.as_view()),
    path('create/phone_number/', views_phone.PhoneCreate.as_view()),
    path('phone_number/<int:pk>', views_phone.PhoneRetrieveUpdateDestroy.as_view()),

    path('companies/', views_company.Company.as_view()),
    path('companies/short/', views_company.CompanyShort.as_view()),
    path('create/company/', views_company.CompanyCreate.as_view()),
    path('company/<int:pk>', views_company.CompanyRetrieveUpdateDestroy.as_view()),
    path('company/short/<int:pk>', views_company.CompanyRetrieveUpdateDestroyShort.as_view()),

    path('vehicles/', views_vehicle.Vehicle.as_view()),
    path('create/vehicle/', views_vehicle.VehicleCreate.as_view()),
    path('vehicle/<int:pk>', views_vehicle.VehicleRetrieveUpdateDestroy.as_view()),

    path('vehicle/issues/', views_vehicle.VehicleIssue.as_view()),
    path('create/vehicle/issue/', views_vehicle.VehicleIssueCreate.as_view()),
    path('vehicle/issue/<int:pk>', views_vehicle.VehicleIssueRetrieveUpdateDestroy.as_view()),

    path('vehicle/inspections/', views_vehicle.VehicleInspection.as_view()),
    path('create/vehicle/inspection/', views_vehicle.VehicleInspectionCreate.as_view()),
    path('vehicle/inspection/<int:pk>', views_vehicle.VehicleInspectionRetrieveUpdateDestroy.as_view()),

    path('vehicle/services/<int:year>', views_vehicle.VehicleService.as_view()),
    path('create/vehicle/service/', views_vehicle.VehicleServiceCreate.as_view()),
    path('vehicle/service/<int:pk>', views_vehicle.VehicleServiceRetrieveUpdateDestroy.as_view()),

    path('vehicle/cleanings/<int:year>', views_vehicle.VehicleCleaning.as_view()),
    path('create/vehicle/cleaning/', views_vehicle.VehicleCleaningCreate.as_view()),
    path('vehicle/cleaning/<int:pk>', views_vehicle.VehicleCleaningRetrieveUpdateDestroy.as_view()),

    path('quotes/', views_quote.Quote.as_view()),
    path('quotes/<int:year>', views_quote.QuoteYear.as_view()),
    path('quotes/archive/<int:year>', views_quote.QuoteArchive.as_view()),
    path('quote/<int:pk>/togglearchive/', views_quote.QuoteToggleArchive.as_view()),
    path('next/quote/', views_quote.NextQuoteNumber),
    path('last/quote/', views_quote.LastQuote),
    path('create/quote/', views_quote.QuoteCreate.as_view()),
    path('quote/<int:pk>', views_quote.QuoteRetrieveUpdateDestroy.as_view()),
    path('quotes/data/<int:year>', views_quote.QuoteData),

    path('project/categories/', views_project.ProjectCategory.as_view()),
    path('project/types/', views_project.ProjectType.as_view()),
    path('project/billings/', views_project.BillingType.as_view()),
    path('project/orders/', views_project.OrderType.as_view()),
    path('project/category/<int:pk>', views_project.ProjectCategoryRetrieveUpdateDestroy.as_view()),
    path('project/type/<int:pk>', views_project.ProjectTypeRetrieveUpdateDestroy.as_view()),
    path('projects/', views_project.Project.as_view()),
    path('projects/minimal', views_project.MinimalProject.as_view()),

    path('projects/<int:year>', views_project.ProjectYear.as_view()),
    path('projects/archive/<int:year>', views_project.ProjectArchive.as_view()),
    path('project/<int:pk>/togglearchive/', views_project.ProjectToggleArchive.as_view()),
    path('create/project/', views_project.ProjectCreate.as_view()),
    path('project/<int:pk>', views_project.ProjectRetrieveUpdateDestroy.as_view()),
    path('services/', views_project.Service.as_view()),
    path('services/<int:year>', views_project.ServiceYear.as_view()),
    path('services/archive/<int:year>', views_project.ServiceArchive.as_view()),
    path('service/<int:pk>/togglearchive/', views_project.ServiceToggleArchive.as_view()),
    path('create/service/', views_project.ServiceCreate.as_view()),
    path('service/<int:pk>', views_project.ServiceRetrieveUpdateDestroy.as_view()),
    path('hses/', views_project.HSE.as_view()),
    path('hses/<int:year>', views_project.HSEYear.as_view()),
    path('hses/archive/<int:year>', views_project.HSEArchive.as_view()),
    path('hse/<int:pk>/togglearchive/', views_project.HSEToggleArchive.as_view()),
    path('create/hse/', views_project.HSECreate.as_view()),
    path('hse/<int:pk>', views_project.HSERetrieveUpdateDestroy.as_view()),
    path('next/project/', views_project.NextProjectNumber),
    path('last/project/', views_project.LastProject),

    path('expenses/<int:month>/<int:year>', views_expense.Expense.as_view()),
    path('create/expense/<int:user_id>/', views_expense.ExpenseCreate.as_view()),
    path('expense/<int:pk>', views_expense.ExpenseRetrieveUpdateDestroy.as_view()),
    path('expense/<int:pk>/approved/', views_expense.ExpenseToggleApproved.as_view()),
    path('miles/<int:month>/<int:year>', views_expense.Mile.as_view()),
    path('create/mile/<int:user_id>/', views_expense.MileCreate.as_view()),
    path('mile/<int:pk>', views_expense.MileRetrieveUpdateDestroy.as_view()),
    path('mile/<int:pk>/approved/', views_expense.MileToggleApproved.as_view()),
    path('milerates/', views_expense.MileRates.as_view()),

    path('tasks/<int:assignee>/', views_task.TaskAssignee.as_view()),
    path('tasks/<int:assignee>/<int:tasklist>/', views_task.TaskAssigneeList.as_view()),
    path('complete/tasks/<int:assignee>/<int:tasklist>/', views_task.TaskAssigneeCompleteList.as_view()),
    path('tasklist/', views_task.TaskList.as_view()),
    path('create/task/', views_task.TaskCreate.as_view()),
    path('task/<int:pk>/completed/', views_task.TaskToggleCompleted.as_view()),
    path('task/<int:pk>', views_task.TaskRetrieveUpdateDestroy.as_view()),
    path('task/project/<int:project>', views_task.TaskProject.as_view()),
    path('task/service/<int:service>', views_task.TaskService.as_view()),
    path('task/hse/<int:hse>', views_task.TaskHSE.as_view()),
    path('task/quote/<int:quote>', views_task.TaskQuote.as_view()),
    path('subtask/<int:pk>/completed/', views_task.SubtaskToggleCompleted.as_view()),
    path('subtask/<int:pk>', views_task.SubtaskRetrieveUpdateDestroy.as_view()),
    path('create/subtask/', views_task.SubtaskCreate.as_view()),

    path('users/', views_user.UserView.as_view()),
    path('signup/', views_user.signup),
    path('login/', views_user.login),
    path('is_active/', views_user.is_active),
]