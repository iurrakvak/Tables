from django.contrib import admin
from django.urls import path, include
from api.views import *

urlpatterns = [
    path('accounts/', AccountGeneralView.as_view()),
    path('accounts/top', AccountTopView.as_view())
]
