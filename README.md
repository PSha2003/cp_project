# Slack DLP Tool

## Overview
This tool scans Slack messages and files for sensitive data using predefined patterns. The application blocks Slack messages containing sensitive data and stores relevant matches in a database. Additionally, it allows file uploads to scan for sensitive data using the DLP (Data Loss Prevention) tool.

## How to run
### 1. Create a Slack App
- Go to the [Slack API page](https://api.slack.com/apps) and create a new Slack app.
- Subscribe to relevant events (e.g., `message` events) and point them to the `/slack/events/` endpoint in your application.

### 2. Set your Slack bot token 
- In `dlp/tasks.py`, set the `SLACK_BOT_TOKEN` variable to your Slack bot’s token. This is required for updating the Slack message to indicate that it has been blocked.
  ```python
  SLACK_BOT_TOKEN = 'your-slack-bot-token'
  ```

### 3. Run the application
- Build and run the application using docker compose:
`docker-compose up --build`

### 4. Access Django Admin
- Go to Django admin panel at [http://localhost:8000/admin](http://localhost:8000/admin) 
- Use the following credentials to login (username: admin, password: P@ssw0rd)

### 5. Add patterns 
- In the Django Admin, navigate to the "Patterns" section and add DLP patterns (e.g., a regex pattern for credit card numbers: \b\d{16}\b).

### 6. Sensitive slack messages
- Slack Messages contaning sensitive data will get blocked and the original message will be replace. 
- Matches for sensitive data will be stored in the database for future.

### 7. Scan a file using DLP tool
- To scan a file using the DLP tool - upload a file using scan/file API. For example, you can use curl to upload a file for scanning: `curl -F 'file=@./scantest.txt' http://127.0.0.1:8000/scan/file/`
- The file content will be scanned for sensitive data, and any matches will be stored in the database.
    
### 8. Queue implementation
- Default implementation uses Redis for the message queue. 
- To switch to SQS, set `use_real_sqs = True` in  `dlp/shared_queue.py`. Update `queue_url` and `region` in the same file. Set AWS credentials in .aws/credentials.ini
