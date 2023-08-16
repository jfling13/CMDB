from django.urls import path
from assets import views

app_name = 'assets'

urlpatterns = [
    path('', views.dashboard),
    path('index/', views.index, name="index"),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('detail/<int:asset_id>/', views.detail, name="detail"),
    path('report/', views.report, name='report'),
]