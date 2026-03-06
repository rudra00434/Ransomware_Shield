import json
import asyncio
import psutil
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

logger = logging.getLogger(__name__)

class NetworkAnalysisConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        # Accept the connection anyway for now based on views.py using AllowAny
        await self.accept()
        self.is_monitoring = False
        self.monitor_task = None
        
        # Initialize Groq if available
        self.llm = None
        if getattr(settings, 'GROQ_API_KEY', None):
            try:
                self.llm = ChatGroq(
                    model_name="llama-3.1-8b-instant",
                    temperature=0.3,
                    groq_api_key=settings.GROQ_API_KEY
                )
                self.prompt_template = PromptTemplate.from_template(
                    """
                    You are 'Ransomware Shield Live Network Analyst', an expert network security AI assistant.
                    You are monitoring a live feed of active network connections from the host machine.
                    
                    Current Active Connections (Snapshot):
                    {network_data}
                    
                    Provide a fast, concise security analysis of this live data. 
                     - Highlight any unrecognized, suspicious, or known malicious ports/IPs.
                     - Point out excessive connections from single processes if any.
                     - If everything looks normal, state that clearly but remain vigilant.
                     Keep it brief (max 3-4 sentences) as this is a real-time updating dashboard.
                    """
                )
            except Exception as e:
                logger.error(f"Failed to init Groq in Consumer: {e}")

    async def disconnect(self, close_code):
        self.is_monitoring = False
        if self.monitor_task:
            self.monitor_task.cancel()

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('command')

        if command == 'start':
            if not self.is_monitoring:
                self.is_monitoring = True
                self.monitor_task = asyncio.create_task(self.monitor_loop())
                await self.send(text_data=json.dumps({"status": "monitoring_started"}))
        
        elif command == 'stop':
            self.is_monitoring = False
            if self.monitor_task:
                self.monitor_task.cancel()
            await self.send(text_data=json.dumps({"status": "monitoring_stopped"}))

    async def monitor_loop(self):
        while self.is_monitoring:
            try:
                connections = self.get_active_connections()
                
                # Send raw data immediately to frontend for the scrolling list
                await self.send(text_data=json.dumps({
                    'type': 'network_data',
                    'connections': connections
                }))

                # Check for Man-in-the-Middle (ARP Spoofing)
                mitm_alert = await self.check_arp_spoofing()
                if mitm_alert:
                    await self.send(text_data=json.dumps({
                        'type': 'mitm_alert',
                        'alert': mitm_alert
                    }))
                
                # Ask AI to analyze it (but don't block the loop completely if it's slow)
                if self.llm and len(connections) > 0:
                    analysis = await self.analyze_with_ai(connections)
                    if analysis:
                        await self.send(text_data=json.dumps({
                            'type': 'ai_analysis',
                            'analysis': analysis
                        }))
                
                # Wait 5 seconds before the next snapshot to avoid API rate limits
                await asyncio.sleep(5)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                await self.send(text_data=json.dumps({'error': str(e)}))
                await asyncio.sleep(5) # Still sleep on error to prevent tight loops

    def get_active_connections(self):
        # Synchronous function, but fast enough it shouldn't block the event loop noticeably 
        # for a small number of connections
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED' or conn.status == 'LISTEN':
                    connections.append({
                        'fd': conn.fd,
                        'family': conn.family.name if hasattr(conn.family, 'name') else str(conn.family),
                        'type': conn.type.name if hasattr(conn.type, 'name') else str(conn.type),
                        'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                        'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                        'status': conn.status,
                        'pid': conn.pid
                    })
        except Exception as e:
            logger.error(f"psutil error: {e}")
            
        # Limit to top 20 to avoid sending massive payloads to Groq
        return connections[:20]

    async def check_arp_spoofing(self):
        import subprocess
        import re
        
        try:
            # Run arp -a non-blocking
            result = await asyncio.to_thread(
                subprocess.run, ['arp', '-a'], capture_output=True, text=True
            )
            output = result.stdout
            
            # Use regex to find IP and MAC addresses in the Windows arp format
            # Format usually looks like: 192.168.1.1       00-11-22-33-44-55     dynamic
            arp_entries = re.findall(r'([0-9\.]+)\s+([0-9a-f\-]{17})\s+', output, re.IGNORECASE)
            
            mac_to_ips = {}
            for ip, mac in arp_entries:
                mac = mac.lower()
                # Ignore broadcast/multicast MACs which naturally map to many IPs
                if mac == 'ff-ff-ff-ff-ff-ff' or mac.startswith('01-00-5e'):
                    continue
                    
                if mac not in mac_to_ips:
                    mac_to_ips[mac] = set()
                mac_to_ips[mac].add(ip)
            
            # Check for duplicates
            for mac, ips in mac_to_ips.items():
                if len(ips) > 1:
                    logger.warning(f"ARP SPOOFING DETECTED: MAC {mac} is associating with multiple IPs: {ips}")
                    return {
                        'title': 'Man-in-the-Middle Attack Detected (ARP Spoofing)',
                        'description': f"A single physical device (MAC: {mac}) is claiming to be multiple IP addresses on your network: {', '.join(ips)}. This strongly indicates an active interception attack.",
                        'severity': 'CRITICAL',
                        'mac': mac,
                        'ips': list(ips)
                    }
                    
            return None
            
        except Exception as e:
            logger.error(f"Error checking ARP table: {e}")
            return None

    async def analyze_with_ai(self, connections):
        try:
            # Convert to a readable string format for the prompt
            conn_str = json.dumps(connections, indent=2)
            
            # Using asyncio.to_thread because llm.invoke is synchronous and blocks the websocket
            response = await asyncio.to_thread(
                self.llm.invoke, 
                self.prompt_template.format(network_data=conn_str)
            )
            return response.content
        except Exception as e:
            logger.error(f"Groq API error in consumer: {e}")
            return "Analysis temporarily unavailable due to API error."
