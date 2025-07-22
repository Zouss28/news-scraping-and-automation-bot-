# Nigerian News to Twitter Bot

This Python script scrapes top headlines from a Nigerian news website (default: Punch), paraphrases them using OpenAI/ChatGPT, and posts them to X (Twitter) with hashtags like #NigeriaNews. All posted tweets are logged to a CSV file.

## Features
- Scrapes top headlines (title + first paragraph) from Punch
- Paraphrases content using OpenAI API with hashtags
- Posts paraphrased content to X (Twitter) using Tweepy
- Logs posted tweets to `log.csv` (timestamp, original, paraphrased, tweet URL)
- CLI argument for number of headlines (default: 3)
- Modular, clean code for easy extension

## Setup
1. **Clone the repo and navigate to the project directory:**
   ```bash
   cd upwork
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API keys:**
   - Open `main.py` and replace the placeholders at the top with your actual OpenAI and Twitter API credentials.

## Usage
Run the script from the project directory:
```bash
python main.py -n 5
```
- `-n` or `--num`: Number of headlines to process (default: 3)

## Output
- Tweets are posted to your X (Twitter) account.
- Each post is logged in `log.csv` with timestamp, original text, paraphrased text, and tweet URL.

## Notes
- The script is designed for easy extension to other news sites.
- All API keys are required for full functionality.
- Paraphrased tweets are limited to 280 characters.

## License
MIT 