import smtplib

def send_email(subject, body, sender_email, receiver_email, password):
    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    print("Email sent successfully.")

send_email("Test Subject", "This is a test email sent from Dattaram.", "dattaramparab181@gmail.com", "dilipjarwal90@gmail.com", "yuwx vzra qtvy rosf")
