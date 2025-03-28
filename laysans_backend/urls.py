from django.contrib import admin
from django.urls import path
from Api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URL for sending a normal mail (contact us)
    path('mail/', views.Mail.as_view(), name='send_mail'), 
    
    # URL for career-related emails (sending resume)
    path('careermail/', views.CareerMail.as_view(), name='career_mail'),

    # URL for fetching clients (list and detail)
    path('client/', views.ClientAPI.as_view(), name='client_list'),  # Fetch all clients
    # URL for fetching career entries (list and detail)
    path('career/', views.CareersAPI.as_view(), name='career_list'),  # Fetch all career entries
    path('career/<int:id>/', views.CareersAPI.as_view()),
    path('chatai/', views.ChatAIView.as_view(), name='chatai'),
    ]