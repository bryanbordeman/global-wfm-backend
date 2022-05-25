from django.urls import path
from . import views

urlpatterns = [
    path('worksegments/', views.WorkSegments.as_view()),
    path('create/worksegment/', views.WorkSegmentCreate.as_view()),
    path('create/worksegment/<int:user_id>/', views.WorkSegmentCreate.as_view()),
    path('worksegment/<int:pk>', views.WorkSegmentRetrieveUpdateDestroy.as_view()),
    path('worksegment/<int:pk>/approved/', views.WorkSegmentToggleApproved.as_view()),
    path('worksegments/<str:isoweek>/', views.WorkSegmentsWeek.as_view()),
    path('admin/worksegments/<str:isoweek>/', views.AdminWorkSegmentsWeek.as_view()),
    path('announcement/', views.Announcement.as_view()),
    path('signup/', views.signup),
    path('login/', views.login),
]