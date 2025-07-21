# AI Assistant

This project is a multi-functional AI assistant that integrates with Telegram, Gmail, and OpenAI/Google AI services. It can summarize emails, draft emails from voice notes, and perform other AI-powered tasks.

## Features

- **Email Summarization**: Fetches emails from the last 24 hours, classifies them (Urgent, FYI, Spam), identifies construction-related issues, and sends a summary via Telegram.
- **Voice Note to Email Draft**: Transcribes voice notes received via Telegram and generates a polite, professional email draft.

## Project Structure

```
.
├── api
│   └── v1
│       ├── dependencies.py
│       └── endpoints
│           └── telegram.py
├── core
│   ├── agent_graph.py
│   └── config.py
├── models
│   ├── openai_models.py
│   └── telegram_models.py
├── prompts
│   ├── email_draft_prompt.py
│   └── router_prompt.py
├── services
│   ├── gmail_service.py
│   ├── google_service.py
│   ├── openai_service.py
│   ├── scheduler_service.py
│   └── telegram_service.py
├── utils
│   └── http_client.py
├── .env.example
├── .gitignore
├── main.py
└── requirements.txt
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Geghi/ai-assistant.git
    cd ai-assistant
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Create a `.env` file** by copying the example file:
    ```bash
    cp .env.example .env
    ```

2.  **Fill in the environment variables** in the `.env` file:

    -   `telegram_token`: Your Telegram Bot token from BotFather.
    -   `telegram_chat_id`: The chat ID to send messages to.
    -   `OPENAI_API_KEY`: Your OpenAI API key.
    -   `GMAIL_CREDENTIALS_FILE`: Path to your Gmail API credentials JSON file.
    -   `TELEGRAM_WEBHOOK_URL`: The URL for your Telegram webhook (this will be your ngrok URL).
    -   `LLM_PROVIDER`: Choose between `google` or `openai`.
    -   `GOOGLE_API_KEY`: Your Google AI API key if you are using Google as the LLM provider.
    -   `GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_JSON`: Your Google Service Account Credentials if you are using Google as the LLM provider.

## Running the Application with Ngrok and Telegram

1.  **Start the FastAPI application:**
    ```bash
    uvicorn main:app --reload
    ```
    The application will be running on `http://127.0.0.1:8000`.

2.  **Expose your local server to the internet using ngrok:**
    ```bash
    ngrok http 8000
    ```
    Ngrok will provide you with a public HTTPS URL (e.g., `https://<random-string>.ngrok.io`).

3.  **Set the Telegram webhook:**
    -   Copy the ngrok HTTPS URL.
    -   Update the `TELEGRAM_WEBHOOK_URL` in your `.env` file to `https://<random-string>.ngrok.io/api/v1/telegram/webhook`.
    -   You will need to run a script or use a tool like `curl` to set the webhook with the Telegram API. The application will attempt to set this on startup.

    To manually set the webhook, you can use the following `curl` command:
    ```bash
    curl -F "url=https://<random-string>.ngrok.io/api/v1/telegram/webhook" "https://api.telegram.org/bot<your_telegram_token>/setWebhook"
    ```

Now your AI assistant is running and connected to Telegram. You can send it voice notes or have it summarize your emails.
