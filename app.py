"""
SaZSoft Global Marketing Ltd - Website
----------------------------------------
A small Flask website with 5 pages (Home, Team, 3x Service pages, Contact)
plus a working contact form that emails submissions to the company inbox.

Run locally:
    python app.py

The contact form needs SMTP credentials to actually send email.
See README.md for full setup instructions (this will NOT send real
emails until you configure a .env file).
"""

import os
import re
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load variables from a local .env file (see .env.example)
load_dotenv()

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration (all pulled from environment variables — never hard-code
# real email passwords directly in source code)
# ---------------------------------------------------------------------------
COMPANY_NAME = "SaZSoft Global Marketing Ltd"
RECEIVING_EMAIL = "christopherbennettwikieditor@gmail.com"

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")  # the Gmail address that SENDS the mail
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")  # a 16-character Gmail "App Password"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Static data for the "Team" page — edit names/emails here any time.
TEAM = {
    "ceo": {"name": "Zeeshan Ahmed", "role": "Chief Executive Officer"},
    "departments": [
        {
            "key": "editorial",
            "title": "Editorial Department",
            "blurb": "Researches, writes and publishes every Wikipedia article we take on.",
            "color": "gold",
            "members": [
                {"name": "James Whitmore", "role": "Senior Editor"},
                {"name": "Christopher Bennett", "role": "Senior Editor"},
                {"name": "Alexander Brooks", "role": "Senior Editor"},
            ],
        },
        {
            "key": "finance",
            "title": "Finance Department",
            "blurb": "Handles invoicing, payments and account queries.",
            "color": "cyan",
            "members": [
                {"name": "Muhammad Adnan", "role": "Finance Officer"},
                {"name": "Zeeshan Ahmed", "role": "Finance Director"},
                {"name": "Muhammad Riaz", "role": "Finance Director"},
            ],
        },
        {
            "key": "client",
            "title": "Client Representative Team",
            "blurb": "Your first point of contact — onboarding, updates and support.",
            "color": "violet",
            "members": [
                {"name": "James Whitmore", "role": "Client Representative"},
                {"name": "Zephiron Maxwell", "role": "Client Representative"},
                {"name": "Jonathan Ellis", "role": "Client Representative"},
                {"name": "Elizabeth Mercer", "role": "Client Representative"},
                {"name": "Ethan Caldwell", "role": "Client Representative"},
                {"name": "Charles Whitaker", "role": "Client Representative"},
                {"name": "Alexander Brooks", "role": "Client Representative"},
                {"name": "Emma Kensington", "role": "Client Representative"},
                {"name": "Matthew Sterling", "role": "Client Representative"},
                {"name": "Andrew Velson", "role": "Client Representative"},
                {"name": "Christopher Bennett", "role": "Client Representative"},
                {"name": "Nathan Cole", "role": "Client Representative"},
                {"name": "Julia Whitaker", "role": "Client Representative"},
                {"name": "David Kensington", "role": "Client Representative"},
                {"name": "Henry Lonford", "role": "Client Representative"},
                {"name": "Justin Reed", "role": "Client Representative"},
                {"name": "Olivia Brooks", "role": "Client Representative"},
                {"name": "Edward Lawson", "role": "Client Representative"},
                {"name": "Lucas Bennett", "role": "Client Representative"},
            ],
        },
    ],
}


def make_email(name):
    """Turns 'James Whitmore' into a placeholder company email.
    Replace TEAM member emails with real addresses whenever you have them."""
    slug = name.lower().replace(" ", ".")
    return f"{slug}@sazsoftglobal.co.uk"


for dept in TEAM["departments"]:
    for m in dept["members"]:
        m["email"] = make_email(m["name"])
TEAM["ceo"]["email"] = make_email(TEAM["ceo"]["name"])


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html", active="home")


@app.route("/team")
def team():
    return render_template("team.html", active="team", team=TEAM)


@app.route("/services/wikipedia-editing")
def service_wikipedia():
    return render_template("service_wikipedia.html", active="wikipedia")


@app.route("/services/web-development")
def service_webdev():
    return render_template("service_webdev.html", active="webdev")


@app.route("/services/graphic-designing")
def service_graphic():
    return render_template("service_graphic.html", active="graphic")


@app.route("/contact")
def contact():
    return render_template("contact.html", active="contact")


# ---------------------------------------------------------------------------
# Contact form submission (AJAX -> JSON)
# ---------------------------------------------------------------------------
@app.route("/submit-contact", methods=["POST"])
def submit_contact():
    data = request.form

    # Honeypot spam trap — real users never fill this hidden field
    if data.get("website"):
        return jsonify(success=True, message="Message sent."), 200

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    service = (data.get("service") or "General Inquiry").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify(success=False, message="Please fill in your name, email and message."), 400

    if not EMAIL_RE.match(email):
        return jsonify(success=False, message="Please enter a valid email address."), 400

    body = (
        f"New enquiry from the {COMPANY_NAME} website\n"
        f"{'-' * 45}\n"
        f"Name:    {name}\n"
        f"Email:   {email}\n"
        f"Service: {service}\n\n"
        f"Message:\n{message}\n"
    )

    sent = send_email(
        subject=f"New website enquiry — {service}",
        body=body,
        reply_to=email,
    )

    if sent:
        return jsonify(success=True, message="Your message has been sent. We'll be in touch shortly."), 200

    # Even if SMTP isn't configured yet (e.g. during local development),
    # don't break the user's experience — just log it and say so.
    print("---- CONTACT FORM SUBMISSION (email NOT sent — SMTP not configured) ----")
    print(body)
    return jsonify(
        success=False,
        message="Sorry, something went wrong sending your message. Please email us directly instead.",
    ), 500


def send_email(subject, body, reply_to):
    """Sends an email via SMTP using the credentials in the environment.
    Returns True on success, False if SMTP isn't configured or fails."""
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        return False

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr((COMPANY_NAME, SMTP_USERNAME))
    msg["To"] = RECEIVING_EMAIL
    msg["Reply-To"] = reply_to

    try:
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=15) as server:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(SMTP_USERNAME, [RECEIVING_EMAIL], msg.as_string())
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(SMTP_USERNAME, [RECEIVING_EMAIL], msg.as_string())
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"[email error] {exc}")
        return False


if __name__ == "__main__":
    app.run(debug=True, port=5000)