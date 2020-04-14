from django.urls import path
from author import views

urlpatterns = [
    path('who-am-i/', views.LoggedInUserAPI.as_view(), name='logged-in-user-detail'),
    path('user/<int:user_id>/<str:follow_type>/', views.FollowAPI.as_view(), name='follow-user'),
    path('user/<int:user_id>/', views.UserAPI.as_view(), name='user-detail'),
    path('passion/', views.PassionListView.as_view(), name='passion-list'),

]
