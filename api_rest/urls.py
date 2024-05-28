from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    path('users/', views.get_users, name='get_all_users'), #
    path('ask/', views.ask_question, name='ask_questions'), 
    # path('', views.index, name='index'),  # URL do frontend
    path('', TemplateView.as_view(template_name='frontend/build/index.html'), name='index'),  # URL principal para o frontend React

    # path('user/<str:nick>', views.get_by_nick), #pequisar por nick str porque é string, poderia ser int também
    # path('data/', views.user_manager)
]