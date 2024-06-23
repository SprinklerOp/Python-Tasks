from twilio.rest import Client

def send_sms_message(message):
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_='+12232504518',
        to='+919324785325'     
    )

    
    print("SMS sent successfully.")


send_sms_message("Hello from Datta!")
