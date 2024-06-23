import smtplib
import geocoder
from googlesearch import search
from twilio.rest import Client
import pyttsx3
import pywhatkit as kit
import datetime
import cv2
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import subprocess
import speech_recognition as sr
import paramiko
import warnings
import boto3

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

# Predefined sender email and password
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-password"

def send_email():
    subject = input("Enter the subject of the email: ")
    body = input("Enter the body of the email: ")
    receiver_email = input("Enter the receiver's email: ")

    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message)
    print("Email sent successfully.")

def get_current_location():
    current_location = geocoder.ip('me')
    latitude, longitude = current_location.latlng
    location_info = geocoder.osm([latitude, longitude], method='reverse')
    return latitude, longitude, location_info.address

def scrape_google():
    query = input("Enter search query: ")
    num_results = int(input("Enter number of results to fetch: "))
    search_results = [result for result in search(query, num_results=num_results)]
    return search_results

def send_sms_message():
    account_sid = input("Enter your Twilio account SID: ")
    auth_token = input("Enter your Twilio auth token: ")
    client = Client(account_sid, auth_token)
    message_body = input("Enter the message you want to send: ")
    from_number = input("Enter the sender's phone number (Twilio number): ")
    to_number = input("Enter the receiver's phone number (in international format): ")

    message = client.messages.create(
        body=message_body,
        from_=from_number,
        to=to_number
    )
    print("SMS sent successfully.")

def speak():
    text = input("Enter the text you want to be spoken: ")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 1.0)
    for voice in voices:
        engine.setProperty('voice', voice.id)
        engine.say(text)
        engine.runAndWait()

def send_whatsapp_message():
    phone_number = input("Enter the phone number (in international format): ")
    message = input("Enter the message you want to send: ")
    number_of_messages = int(input("Enter number of messages: "))
    now = datetime.datetime.now()

    for i in range(number_of_messages):
        send_time = now + datetime.timedelta(minutes=i + 1)
        hour = send_time.hour
        minute = send_time.minute
        try:
            kit.sendwhatmsg(phone_number, message, hour, minute)
            print(f"Message scheduled successfully at {hour}:{minute:02d}: {message}")
        except Exception as e:
            print(f"An error occurred: {e}")

def run_local_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print("Error:", result.stderr)

def run_remote_command():
    host = input("Enter the remote host: ")
    username = input("Enter the remote username: ")
    password = input("Enter the remote password: ")
    command = input("Enter the command to run: ")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read()
        error = stderr.read()
        if output:
            print(output.decode())
        if error:
            print("Error:", error.decode())
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        ssh_client.close()

def get_default_audio_device():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume.iid, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def get_current_volume():
    volume = get_default_audio_device()
    current_volume = volume.GetMasterVolumeLevelScalar()
    return int(current_volume * 100)

def set_volume():
    volume = get_default_audio_device()
    try:
        level = int(input("Enter the volume level (0-100): "))
        if 0 <= level <= 100:
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            print(f"Volume set to {level}%")
        else:
            print("Volume level must be between 0 and 100")
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 100")

def capture_image():
    a = cv2.VideoCapture(0)
    status, photo = a.read()
    if status:
        filename = input("Enter the filename to save the image (e.g., image.png): ")
        cv2.imwrite(filename, photo)
        cv2.imshow(filename, photo)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
        print(f"Image captured and saved as {filename}")
    else:
        print("Failed to capture image")

def recognize_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=5)
        print("Microphone calibrated")
        print("Speak now...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

def show_menu():
    print("\nMenu:")
    print("1. Send an Email")
    print("2. Get Current Location")
    print("3. Scrape Google")
    print("4. Run Local/Remote Shell Command")
    print("5. Send SMS Message")
    print("6. Text to Speech")
    print("7. Send WhatsApp Message")
    print("8. Volume Control")
    print("9. Capture Image")
    print("10. Voice Bot")
    print("11. Manage AWS EC2 Instances")
    print("12. Exit")

def voicebot():
    import google.generativeai as genai
    from gtts import gTTS

    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 140)
        engine.setProperty('volume', 1.0)
        for voice in voices:
            engine.setProperty('voice', voice.id)
            engine.say(text)
            engine.runAndWait()

    api_key = input("Enter your Google API key: ")
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    print('Voice bot starting')

    while True:
        print("-- Speak Now -- ")
        prompt = recognize_voice()
        if "exit" in prompt or "quit" in prompt:
            break

        if prompt:
            response = chat_session.send_message(prompt)
            print(response.text)
            speak(response.text)

