import os
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging
from uuid import uuid4
from datetime import datetime, timezone

# Configuración del logger para Application Insights
logger = logging.getLogger("app_insights")
logger.setLevel(logging.INFO)

# Leer el string de conexión desde variable de entorno
AI_CONNECTION_STRING = os.getenv("APPINSIGHTS_CONNECTION_STRING", "InstrumentationKey=YOUR_INSTRUMENTATION_KEY;IngestionEndpoint=https://region.in.applicationinsights.azure.com/;LiveEndpoint=https://region.livediagnostics.monitor.azure.com/;ApplicationId=YOUR_APPLICATION_ID")

if not any(isinstance(h, AzureLogHandler) for h in logger.handlers):
    logger.addHandler(AzureLogHandler(connection_string=AI_CONNECTION_STRING))

def log_event(event_type, payload, session_id, interaction_id, agent_name="AWS_Agent"):
    event = {
        "AgentName": agent_name,
        "Timestamp": datetime.now(timezone.utc).isoformat(),
        "EventType": event_type,
        "Payload": payload,
        "SessionID": session_id,
        "InteractionID": interaction_id
    }
    logger.info(event)
