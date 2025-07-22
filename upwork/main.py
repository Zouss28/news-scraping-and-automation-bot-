import requests
from bs4 import BeautifulSoup
import tweepy
import csv
import logging
import sys
import argparse
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import os
from requests_oauthlib import OAuth1Session
# ========== CONFIGURATION (Replace with your actual keys/secrets) ==========
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
LOG_FILE = 'log.csv'
NEWS_URL = 'https://punchng.com/'

# ========== LOAD PARAPHRASING MODEL ==========
logging.info('Loading Hugging Face paraphrasing model...')
paraphrase_tokenizer = AutoTokenizer.from_pretrained('Vamsi/T5_Paraphrase_Paws')
paraphrase_model = AutoModelForSeq2SeqLM.from_pretrained('Vamsi/T5_Paraphrase_Paws')
paraphraser = pipeline('text2text-generation', model=paraphrase_model, tokenizer=paraphrase_tokenizer)

# ========== LOGGING SETUP ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== SCRAPE HEADLINES ==========
def scrape_headlines(url, num_headlines=3):
    """
    Scrape top headlines (title + first paragraph) from Punch.
    Returns a list of dicts: [{'title': ..., 'paragraph': ...}, ...]
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        articles = []
        for h2 in soup.find_all('h2', class_='post-title')[:num_headlines]:
            a = h2.find('a')
            if not a or not a['href']:
                continue
            article_url = a['href']
            title = a.get_text(strip=True)
            art_resp = requests.get(article_url, headers=headers, timeout=10)
            art_resp.raise_for_status()
            art_soup = BeautifulSoup(art_resp.text, 'html.parser')
            p = art_soup.find('div', class_='post-content')
            first_p = p.find('p').get_text(strip=True) if p and p.find('p') else ''
            articles.append({'title': title, 'paragraph': first_p, 'url': article_url})
        return articles
    except Exception as e:
        logging.error(f"Error scraping headlines: {e}")
        return []

# ========== PARAPHRASE CONTENT ==========
def paraphrase_content(title, paragraph):
    """
    Use Hugging Face T5 model to paraphrase the news content and add hashtags.
    Returns paraphrased string (max 280 chars).
    """
    # Truncate paragraph to first 300 characters or first sentence
    if len(paragraph) > 300:
        paragraph = paragraph[:300].rsplit('.', 1)[0] + '.'
    prompt = f"paraphrase: {title}. {paragraph} #NigeriaNews"
    try:
        result = paraphraser(prompt, max_length=256, num_return_sequences=1, do_sample=True)[0]['generated_text']
        # Ensure hashtags and length
        if '#NigeriaNews' not in result:
            result += ' #NigeriaNews'
        return result[:280]
    except Exception as e:
        logging.error(f"Error paraphrasing content: {e}")
        return ''

# ========== POST TO TWITTER ==========
def post_to_twitter(text):
    """
    Post paraphrased text to Twitter using Tweepy Client. Returns tweet URL or None.
    """
    try:
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET
        )
        tweet = client.create_tweet(text=text)
        tweet_id = tweet.data.get('id')
        tweet_url = f"https://twitter.com/user/status/{tweet_id}" if tweet_id else None
        return tweet_url
    except Exception as e:
        logging.error(f"Error posting to Twitter: {e}")
        return None

# ========== LOG POST ==========
def log_post(timestamp, original, paraphrased, tweet_url):
    """
    Log the post to a CSV file with timestamp, original, paraphrased, and tweet URL.
    """
    try:
        file_exists = False
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                file_exists = True
        except FileNotFoundError:
            pass
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['timestamp', 'original', 'paraphrased', 'tweet_url'])
            writer.writerow([timestamp, original, paraphrased, tweet_url])
    except Exception as e:
        logging.error(f"Error logging post: {e}")

# ========== MAIN ==========
def main():
    parser = argparse.ArgumentParser(description='Scrape, paraphrase, and tweet Nigerian news headlines.')
    parser.add_argument('-n', '--num', type=int, default=3, help='Number of headlines to process (default: 3)')
    args = parser.parse_args()

    headlines = scrape_headlines(NEWS_URL)
    if not headlines:
        logging.error('No headlines found. Exiting.')
        sys.exit(1)

    for item in headlines:
        original = f"{item['title']}\n{item['paragraph']}"
        paraphrased = paraphrase_content(item['title'], item['paragraph'])
        if not paraphrased:
            continue
        tweet_url = post_to_twitter(paraphrased)
        timestamp = datetime.now().isoformat()
        log_post(timestamp, original, paraphrased, tweet_url or '')
        logging.info(f"Tweeted: {paraphrased}\nURL: {tweet_url}")

if __name__ == '__main__':
    main() 