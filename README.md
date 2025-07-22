# Nigerian News Paraphraser & Twitter Bot

This project is a Python automation tool that:
- Scrapes top headlines from a Nigerian news website (Punch).
- Paraphrases the headline and first paragraph using a Hugging Face T5 model.
- Posts the paraphrased content to X (Twitter) with relevant hashtags.
- Logs all posted tweets to a CSV file for tracking and auditing.

---

## Features

- **Web Scraping:** Fetches the latest headlines and first paragraphs from Punch (https://punchng.com/).
- **AI Paraphrasing:** Uses the Hugging Face model `Vamsi/T5_Paraphrase_Paws` to paraphrase news content and append hashtags like `#NigeriaNews`.
- **Twitter Automation:** Posts paraphrased news to X (Twitter) using the official Twitter API v2 via Tweepy.
- **Logging:** Saves each tweet's timestamp, original text, paraphrased text, and tweet URL to `log.csv`.
- **CLI Support:** Specify the number of headlines to process with a command-line argument (`-n`).
- **Extensible:** Modular code structure for easy adaptation to other news sites or social platforms.
- **Error Handling:** Basic error handling and logging for robust operation.

---

## Tech Stack

- **Python 3.10+**
- **Libraries:**
  - `requests` (HTTP requests)
  - `beautifulsoup4` (HTML parsing)
  - `tweepy` (Twitter API v2)
  - `transformers`, `torch`, `sentencepiece`, `tiktoken`, `protobuf` (Hugging Face model support)
  - `csv`, `logging`, `argparse`, `datetime` (standard library)
- **No frameworks or databases required**

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd upwork
```

### 2. Install dependencies

This project uses `pip` for dependency management.  
Install all required packages with:

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Open `main.py` and replace the placeholder values at the top with your actual Twitter API credentials:

```python
TWITTER_API_KEY = "your-key"
TWITTER_API_SECRET = "your-secret"
TWITTER_ACCESS_TOKEN = "your-access-token"
TWITTER_ACCESS_SECRET = "your-access-secret"
```

> **Note:** For production, consider using environment variables or a `.env` file for secrets.

---

## Usage

Run the script from the project directory:

```bash
python main.py -n 3
```

- `-n` or `--num`: Number of headlines to process (default: 3)

**What happens:**
- The script scrapes the latest headlines and first paragraphs from Punch.
- Each is paraphrased and posted to your X (Twitter) account.
- All activity is logged in `log.csv`.

---

## Environment Variables

Currently, API keys are hardcoded in `main.py`.  
For better security, you can refactor to use environment variables:

```python
import os
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')
```

**Example `.env` file:**
```
TWITTER_API_KEY=your-key
TWITTER_API_SECRET=your-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_SECRET=your-access-secret
```

And load with [python-dotenv](https://pypi.org/project/python-dotenv/).

---

## Folder Structure

```
upwork/
│
├── main.py              # Main script: scraping, paraphrasing, tweeting, logging
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── log.csv              # (Generated) Log of posted tweets
├── pyvenv.cfg           # Python virtual environment config
├── bin/, include/, lib/ # Virtual environment folders
```

---

## API Overview

- **No REST API is exposed.**
- The script interacts with:
  - Punch (news scraping)
  - Twitter API v2 (posting tweets)

---

## Docker

*No Dockerfile detected.*  
To dockerize, create a `Dockerfile` with:

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py", "-n", "3"]
```

---

## Contributing

- Code is formatted for clarity and modularity.
- No linting, formatting, or Husky hooks detected.
- PRs and issues welcome!

---

## License

MIT 