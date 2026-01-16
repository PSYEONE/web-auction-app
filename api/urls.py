from django.contrib import admin
from django.urls import include, path, re_path
from .views import main_spa, CustomLoginView, SignUpView, logout_view, UserProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/', include('auction.urls')),

    # Serve Vue SPA for all other routes (must be last)
    re_path(r'^.*$', main_spa, name='spa_catchall'),
]
