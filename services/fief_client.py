"""
Fief authentication client service.
This file contains configuration for Fief authentication service.
"""

import os
from fief_client import FiefAsync, FiefAccessTokenInfo
from fief_client.integrations.fastapi import FiefAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fief client configuration
fief_client = FiefAsync(
    base_url=os.getenv("FIEF_BASE_URL"),
    client_id=os.getenv("FIEF_CLIENT_ID"),
    client_secret=os.getenv("FIEF_CLIENT_SECRET"),
)

# FastAPI integration
auth = FiefAuth(fief_client, auth_redirect_uri=os.getenv("AUTH_REDIRECT_URI"))
