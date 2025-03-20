import time
import re
import sqlite3
from nltk.tokenize import word_tokenize, sent_tokenize
from openai import OpenAI
import requests
from textblob import TextBlob
import httpx
import nltk

class AgentOversight:
    """A class to oversee AI agent outputs with validation, guidance, and metrics."""

    def __init__(self, openai_api_key=None, deepseek_api_key=None, grok_api_key=None, proxy=None):
        """Initialize with optional API keys and proxy for supported models."""
        self.metrics = {"response_time": [], "accuracy": []}
        self.rules = {}
        # Ensure NLTK punkt is downloaded
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        if openai_api_key:
            http_client = httpx.Client() if not proxy else httpx.Client(proxies={"http://": proxy, "https://": proxy})
            self.openai_client = OpenAI(api_key=openai_api_key, http_client=http_client)
        else:
            self.openai_client = None
        self.deepseek_api_key = deepseek_api_key
        self.grok_api_key = grok_api_key
        self._db_initialized = False

    def _init_db(self):
        """Initialize SQLite database for metrics logging if not already done."""
        if not self._db_initialized:
            conn = sqlite3.connect("oversight.db")
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS metrics
                        (id INTEGER PRIMARY KEY, response_time REAL, accuracy REAL, timestamp TEXT)''')
            conn.commit()
            conn.close()
            self._db_initialized = True

    def _log_metrics(self, response_time, accuracy):
        """Log metrics to SQLite database."""
        self._init_db()  # Ensure database is ready
        conn = sqlite3.connect("oversight.db")
        c = conn.cursor()
        c.execute("INSERT INTO metrics (response_time, accuracy, timestamp) VALUES (?, ?, datetime('now'))",
                  (response_time, accuracy))
        conn.commit()
        conn.close()

    def set_rules(self, rules_input):
        """Parse and set user-defined rules from a comma-separated string."""
        self.rules.clear()
        if not rules_input:
            return
        for rule in rules_input.split(","):
            try:
                key, value = rule.split("=")
                self.rules[key.strip()] = value.strip()
            except ValueError:
                continue

    def get_model_output(self, model_name, input_text):
        """Fetch output from the specified AI model."""
        start_time = time.time()
        if model_name == "openai" and self.openai_client:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": input_text}],
                temperature=0.2,
                max_tokens=200
            )
            output = response.choices[0].message.content
        elif model_name == "deepseek" and self.deepseek_api_key:
            headers = {"Authorization": f"Bearer {self.deepseek_api_key}"}
            payload = {
                "model": "deepseek-r1",
                "messages": [{"role": "user", "content": input_text}],
                "temperature": 0.2,
                "max_tokens": 200
            }
            response = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers)
            output = response.json()["choices"][0]["message"]["content"]
        elif model_name == "grok" and self.grok_api_key:
            headers = {"Authorization": f"Bearer {self.grok_api_key}"}
            payload = {
                "model": "grok-3",
                "prompt": input_text,
                "temperature": 0.2,
                "max_tokens": 200
            }
            response = requests.post("https://api.xai.com/grok", json=payload, headers=headers)  # Placeholder endpoint
            output = response.json()["response"]
        else:
            raise ValueError(f"Unsupported model: {model_name} or missing API key")
        return output, start_time

    def validate_output(self, output):
        """Validate output against user-defined rules."""
        if not self.rules:
            return True, "No rules defined."

        results = []
        words = word_tokenize(output)
        sentences = sent_tokenize(output)
        word_count = len(words)
        char_count = len(output)
        unique_words = len(set(words))

        # Text Length Rules
        if "max_words" in self.rules:
            max_words = int(self.rules["max_words"])
            valid = word_count <= max_words
            results.append(f"Word count: {word_count} (max: {max_words}) - {'Valid' if valid else 'Invalid'}")
        if "min_words" in self.rules:
            min_words = int(self.rules["min_words"])
            valid = word_count >= min_words
            results.append(f"Word count: {word_count} (min: {min_words}) - {'Valid' if valid else 'Invalid'}")
        if "max_chars" in self.rules:
            max_chars = int(self.rules["max_chars"])
            valid = char_count <= max_chars
            results.append(f"Char count: {char_count} (max: {max_chars}) - {'Valid' if valid else 'Invalid'}")
        if "min_chars" in self.rules:
            min_chars = int(self.rules["min_chars"])
            valid = char_count >= min_chars
            results.append(f"Char count: {char_count} (min: {min_chars}) - {'Valid' if valid else 'Invalid'}")
        if "max_sentences" in self.rules:
            max_sentences = int(self.rules["max_sentences"])
            valid = len(sentences) <= max_sentences
            results.append(f"Sentence count: {len(sentences)} (max: {max_sentences}) - {'Valid' if valid else 'Invalid'}")
        if "min_sentences" in self.rules:
            min_sentences = int(self.rules["min_sentences"])
            valid = len(sentences) >= min_sentences
            results.append(f"Sentence count: {len(sentences)} (min: {min_sentences}) - {'Valid' if valid else 'Invalid'}")

        # Content Rules
        if "must_contain" in self.rules:
            keyword = self.rules["must_contain"]
            valid = keyword.lower() in output.lower()
            results.append(f"Contains '{keyword}': {'Yes' if valid else 'No'}")
        if "must_not_contain" in self.rules:
            keyword = self.rules["must_not_contain"]
            valid = keyword.lower() not in output.lower()
            results.append(f"Does not contain '{keyword}': {'Yes' if valid else 'No'}")
        if "exact_match" in self.rules:
            exact_text = self.rules["exact_match"]
            valid = output.strip() == exact_text.strip()
            results.append(f"Exact match '{exact_text}': {'Yes' if valid else 'No'}")
        if "starts_with" in self.rules:
            prefix = self.rules["starts_with"]
            valid = output.strip().startswith(prefix)
            results.append(f"Starts with '{prefix}': {'Yes' if valid else 'No'}")
        if "ends_with" in self.rules:
            suffix = self.rules["ends_with"]
            valid = output.strip().endswith(suffix)
            results.append(f"Ends with '{suffix}': {'Yes' if valid else 'No'}")

        # Structural Rules
        if "has_punctuation" in self.rules:
            expected = self.rules["has_punctuation"].lower() == "yes"
            valid = any(c in output for c in ".,!?") == expected
            results.append(f"Has punctuation: {'Yes' if valid else 'No'}")
        if "has_numbers" in self.rules:
            expected = self.rules["has_numbers"].lower() == "yes"
            valid = bool(re.search(r'\d', output)) == expected
            results.append(f"Has numbers: {'Yes' if valid else 'No'}")
        if "max_unique_words" in self.rules:
            max_unique = int(self.rules["max_unique_words"])
            valid = unique_words <= max_unique
            results.append(f"Unique words: {unique_words} (max: {max_unique}) - {'Valid' if valid else 'Invalid'}")
        if "min_unique_words" in self.rules:
            min_unique = int(self.rules["min_unique_words"])
            valid = unique_words >= min_unique
            results.append(f"Unique words: {unique_words} (min: {min_unique}) - {'Valid' if valid else 'Invalid'}")

        # Advanced Rules (OpenAI or TextBlob)
        if self.openai_client:
            if "is_coherent" in self.rules and self.rules["is_coherent"] == "yes":
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Evaluate coherence based on grammar, flow, and clarity. Respond with 'Yes' or 'No' and a one-sentence explanation."},
                        {"role": "user", "content": f"Text: '{output}'"}
                    ],
                    temperature=0.2,
                    max_tokens=50,

                )
                result = response.choices[0].message.content
                valid = "Yes" in result
                if word_count < 2 and valid:
                    result = "No - Text is too short to be coherent."
                    valid = False
                results.append(f"Coherence: {result}")
            if "tone" in self.rules:
                expected_tone = self.rules["tone"].lower()
                blob = TextBlob(output)
                polarity = blob.sentiment.polarity
                tone = "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"
                valid = tone == expected_tone
                results.append(f"Tone: {tone} (expected: {expected_tone}) - {'Valid' if valid else 'Invalid'}")
            if "is_factual" in self.rules and self.rules["is_factual"] == "yes":
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Check if this text is factually plausible. Respond with 'Yes' or 'No' and a brief explanation."},
                        {"role": "user", "content": f"Text: '{output}'"}
                    ],
                    temperature=0.2,
                    max_tokens=50
                )
                result = response.choices[0].message.content
                valid = "Yes" in result
                results.append(f"Factual: {result}")
            if "readability" in self.rules:
                expected_level = self.rules["readability"].lower()
                blob = TextBlob(output)
                score = 206.835 - 1.015 * (word_count / len(sentences)) - 84.6 * (sum(len(w) for w in words) / word_count)
                level = "easy" if score > 60 else "medium" if score > 30 else "hard"
                valid = level == expected_level
                results.append(f"Readability: {level} (expected: {expected_level}) - {'Valid' if valid else 'Invalid'}")

        overall_valid = all("Invalid" not in r and "No" not in r for r in results)
        return overall_valid, " | ".join(results)

    def provide_guidance(self, output):
        """Generate suggestions based on rule violations or improvement requests."""
        if not self.rules:
            return "No rules to guide against."

        words = len(word_tokenize(output))
        sentences = len(sent_tokenize(output))
        guidance = []

        # Text Length Guidance
        if "max_words" in self.rules and words > int(self.rules["max_words"]):
            guidance.append("Shorten the response.")
        if "min_words" in self.rules and words < int(self.rules["min_words"]):
            guidance.append("Add more details.")
        if "max_chars" in self.rules and len(output) > int(self.rules["max_chars"]):
            guidance.append("Reduce character count.")
        if "min_chars" in self.rules and len(output) < int(self.rules["min_chars"]):
            guidance.append("Increase character count.")
        if "max_sentences" in self.rules and sentences > int(self.rules["max_sentences"]):
            guidance.append("Fewer sentences needed.")
        if "min_sentences" in self.rules and sentences < int(self.rules["min_sentences"]):
            guidance.append("Add more sentences.")

        # Content Guidance
        if "must_contain" in self.rules and self.rules["must_contain"].lower() not in output.lower():
            guidance.append(f"Include '{self.rules['must_contain']}'.")
        if "must_not_contain" in self.rules and self.rules["must_not_contain"].lower() in output.lower():
            guidance.append(f"Remove '{self.rules['must_not_contain']}'.")
        if "exact_match" in self.rules and output.strip() != self.rules["exact_match"].strip():
            guidance.append(f"Match '{self.rules['exact_match']}' exactly.")
        if "starts_with" in self.rules and not output.strip().startswith(self.rules["starts_with"]):
            guidance.append(f"Start with '{self.rules['starts_with']}'.")
        if "ends_with" in self.rules and not output.strip().endswith(self.rules["ends_with"]):
            guidance.append(f"End with '{self.rules['ends_with']}'.")

        # Structural Guidance
        if "has_punctuation" in self.rules and self.rules["has_punctuation"] == "yes" and not any(c in output for c in ".,!?"):
            guidance.append("Add punctuation.")
        if "has_numbers" in self.rules and self.rules["has_numbers"] == "yes" and not re.search(r'\d', output):
            guidance.append("Include numbers.")

        # Advanced Guidance (OpenAI)
        if self.openai_client and "improve" in self.rules and self.rules["improve"] == "yes":
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Suggest one specific, concise improvement based on clarity or relevance."},
                    {"role": "user", "content": f"Text: '{output}'"}
                ],
                temperature=0.2,
                max_tokens=30
            )
            guidance.append(response.choices[0].message.content)

        return " ".join(guidance) if guidance else "Looks good!"

    def track_metrics(self, output, start_time):
        """Track performance metrics based on output and response time."""
        response_time = time.time() - start_time
        self.metrics["response_time"].append(response_time)
        is_valid, _ = self.validate_output(output)
        accuracy = 1.0 if is_valid else 0.8
        if "max_response_time" in self.rules:
            max_time = float(self.rules["max_response_time"])
            if response_time > max_time:
                accuracy = min(accuracy, 0.5)
        self.metrics["accuracy"].append(accuracy)
        self._log_metrics(response_time, accuracy)  # Log automatically
        return {"response_time": response_time, "accuracy": accuracy}

    def process_input(self, model_name, input_text, auto_correct=False, max_retries=1):
        """Process input through the model with optional auto-correction."""
        output, start_time = self.get_model_output(model_name, input_text)
        is_valid, validation_result = self.validate_output(output)
        guidance = self.provide_guidance(output)
        metrics = self.track_metrics(output, start_time)
        retries = 0

        while (auto_correct and guidance != "Looks good!" and retries < max_retries and 
               model_name in ["openai", "deepseek", "grok"]):
            corrected_input = f"{input_text}\n\nRevise based on this feedback: {guidance}"
            output, new_start_time = self.get_model_output(model_name, corrected_input)
            is_valid, validation_result = self.validate_output(output)
            guidance = self.provide_guidance(output)
            metrics = self.track_metrics(output, new_start_time)
            retries += 1

        return {
            "output": output,
            "validation": validation_result,
            "guidance": guidance,
            "metrics": metrics,
            "retries": retries
        }