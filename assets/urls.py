from django.urls import path,include
from assets import views
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings

app_name = 'assets'

urlpatterns = [
    path('', views.dashboard),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('login/',views.login, name="login"),
    path('index/', views.index, name="index"),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('detail/<int:asset_id>/', views.detail, name="detail"),
    path('report/', views.report, name='report'),
    path('logout/',views.logout,name='logout'),
    
]