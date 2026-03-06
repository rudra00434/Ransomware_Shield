from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

class AIChatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get('message', '')
        if not user_message:
            return Response({'error': 'Message required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not getattr(settings, 'GROQ_API_KEY', None):
            return Response({
                'reply': "AI Assistant is currently offline. Please configure the GROQ_API_KEY in the backend.",
                'suggestions': []
            })
            
        try:
            llm = ChatGroq(
                model_name="llama-3.1-8b-instant",
                temperature=0.5,
                groq_api_key=settings.GROQ_API_KEY
            )
            
            template = """
            You are 'Ransomware Shield Analyst', an expert cybersecurity AI assistant.
            You help users understand malware, ransomware, cybersecurity best practices, and analyze their scan results.
            Keep your answers concise, professional, and easy to understand for IT professionals.
            
            User message: {message}
            
            Provide a helpful response.
            """
            
            prompt = PromptTemplate.from_template(template)
            response = llm.invoke(prompt.format(message=user_message))
            
            return Response({
                'reply': response.content,
                'suggestions': [
                    "What is ransomware?",
                    "How to secure an active directory?",
                    "Explain file entropy."
                ]
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NetworkAnalysisView(APIView):
    permission_classes = [AllowAny] # Or IsAuthenticated based on requirements

    def post(self, request):
        network_data = request.data.get('data', '')
        if not network_data:
            return Response({'error': 'Network data required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not getattr(settings, 'GROQ_API_KEY', None):
            return Response({
                'reply': "Network Analysis is currently offline. Please configure the GROQ_API_KEY in the backend.",
            })
            
        try:
            llm = ChatGroq(
                model_name="llama-3.1-8b-instant",
                temperature=0.3,
                groq_api_key=settings.GROQ_API_KEY
            )
            
            template = """
            You are 'Ransomware Shield Network Analyst', an expert network security AI assistant.
            You help users analyze network logs, IP addresses, packet streams, or structural anomalies for potential security threats.
            Keep your answers concise, professional, and highlight any indicators of compromise (IoCs) or suspicious patterns.
            
            Network Data provided by user:
            {network_data}
            
            Provide a detailed security analysis of the provided network data. Point out potential vulnerabilities, attacks (like DDoS, port scanning, ransomware C2 communication), and recommend mitigation steps.
            """
            
            prompt = PromptTemplate.from_template(template)
            response = llm.invoke(prompt.format(network_data=network_data))
            
            return Response({
                'analysis': response.content,
            })
        except Exception as e:
            logger.error(f"Error in Network Analysis: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
