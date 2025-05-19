import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from twikit import Client

# Load credentials from .env
load_dotenv()
USERNAME = os.getenv("USERNAME")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

client = Client('en-US')
app = FastAPI()

ACCOUNTS = [
    'thenextweb',
    'TechCrunch',
    'TechRepublic',
    'engadget',
    'arstechnica',
    'WIRED',
    'gigaom',
    'mashable'
]

async def get_latest_tweets_from_user(username, limit=10):
    user = await client.get_user_by_screen_name(username)
    tweets = await client.get_user_tweets(user.id, "tweets", limit)
    return [{"created_at": str(tweet.created_at), "text": tweet.full_text} for tweet in tweets]

async def authenticate():
    if os.path.exists('cookies.json'):
        client.load_cookies('cookies.json')
    else:
        await client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD
        )
        client.save_cookies('cookies.json')

async def fetch_all_tweets():
    await authenticate()
    all_tweets = {}
    for account in ACCOUNTS:
        try:
            tweets = await get_latest_tweets_from_user(account)
            all_tweets[account] = tweets
        except Exception as e:
            all_tweets[account] = {"error": str(e)}
    return all_tweets

@app.get("/")
async def root():
    data = await fetch_all_tweets()
    return JSONResponse(content=data)
