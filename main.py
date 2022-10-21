import argparse
import http.client
import json
import sys


def format_str(subject, body):
    retval = f"*{subject}*\n\n" + body
    return retval


def send(botid: str, userid: str, subject: str, body: str):
    h1 = http.client.HTTPSConnection("api.telegram.org")
    request = {
        "chat_id": userid,
        "text": format_str(subject, body),
        "parse_mode": "MarkdownV2",
    }
    response = h1.request(
        "POST",
        f"/bot{botid}/sendMessage",
        body=json.dumps(request),
        headers={"Content-Type": "application/json"},
    )

    response = h1.getresponse()
    if response.status != 200:
        print('Failed to send message:')
        print(f"Status: {response.status}, reason: {response.reason}")
        print(f"Body: {response.read()}")
    h1.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read an email from stdin and send it to the given telegram ids"
    )
    parser.add_argument("bottoken", help="Token to use to send the message with")
    parser.add_argument("userid", help="Telegram userid to send the message to")
    parser.add_argument("subject", help="Subject of the message to be sent")
    args = parser.parse_args()
    body = sys.stdin.read()
    send(args.bottoken, args.userid, args.subject, body)
