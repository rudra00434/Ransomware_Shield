from django.urls import path
from .views import AIChatView, NetworkAnalysisView

urlpatterns = [
    path('chat/', AIChatView.as_view(), name='ai_chat'),
    path('network-analysis/', NetworkAnalysisView.as_view(), name='network_analysis'),
]
