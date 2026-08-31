"""Build and send an HTML internship digest email via SendGrid."""
import os
from html import escape
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "your.email@example.com"
TO_EMAIL = "your.email@example.com"

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
    """Send an HTML email from FROM_EMAIL to TO_EMAIL using SendGrid."""
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject=subject,
        html_content=body,
    )
    client = SendGridAPIClient(SENDGRID_API_KEY)
    response = client.send(message)
    print(response.status_code)
def run(postings):
    """Build the digest subject and body, then send the email."""
    subject = f"Internship Digest - {len(postings)} new postings"
    body = format_email_body(postings)
    send_email(subject, body)