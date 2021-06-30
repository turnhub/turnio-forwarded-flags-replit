from flask import Flask, request
import os
import requests

app = Flask("app")

# Repl provides these environment variables, we use it
# to construct the URL that this repl will be accessible on.
repl_owner = os.environ.get("REPL_OWNER")
repl_slug = os.environ.get("REPL_SLUG")
repl_url = f"https://{repl_slug}.{repl_owner.lower()}.repl.co"

TOKEN = os.environ.get("TOKEN")
HOST = os.environ.get("HOST", "https://whatsapp.turn.io")

@app.route("/")
def hello_world():
    return f"The Turn UI integration API endpoint is at {repl_url}/forwarded"


@app.route("/forwarded", methods=["POST"])
def forwarded():
    json = request.json

    if 'messages' not in json:
      return ''

    [message] = json["messages"]
    from_ = message["from"]
    context = message.get("context", {})
    forwarded = context.get("forwarded")
    frequently_forwarded = context.get("frequently_forwarded")

    if forwarded:
      send_reply(from_, "That message was forwarded!")
    elif frequently_forwarded:
      send_reply(from_, "That message was frequently forwarded!")
    else:
      print('this was not a forwarded message')

    return ''


def send_reply(to, text):
    return requests.post(f"{HOST}/v1/messages", headers={
        "Authorization": f"Bearer {TOKEN}",
        }, json={
          "to": to,
          "type": "text",
          "text": {
            "body": text
          }
        })

app.run(host='0.0.0.0', port=8080)