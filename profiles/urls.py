from django.urls import path
from .views import (
    profile_test_view, 
    profile_my_view,
    MyProfileData, 
    MyProfileView,
    invites_received_view,
    profiles_list_view,
    invites_profiles_list_view,
    ProfileListView,
    send_invatation,
    remove_from_friends,
    accept_invatation,
    reject_invatation,
    ProfileDetailView,
    # SearchResultsView,
    )

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name="all-profiles-view"),
    path('my/', profile_my_view, name="my-profile-view"),
    path('my-invites/', invites_received_view, name="my-invites-view"),
    path('to-invite/', invites_profiles_list_view, name="invite-profiles-view"),
    path('send-invite/',send_invatation, name="send-invite"),
    path('remove-friend/',remove_from_friends, name="remove-friend"),
    path('<slug>/', ProfileDetailView.as_view(), name="profile-detail-view"),
    path('my-invites/accept/', accept_invatation, name="accept-invite"),
    path('my-invites/reject/', reject_invatation, name="reject-invite"),
    path('my-profile-json/', MyProfileData.as_view(), name='my-profile-json'),
    # path('search/', SearchResultsView.as_view(), name='search_results'),
]