# AWS EC2 Management Functions
def create_instance(ec2_resource):
    instance = ec2_resource.create_instances(
        InstanceType="t2.micro",
        ImageId="ami-0cc9838aa7ab1dce7",
        MaxCount=1,
        MinCount=1
    )
    instance_id = instance[0].id
    print(f"Instance created with ID: {instance_id}")
    return instance_id

def stop_instance(ec2_client, instance_id):
    try:
        stop_response = ec2_client.stop_instances(InstanceIds=[instance_id])
        print(f"Stopping instance: {instance_id}")
        waiter = ec2_client.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=[instance_id])
        print(f"Instance stopped: {instance_id}")
    except boto3.exceptions.Boto3Error as error:
        print(f"Error stopping instance: {error}")

def terminate_instance(ec2_client, instance_id):
    try:
        terminate_response = ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"Terminating instance: {instance_id}")
        waiter = ec2_client.get_waiter('instance_terminated')
        waiter.wait(InstanceIds=[instance_id])
        print(f"Instance terminated: {instance_id}")
    except boto3.exceptions.Boto3Error as error:
        print(f"Error terminating instance: {error}")

def aws_menu():
    access_key = input("Enter your AWS access key: ")
    secret_key = input("Enter your AWS secret key: ")

    ec2_resource = boto3.resource(
        "ec2",
        region_name="ap-south-1",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    ec2_client = boto3.client(
        "ec2",
        region_name="ap-south-1",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    while True:
        print("AWS EC2 Management:")
        print("1. Create an EC2 instance")
        print("2. Stop an EC2 instance")
        print("3. Terminate an EC2 instance")
        print("4. Back to main menu")
        choice = input("Enter the number of your choice: ")

        if choice == '1':
            create_instance(ec2_resource)
        elif choice == '2':
            instance_id = input("Enter the instance ID to stop: ")
            stop_instance(ec2_client, instance_id)
        elif choice == '3':
            instance_id = input("Enter the instance ID to terminate: ")
            terminate_instance(ec2_client, instance_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter a valid number (1-4).")

def main():
    while True:
        show_menu()
        user_choice = input("Enter the number of your choice or say the action: ").lower()

        if user_choice == '1' or 'email' in user_choice:
            send_email()

        elif user_choice == '2' or 'location' in user_choice:
            latitude, longitude, address = get_current_location()
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            print(f"Address: {address}")

        elif user_choice == '3' or 'scrape' in user_choice:
            results = scrape_google()
            for result in results:
                print(result)

        elif user_choice == '4' or 'shell' in user_choice:
            print("\nShell Command Menu:")
            print("1. List files")
            print("2. Create a directory")
            print("3. Display running processes")
            print("4. Show current directory")
            print("5. Back to main menu")
            shell_choice = input("Enter your choice: ")

            if shell_choice == "1":
                command = "ls -l"
            elif shell_choice == "2":
                dir_name = input("Enter directory name to create: ")
                command = f"mkdir {dir_name}"
            elif shell_choice == "3":
                command = "ps -aux"
            elif shell_choice == "4":
                command = "pwd"
            elif shell_choice == "5":
                continue
            else:
                print("Invalid choice")
                continue

            location = input("Run command locally or remotely? (local/remote): ")

            if location == "local":
                run_local_command(command)
            elif location == "remote":
                run_remote_command()
            else:
                print("Invalid location")

        elif user_choice == '5' or 'sms' in user_choice:
            send_sms_message()

        elif user_choice == '6' or 'speak' in user_choice:
            speak()

        elif user_choice == '7' or 'whatsapp' in user_choice:
            send_whatsapp_message()

        elif user_choice == '8' or 'volume' in user_choice:
            current_volume = get_current_volume()
            print(f"Current volume: {current_volume}%")
            set_volume()

        elif user_choice == '9' or 'selfie' in user_choice or 'photo' in user_choice:
            capture_image()

        elif user_choice == '10' or 'voicebot' in user_choice:
            voicebot()

        elif user_choice == '11' or 'aws' in user_choice:
            aws_menu()

        elif user_choice == '12' or 'exit' in user_choice:
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
