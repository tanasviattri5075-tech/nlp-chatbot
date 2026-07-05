# NLPBot — AI Chatbot with NLP

A rule-based/intent-matching chatbot that understands user intent using classic
NLP (tokenization, lemmatization, TF-IDF + cosine similarity) and responds with
contextual replies through a Flask web app.

Tech stack: **Python, NLTK, scikit-learn, Flask, HTML/CSS/JS**

## How it works

1. `intents.json` defines a set of **tags** (e.g. `greeting`, `joke`, `help`),
   each with example **patterns** (things a user might type) and **responses**.
2. On startup, `chatbot.py` preprocesses every pattern (lowercase → remove
   punctuation → tokenize → remove stopwords → lemmatize) and fits a
   **TF-IDF vectorizer** over all of them.
3. When a user sends a message, it's preprocessed the same way and compared
   against every known pattern using **cosine similarity**.
4. The best-matching pattern's tag is used to pick a random response. If the
   best match score is below a confidence threshold, the bot falls back to a
   generic "I didn't understand that" reply.
5. Flask (`app.py`) exposes this over a `/chat` endpoint, and a simple chat UI
   (`templates/index.html`, `static/`) talks to it over `fetch()`.

## Setup

```bash
# 1. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

The first run will auto-download the small NLTK data packages it needs
(`punkt`, `wordnet`, `stopwords`) — this requires an internet connection once.

## Testing the NLP logic on its own (no web server)

```bash
python chatbot.py
```

This drops you into a command-line chat loop, useful for quickly iterating on
`intents.json` without touching the web layer.

## Customizing it

This demo ships with generic intents (greetings, jokes, thanks, etc).
To turn it into something useful for a specific domain (e.g. a college
FAQ bot, a product support bot):

1. Open `intents.json`.
2. Add a new object to the `intents` list with a `tag`, a list of `patterns`
   (5–10 varied example phrases people might use), and a list of `responses`.
3. Restart the app — the vectorizer refits automatically from the updated file.

Tip: more, varied patterns per intent = better matching. If two intents keep
getting confused with each other, add more distinguishing patterns to each.

## Possible extensions (good next steps for a portfolio project)

- Swap the TF-IDF matcher for a proper intent-classification model
  (e.g. a small `sklearn` `LogisticRegression`/`SVC` trained on the patterns).
- Add conversation memory (track previous intent to handle follow-ups).
- Add spaCy NER to extract entities (names, dates, products) from messages.
- Deploy it (Render, Railway, PythonAnywhere) so you have a live demo link
  for your resume/portfolio.

## Project structure

```
nlp_chatbot/
├── app.py              # Flask server & /chat API route
├── chatbot.py          # NLP pipeline (preprocessing + intent matching)
├── intents.json        # Training data: patterns & responses per intent
├── requirements.txt
├── templates/
│   └── index.html      # Chat UI markup
└── static/
    ├── style.css        # Chat UI styling
    └── script.js        # Chat UI client logic (fetch → /chat)
```
