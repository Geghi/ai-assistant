🛠 How to Implement the POC
1. Telegram Bot Setup
Create via BotFather

Set webhook to your FastAPI or Azure endpoint

2. Email Summarizer Logic
Use Gmail API to:

Authenticate (OAuth2)

Fetch last 24h emails

Store last processed ID

Use GPT-4o to:

Classify (Urgent / FYI / Spam)

Detect construction-related issues (via prompt)

Summarize important messages

Send result via Telegram

3. Voice Note to Email Draft
Receive voice via Telegram webhook

Download audio file → transcribe with Whisper API

Generate email draft with GPT-4o:

Use a prompt like:
"Write a polite business follow-up email based on this message..."

Send draft back to user via Telegram