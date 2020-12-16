from django.urls import path
from . import views

app_name = 'SBFapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('userprofile/', views.profile, name='profile'),
    path('chat/<str:room_name>/video/', views.videologin, name='video'),
    path('userprofile/edit/', views.profileedit, name = "profile_edit"),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('schedule/', views.ScheduleView.as_view(), name='schedule'),
    path('schedule/create-event', views.EventCreateView.as_view(), name='event_form'),
    path('community/', views.PostsListView.as_view(), name='community'),
    path('community/create-post', views.PostCreateView.as_view(), name='post_form'),
    path('community/<int:pk>/',views.PostView.as_view(),name='post'),
    path('community/<int:pk>/comment',views.CommentsView.as_view(),name='comment'),
    path('community/<int:pk>/join-group', views.join_study_buddy, name='join_study_buddy'),
    path('<int:pk>/event', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/event/edit', views.EventUpdateView.as_view(), name='event_edit'),
    path('<int:pk>/event/delete', views.EventDeleteView.as_view(), name='event_delete'),
    path('groups/',views.GroupsListView.as_view(),name='groupslist'),
    path('groups/create-group/',views.GroupsCreateView.as_view(),name='group_form'),
    path('groups/<int:pk>/',views.GroupsView.as_view(),name='group'),
    path('groups/<int:pk>/join-group/',views.join_group,name='group_add'),
    path('groups/<int:pk>/pre-edit', views.edit_group, name='edit_group'),
    path('groups/<int:pk>/edit/',views.GroupUpdateView.as_view() ,name='update_group'),
]

