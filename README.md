# 🛡️ AI-Powered Phishing Email Detector

> **Blue Team SOC Analyst Project** | Email Triage · Rule-Based Detection · LLM Analysis · Prompt Injection Defense  
> Part of the [raphsec](https://github.com/raphsec) Blue Team Lab Roadmap

![Blue Team](https://img.shields.io/badge/BLUE_TEAM-SOC_ANALYST-blue?style=for-the-badge) ![Phishing](https://img.shields.io/badge/PHISHING-DETECTION-red?style=for-the-badge) ![AI](https://img.shields.io/badge/AI-GROQ-blueviolet?style=for-the-badge) ![Python](https://img.shields.io/badge/PYTHON-STREAMLIT-green?style=for-the-badge)

Paste a suspicious email and get a **Phishing** or **Legitimate** verdict, with a confidence score and the reasons behind it.

Built as a Blue Team / SOC portfolio project. It runs on free tools only, and the heavy AI work happens in the cloud so a laptop stays fast.

## How it works

![Architecture](docs/01-architecture.png)

1. **Streamlit app**: a simple local web page where you paste the email.
2. **Quick checks** (`checks.py`): plain Python rules collect hard evidence: raw-IP links, URL shorteners, punycode domains, non-HTTPS links, and a From vs Reply-To domain mismatch.
3. **Groq AI** (`openai/gpt-oss-20b`): receives the email plus the rule findings and returns a structured JSON verdict.
4. **Verdict**: the app shows Phishing or Legitimate, a confidence score, red flags, and a recommended action.
5. **.env file**: the Groq API key is stored here and read at runtime, so it never appears in the code or on GitHub.

## Why rules plus AI

Rules give facts that cannot be argued with (a link really does use a raw IP address). The AI adds judgment about tone, urgency and context. Together the result is easier to trust and easier to explain.

## Security design

- **Untrusted input:** the prompt tells the model the email is data, never instructions, and treats "ignore previous instructions" inside an email as a phishing indicator.
- **Defanged links:** links shown in the app are written as `hxxp://192[.]0[.]2[.]44` so nobody clicks them by accident.
- **Secrets:** the API key lives only in `.env`, which is listed in `.gitignore`.
- **Deterministic output:** temperature is 0 and the response must be valid JSON.

## Demo

**Phishing email**

![Phishing verdict](docs/08-app-phishing-verdict.png)

**Legitimate email**

![Legitimate verdict](docs/09-app-legitimate-verdict.png)

**Prompt injection attempt (the email tells the AI to call it Legitimate)**

![Prompt injection test](docs/10-prompt-injection-test.png)

The model ignored the embedded instruction, flagged it as a red flag, and the rule-based checks caught the shortened, non-HTTPS link on their own.

**Quick checks on their own**

![Local checks](docs/07-local-checks.png)

## Setup

```bash
git clone https://github.com/raphsec/phishing-email-detector.git
cd phishing-email-detector

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a free key at https://console.groq.com/keys, then create a file named `.env` in the project folder containing one line:

```
GROQ_API_KEY=your_key_here
```

## Run

```bash
streamlit run app.py
```

Open http://localhost:8501 and paste an email.

## Limits

- The free Groq tier has rate limits. If you hit one, wait a minute and try again.
- Emails are cut to 6,000 characters.
- AI verdicts can be wrong. Use this as a triage aid, not a final ruling.

## Next steps

- Parse SPF, DKIM and DMARC results from full email headers
- Cross-check extracted links with my urlscan.io phishing URL scanner project
- Upload `.eml` files directly

## Tech

Python, Streamlit, Groq API, python-dotenv, regex
