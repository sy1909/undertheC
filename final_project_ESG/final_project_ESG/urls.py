"""final_project_ESG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from final_project_ESG import views
from final_project_ESG import views2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('model_load/', views.model_load , name = 'model_load'),
    path('create_wordcloud/', views.create_wordcloud , name = 'create_wordcloud'),
    path('wordcloud2/', views.wordcloud2 , name = 'wordcloud2'),    
    path('model_load2/', views.model_load2 , name = 'model_load2'),   
    path('model_load_emission/', views2.model_load_emission , name = 'model_load_emission'),   
    
]
