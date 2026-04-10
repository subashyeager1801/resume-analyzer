from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze, name='analyze'),
    
    path('result/<int:analysis_id>/', views.result_detail, name='result_detail'),
    path('download/<int:analysis_id>/', views.download_pdf, name='download_pdf'),
]