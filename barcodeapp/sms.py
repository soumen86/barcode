import email, smtplib, ssl
from providers import PROVIDERS

def send_sms_via_email(
    number: str,
    message: str,
    provider: str,
    sender_credentials: tuple,
    subject: str = "food coupon",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'
    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

def main():
    number = "8586104569"
    message = "http://127.0.0.1:8000/media/Arun%20Kundu_qr_1683335874.6399226_2.png"
    provider = "T-Mobile"

    sender_credentials = ("ghosh.soumen86@gmail.com", "flyryksfluycnyhl")

    send_sms_via_email(number, message, provider, sender_credentials)

if __name__ == "__main__":
    main()
