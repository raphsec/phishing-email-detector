import re
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s<>\"')\]]+", re.IGNORECASE)
IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
FROM_RE = re.compile(r"^From:.*?@([\w.-]+)", re.IGNORECASE | re.MULTILINE)
REPLY_RE = re.compile(r"^Reply-To:.*?@([\w.-]+)", re.IGNORECASE | re.MULTILINE)
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly", "rebrand.ly", "cutt.ly"}


def defang(url):
    """Make a link unclickable so nobody opens it by accident."""
    return url.replace("http", "hxxp", 1).replace(".", "[.]")


def extract_signals(email_text):
    """Collect hard evidence from the email using simple rules."""
    signals = []

    urls = list(dict.fromkeys(URL_RE.findall(email_text)))
    for url in urls[:15]:
        url = url.rstrip(".,;:")
        host = (urlparse(url).hostname or "").lower()
        if IP_RE.match(host):
            signals.append("Link uses a raw IP address: " + defang(url))
        if host in SHORTENERS:
            signals.append("Link uses a URL shortener: " + defang(url))
        if "xn--" in host:
            signals.append("Link uses punycode (possible look-alike domain): " + defang(url))
        if url.lower().startswith("http://"):
            signals.append("Link is not HTTPS: " + defang(url))

    sender = FROM_RE.search(email_text)
    reply = REPLY_RE.search(email_text)
    if sender and reply and sender.group(1).lower() != reply.group(1).lower():
        signals.append(
            "From domain (" + sender.group(1) + ") differs from Reply-To domain (" + reply.group(1) + ")"
        )

    return signals


if __name__ == "__main__":
    demo = """From: "PayPal Security" <security-alert@paypa1-support.example>
Reply-To: helpdesk.recovery@gmail.com
Subject: URGENT: Verify your account

Click here to verify now: http://192.0.2.44/paypal/secure-login
"""
    for signal in extract_signals(demo):
        print("-", signal)
