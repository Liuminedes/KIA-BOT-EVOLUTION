import os
from dotenv import load_dotenv
load_dotenv()

EVOLUTION_URL      = os.getenv("EVOLUTION_URL")
EVOLUTION_API_KEY  = os.getenv("EVOLUTION_API_KEY")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "kia-bot")
BRYAN_NUMBER       = os.getenv("BRYAN_NUMBER", "573007271627")
REDIS_URL          = os.getenv("REDIS_URL", "redis://localhost:6379")