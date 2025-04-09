# Slack DLP Tool

## How to run

1. Create Slack app, subscribe to events, point to `/slack/events/`.
2. Set your Slack bot token in `tasks.py`. This will switch the message on slack saying the original message is blocked
3. Run: `docker-compose up --build`
4. Access Django Admin: [http://localhost:8000/admin](http://localhost:8000/admin) (username: admin, password: P@ssw0rd)
5. Add patterns like credit card regex: `\b\d{16}\b`
6. Slack Messages with sensitive data get blocked and stored.
7. To scan a file using the DLP tool - upload a file using scan/file API. example: curl -F 'file=@./scantest.txt' http://127.0.0.1:8000/scan/file/
8. Messages from files with sensitive data get stored
