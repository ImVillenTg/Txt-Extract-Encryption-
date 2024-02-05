import os

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

BOT_TOKEN = os.environ.get("BOT_TOKEN", "6578803085:AAEVvQbNeB-AT03hidM0jdWZEDVfjQby5XE")
API_ID = int(os.environ.get("API_ID", "22029683"))
API_HASH = os.environ.get("API_HASH", "bac50459b37341db660944b55ae360eb")
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "5501543173").split())
ADMINS = [int(chat) for chat in os.getenv("ADMINS", "5501543173,5889270631").split(",") if chat != ""]
GROUPS = [int(chat) for chat in os.getenv("GROUPS", "-1002043823399").split(",") if chat != ""]

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
