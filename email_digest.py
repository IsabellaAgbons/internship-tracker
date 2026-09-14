"""Build and send an HTML internship digest email via Gmail SMTP."""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from html import escape
from dotenv import load_dotenv

load_dotenv()
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
FROM_EMAIL = "bellagbons6@gmail.com"
TO_EMAIL = "bellagbons6@gmail.com"

def format_email_body(postings):
    """Return an HTML digest of postings, or a no-news message if the list is empty."""
    if not postings:
        return "<p>No new internships this week</p>"
    rows = []
    for posting in postings:
        company = escape(str(posting.get("company", "")))
        role = escape(str(posting.get("role", "")))
        location = escape(str(posting.get("location", "")))
        url = escape(str(posting.get("url", "")), quote=True)
        rows.append(
            "<tr>"
            f"<td>{company}</td>"
            f"<td>{role}</td>"
            f"<td>{location}</td>"
            f'<td><a href="{url}">View posting</a></td>'
            "</tr>"
        )
    return (
        "<h1>New internships</h1>"
        "<table>"
        "<tr><th>Company</th><th>Role</th><th>Location</th><th>Link</th></tr>"
        f"{''.join(rows)}"
        "</table>"
    )
def send_email(subject, body):
    """Send an HTML email from FROM_EMAIL to TO_EMAIL using Gmail SMTP."""
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = FROM_EMAIL
    message["To"] = TO_EMAIL
    message.attach(MIMEText(body, "html"))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(FROM_EMAIL, GMAIL_APP_PASSWORD)
    server.send_message(message)
    server.quit()
def run(postings):
    """Build the digest subject and body, then send the email."""
    subject = f"Internship Digest - {len(postings)} new postings"
    body = format_email_body(postings)
    send_email(subject, body)