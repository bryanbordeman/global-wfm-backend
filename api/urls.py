from django.urls import path
from . import views_worksegment
from . import views_announcement
from . import views_project
from . import views_expense
from . import views_user


urlpatterns = [
    path('worksegments/', views_worksegment.WorkSegments.as_view()),
    path('create/worksegment/', views_worksegment.WorkSegmentCreate.as_view()),
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
    path('expenses/', views_expense.Expense.as_view()),
    path('create/expense/', views_expense.ExpenseCreate.as_view()),
    path('expense/<int:pk>', views_expense.ExpenseRetrieveUpdateDestroy.as_view()),
    path('signup/', views_user.signup),
    path('login/', views_user.login),
]