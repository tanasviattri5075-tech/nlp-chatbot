"""
Core NLP logic for the chatbot.

Approach:
1. Load intents (patterns + responses) from intents.json
2. Preprocess text: tokenize, lowercase, remove punctuation/stopwords, lemmatize
3. Vectorize all known patterns with TF-IDF
4. For a new user message, vectorize it the same way and compare with
   cosine similarity against every known pattern
5. If the best match score is above a confidence threshold, reply with a
   random response from that intent's tag. Otherwise, use the fallback intent.
"""

import json
import random
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Make sure required NLTK data is available (no-op if already downloaded)
for pkg in ["punkt", "punkt_tab", "wordnet", "omw-1.4", "stopwords"]:
    try:
        nltk.data.find(pkg)
    except LookupError:
        nltk.download(pkg, quiet=True)

lemmatizer = WordNetLemmatizer()
try:
    STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    STOPWORDS = set(stopwords.words("english"))


def preprocess(text: str) -> str:
    """Lowercase, strip punctuation, tokenize, remove stopwords, lemmatize."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(tok) for tok in tokens if tok not in STOPWORDS]
    return " ".join(tokens)


class Chatbot:
    def __init__(self, intents_path: str = "intents.json", confidence_threshold: float = 0.25):
        with open(intents_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.intents = data["intents"]
        self.confidence_threshold = confidence_threshold

        # Flatten (pattern -> tag) pairs, skipping the fallback intent (no patterns)
        self.patterns = []
        self.pattern_tags = []
        for intent in self.intents:
            for pattern in intent["patterns"]:
                self.patterns.append(preprocess(pattern))
                self.pattern_tags.append(intent["tag"])

        self.responses_by_tag = {intent["tag"]: intent["responses"] for intent in self.intents}

        # Fit TF-IDF over all known patterns
        self.vectorizer = TfidfVectorizer()
        self.pattern_matrix = self.vectorizer.fit_transform(self.patterns)

    def get_response(self, user_input: str, with_meta: bool = False):
        """Return the bot's reply. If with_meta=True, also return the
        matched intent tag and confidence score (useful for showing the
        NLP pipeline's reasoning in a UI)."""
        cleaned = preprocess(user_input)
        if not cleaned.strip():
            reply = random.choice(self.responses_by_tag["fallback"])
            return (reply, "fallback", 0.0) if with_meta else reply

        user_vec = self.vectorizer.transform([cleaned])
        similarities = cosine_similarity(user_vec, self.pattern_matrix)[0]

        best_idx = similarities.argmax()
        best_score = float(similarities[best_idx])

        if best_score < self.confidence_threshold:
            tag = "fallback"
        else:
            tag = self.pattern_tags[best_idx]

        reply = random.choice(self.responses_by_tag[tag])
        return (reply, tag, best_score) if with_meta else reply


if __name__ == "__main__":
    # Quick command-line test loop
    bot = Chatbot()
    print("NLPBot is ready! Type 'quit' to exit.")
    while True:
        msg = input("You: ")
        if msg.lower() in ("quit", "exit"):
            break
        print("Bot:", bot.get_response(msg))
