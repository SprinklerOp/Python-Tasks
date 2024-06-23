from twilio.rest import Client

def send_sms_message(message):
    account_sid = 'ACc92aec7d8fdf0a995c21bb6ed0f9e287'
    auth_token = '1e272c02402fe7b9c2dd703155a74411'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_='+12232504518',
        to='+919324785325'     
    )

    
    print("SMS sent successfully.")


send_sms_message("Hello from Datta!")
