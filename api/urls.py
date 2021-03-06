from django.urls import path
from . import views_worksegment
from . import views_announcement
from . import views_project
from . import views_expense
from . import views_user
from . import views_task
from . import views_user


urlpatterns = [
    path('worksegments/', views_worksegment.WorkSegments.as_view()),
    path('create/worksegment/<int:user_id>/', views_worksegment.WorkSegmentCreate.as_view()),
    path('worksegment/<int:pk>', views_worksegment.WorkSegmentRetrieveUpdateDestroy.as_view()),
    path('worksegment/<int:pk>/approved/', views_worksegment.WorkSegmentToggleApproved.as_view()),
    path('worksegments/<str:isoweek>/', views_worksegment.WorkSegmentsWeek.as_view()),
    path('admin/worksegments/<str:isoweek>/', views_worksegment.AdminWorkSegmentsWeek.as_view()),
    path('announcement/', views_announcement.Announcement.as_view()),
    path('create/announcement/', views_announcement.AnnouncementCreate.as_view()),
    path('announcement/<int:pk>', views_announcement.AnnouncementRetrieveUpdateDestroy.as_view()),
    path('projects/', views_project.Project.as_view()),
    path('create/project/', views_project.ProjectCreate.as_view()),
    path('project/<int:pk>', views_project.ProjectRetrieveUpdateDestroy.as_view()),
    path('expenses/<int:month>', views_expense.Expense.as_view()),
    path('create/expense/<int:user_id>/', views_expense.ExpenseCreate.as_view()),
    path('expense/<int:pk>', views_expense.ExpenseRetrieveUpdateDestroy.as_view()),
    path('expense/<int:pk>/approved/', views_expense.ExpenseToggleApproved.as_view()),
    path('miles/<int:month>', views_expense.Mile.as_view()),
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
    path('subtask/<int:pk>/completed/', views_task.SubtaskToggleCompleted.as_view()),
    path('subtask/<int:pk>', views_task.SubtaskRetrieveUpdateDestroy.as_view()),
    path('create/subtask/', views_task.SubtaskCreate.as_view()),
    path('users/', views_user.UserView.as_view()),
    path('signup/', views_user.signup),
    path('login/', views_user.login),
]