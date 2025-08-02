import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Set up SMS via email
EMAIL_FROM = 'mcfay1999@gmail.com'
EMAIL_TO = '9787667222@vtext.com'  # ← YOUR NUMBER'S SMS EMAIL
EMAIL_PASS = 'Molly0704!'  # Gmail app password

def send_sms(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject  # Most carriers will ignore this
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

def check_filings():
    url = "https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    today = datetime.now().strftime("%m/%d/%Y")
    alerts = []

    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 4:
            continue
        name = cells[0].get_text(strip=True)
        date = cells[2].get_text(strip=True)
        if today in date and ("Pelosi" in name or "Greene" in name):
            alerts.append(f"{name} filed on {date}")

    if alerts:
        send_sms("Congress Trade Alert", "\n".join(alerts))

check_filings()

