from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def generate_explanation(threat_level, scan_results):
    """
    Uses LangChain and Groq to explain a threat result to the user.
    """
    if not getattr(settings, 'GROQ_API_KEY', None):
        return f"The file was marked as {threat_level}. The static analyzer found {len(scan_results.get('static', {}).get('suspicious_sections', []))} suspicious sections. Please do not execute this file."
    
    try:
        llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0.2,
            groq_api_key=settings.GROQ_API_KEY
        )
        
        template = """
        You are an expert cybersecurity analyst. A user scanned a file and we need a plain-english explanation.
        Overall Threat Level: {threat_level}
        Scan Results (JSON): {scan_results}
        
        Provide the following:
        1. Explain the threat to a non-technical user in 2 short paragraphs based on the scan results. Focus on the file entropy, specific suspicious sections, or YARA matches if present.
        2. Provide 2 strict, bulleted remediation steps the user should take.
        """
        
        prompt = PromptTemplate.from_template(template)
        response = llm.invoke(prompt.format(threat_level=threat_level, scan_results=scan_results))
        
        return response.content
    except Exception as e:
        logger.error(f"Error generating LLM explanation: {e}")
        return f"The file was marked as {threat_level}. An error occurred generating the detailed AI explanation."
