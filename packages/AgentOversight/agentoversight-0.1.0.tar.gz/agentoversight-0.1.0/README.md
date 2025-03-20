# AgentOversight

A modular tool to monitor, validate, and guide agentic AI performance.

AgentOversight is a Python-based platform designed to oversee AI agents. It allows users to define custom validation rules, receive directional guidance, and track performance metrics—all through a web interface or programmatically. Supporting multiple models like OpenAI, DeepSeek, and Grok, it’s perfect for developers and researchers ensuring AI reliability.

## Why AgentOversight

- **Consistency**: Agents might interpret rules differently across runs, leading to inconsistent validation (e.g., word counting could vary slightly).

- **Latency**: Sending requests to an external AI (via API) adds network delay compared to local computation.

- **Cost** : If using a paid API (e.g., OpenAI), each validation request costs money, whereas local code is free.

- **Control**: You’re dependent on the agent’s capabilities and can’t easily tweak the validation logic without changing the prompt, which might not scale for a UI-driven tool.

- **Metrics**: Tracking performance (e.g., response time) becomes trickier if the agent handles everything remotely.

```

The AgentOversight class exists as a dedicated local component for these reasons:
Independence: It decouples validation, guidance, and metrics from any specific AI agent, making the hub a standalone tool that can oversee any agent’s output (e.g., Grok, ChatGPT, or a custom model). You don’t need an AI to use it—just the output text.

Performance: Local processing is faster and doesn’t rely on external API calls, which is critical for real-time monitoring in a web app.

Customizability: You control the logic. Want to add a new rule type (e.g., max_sentences)? Just update the class—no need to rewrite prompts or rely on an agent understanding it.

Transparency: The rules and results are deterministic and visible in code, not hidden in an AI’s black-box reasoning.

Metrics Tracking: It’s easier to log and analyze metrics (e.g., response time, accuracy trends) locally with a database than to extract them from agent responses.

Why Not Just Prompt?
The hub’s goal is to oversee agents, not replace their work. If the agent itself validates its output, you lose the independent “second opinion” that an oversight tool provides.

Users might want to apply consistent rules across multiple agents or outputs without crafting prompts each time—AgentOversight makes this reusable and UI-driven.

```

## Features

- **Custom Validation**: Define rules (e.g., `max_words=50`) to validate agent outputs.
- **Directional Guidance**: Get actionable suggestions (e.g., "Shorten the response").
- **Performance Metrics**: Track response time and accuracy, logged automatically to SQLite (`oversight.db`).
- **Multi-Model Support**: Test outputs from OpenAI, DeepSeek, Grok, and more.
- **Auto-Correction**: Optionally refine outputs based on guidance with a configurable retry limit.
- **Web Interface**: Built with Flask for easy interaction and visualization.

## Installation Methods

### Via pip

```bash
pip install agent-oversight
```

### From Source

Clone the repository:

```bash
git clone https://github.com/LogeswaranA/AgentOversight.git
cd AgentOversight
```

Set up a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Web Interface

Run the Flask app:

```bash
agent-oversight
```

Open your browser to [http://127.0.0.1:5000](http://127.0.0.1:5000). Metrics are automatically logged to `oversight.db` in your working directory.

### Programmatic Example

```python
from AgentOversight.agent_logic import AgentOversight

# Initialize with optional API keys
oversight = AgentOversight(openai_api_key="your-openai-key")
oversight.set_rules("max_words=10,must_contain=test")

# Process input with auto-correction
result = oversight.process_input("openai", "Write a short test sentence.", auto_correct=True)
print(result)  # Metrics are logged to oversight.db automatically
```

#### Sample Output:

```python
{
    'output': 'This is a test.',
    'validation': 'Word count: 5 (max: 10) - Valid | Contains 'test': Yes',
    'guidance': 'Looks good!',
    'metrics': {'response_time': 0.85, 'accuracy': 1.0},
    'retries': 0
}
```

> **Note**: The SQLite database (`oversight.db`) is created and metrics are logged automatically whenever `process_input` or `track_metrics` is called. No separate initialization is required.

## Supported Rules

### Text Length
- `max_words=<int>`: Max word count (e.g., `max_words=50`).
- `min_words=<int>`: Min word count (e.g., `min_words=10`).
- `max_chars=<int>`: Max character count (e.g., `max_chars=200`).
- `min_chars=<int>`: Min character count (e.g., `min_chars=20`).
- `max_sentences=<int>`: Max sentence count (e.g., `max_sentences=3`).
- `min_sentences=<int>`: Min sentence count (e.g., `min_sentences=1`).

### Content
- `must_contain=<text>`: Must include text (e.g., `must_contain=data`).
- `must_not_contain=<text>`: Must exclude text (e.g., `must_not_contain=error`).
- `exact_match=<text>`: Must match exactly (e.g., `exact_match=Hello world`).
- `starts_with=<text>`: Must start with text (e.g., `starts_with=The`).
- `ends_with=<text>`: Must end with text (e.g., `ends_with=.`).

### Structural
- `has_punctuation=<yes/no>`: Check for punctuation (e.g., `has_punctuation=yes`).
- `has_numbers=<yes/no>`: Check for numbers (e.g., `has_numbers=no`).
- `max_unique_words=<int>`: Max unique words (e.g., `max_unique_words=20`).
- `min_unique_words=<int>`: Min unique words (e.g., `min_unique_words=5`).

### Advanced (OpenAI)
- `is_coherent=<yes>`: Must be coherent (e.g., `is_coherent=yes`).
- `tone=<positive/negative/neutral>`: Must match tone (e.g., `tone=positive`).
- `is_factual=<yes>`: Must be factually plausible (e.g., `is_factual=yes`).
- `readability=<easy/medium/hard>`: Must match readability level (e.g., `readability=easy`).
- `improve=<yes>`: Suggest an improvement (e.g., `improve=yes`).

### Performance
- `max_response_time=<float>`: Max response time in seconds (e.g., `max_response_time=1.5`).

## Supported Models

- `openai`: GPT-3.5-turbo (requires OpenAI API key).
- `deepseek`: DeepSeek R1 (requires DeepSeek API key).
- `grok`: Grok 3 (requires xAI API key, placeholder until official API is available).

## Requirements

Create a `requirements.txt` file with:

```text
Flask==2.3.3
nltk==3.8.1
openai==1.10.0
requests==2.31.0
textblob==0.18.0
```

## Configuration

**API Keys**: Provide keys during initialization (e.g., `AgentOversight(openai_api_key="your-key")`). For security, use environment variables:

```python
import os
oversight = AgentOversight(openai_api_key=os.getenv("OPENAI_API_KEY"))
```

## Contributing

1. Fork the repository: [GitHub Repository](https://github.com/LogeswaranA/AgentOversight).
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

For questions or suggestions, reach out via GitHub Issues or email at [loks2cool@gmail.com](mailto:loks2cool@gmail.com).

