from openai import OpenAI
import sptipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

api_ky = os.environ["OPENAI_API_KEY"]
client_id = os.environ.get("SP_CLI_KEY") 
client_secret = os.environ.get("SP_SCR_KEY")

client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

client = OpenAI(api_key=api_ky)

print("hello")

