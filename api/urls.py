from django.urls import path
from . import views
from . import views_announcement
from . import views_user

urlpatterns = [
    path('worksegments/', views.WorkSegments.as_view()),
    path('create/worksegment/', views.WorkSegmentCreate.as_view()),
    path('create/worksegment/<int:user_id>/', views.WorkSegmentCreate.as_view()),
    path('worksegment/<int:pk>', views.WorkSegmentRetrieveUpdateDestroy.as_view()),
    path('worksegment/<int:pk>/approved/', views.WorkSegmentToggleApproved.as_view()),
    path('worksegments/<str:isoweek>/', views.WorkSegmentsWeek.as_view()),
    path('admin/worksegments/<str:isoweek>/', views.AdminWorkSegmentsWeek.as_view()),
    path('announcement/', views_announcement.Announcement.as_view()),
    path('create/announcement/', views_announcement.AnnouncementCreate.as_view()),
    path('announcement/<int:pk>', views_announcement.AnnouncementRetrieveUpdateDestroy.as_view()),
    path('signup/', views_user.signup),
    path('login/', views_user.login),
]