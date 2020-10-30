from django.contrib import admin
from django.urls import path, include
from api.views import AccountGeneralView, RootView, OperationGeneralView

urlpatterns = [
    path('accounts/', AccountGeneralView.as_view()),
    path('operations/', OperationGeneralView.as_view()),
    path('', RootView.as_view())
]
