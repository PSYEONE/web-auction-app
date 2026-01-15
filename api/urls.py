from django.contrib import admin
from django.urls import include, path
from .views import main_spa, CustomLoginView, SignUpView, logout_view

urlpatterns = [
    path('', main_spa, name='spa_home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/', include('auction.urls')),
    path('admin/', admin.site.urls),
]