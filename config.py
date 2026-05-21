import os
from dotenv import load_dotenv

load_dotenv()

class DefaultConfig:
    """Extended configuration to support Azure AI Language Service
    Added for sentiment analysis integration (MS631 Project)
    """
    PORT = 3978
    APP_ID = ""
    APP_PASSWORD = ""

    API_KEY = os.environ.get("MicrosoftAPIKey")
    ENDPOINT_URI = os.environ.get("MicrosoftAIServiceEndpoint")
