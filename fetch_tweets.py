import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from twikit import Client

# Load credentials from .env
load_dotenv()
USERNAME = os.getenv("USERNAME")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

client = Client('en-US')

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

async def main():
    st.set_page_config(page_title="Tech Tweets JSON", layout="wide")
    st.title("📱 Latest Tweets from Tech Accounts (JSON)")

    with st.spinner("Fetching tweets for all accounts..."):
        data = await fetch_all_tweets()

    st.json(data)

if __name__ == "__main__":
    asyncio.run(main())
