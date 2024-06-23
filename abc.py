import subprocess
import paramiko
import warnings
import smtplib
import geocoder
import googlesearch
import psutil
from twilio.rest import Client
import pyttsx3
import pywhatkit as kit
import datetime
import cv2
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import speech_recognition as sr

def send_email(subject, body, sender_email, receiver_email, password):
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    print("Email sent successfully.")

def get_current_location():
    current_location = geocoder.ip('me')
    latitude, longitude = current_location.latlng
    location_info = geocoder.osm([latitude, longitude], method='reverse')
    return latitude, longitude, location_info.address

def scrape_google(query, num_results=5):
    search_results = []
    for result in googlesearch.search(query, num_results=num_results):
        search_results.append(result)
    return search_results

def send_sms_message():
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=input("Enter the message you want to send: "),
        from_='+12232504518',
        to='+919324785325'
    )
    print("SMS sent successfully.")

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for i, voice in enumerate(voices):
        print(f"Voice {i}: {voice.name} ({voice.id})")
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 1.0)
    for voice in voices:
        engine.setProperty('voice', voice.id)
        print(f"Testing voice: {voice.name}")
        engine.say(text)
        engine.runAndWait()

def send_whatsapp_message(phone_number, message, number_of_messages):
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

def shell_command():
    subprocess.run(input("Enter the shell command: "), shell=True)

def get_default_audio_device():
    """Get the default audio device"""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume.iid, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def get_current_volume():
    """Get the current volume level as a percentage"""
    volume = get_default_audio_device()
    current_volume = volume.GetMasterVolumeLevelScalar()
    return int(current_volume * 100)

def set_volume(level):
    """Set the volume level (0 to 100)"""
    volume = get_default_audio_device()
    if 0 <= level <= 100:
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        print(f"Volume set to {level}%")
    else:
        raise ValueError("Volume level must be between 0 and 100")

def capture_image():
    a = cv2.VideoCapture(0)
    status, photo = a.read()
    if status:
        cv2.imwrite("datta.png", photo)
        cv2.imshow("datta.png", photo)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
        print("Image captured and saved as datta.png")
    else:
        print("Failed to capture image")

def run_local_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print("Error:", result.stderr)

def run_remote_command(host, username, password, command):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read()
    error = stderr.read()
    if output:
        print(output.decode())
    if error:
        print("Error:", error.decode())
    ssh_client.close()

def run_command(location, command):
    if location == "local":
        run_local_command(command)
    elif location == "remote":
        host = input("Enter remote host: ")
        username = input("Enter remote username: ")
        password = input("Enter remote password: ")
        run_remote_command(host, username, password, command)
    else:
        print("Invalid location")

def voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=5)
        print("Microphone calibrated")
        print("-------- !!  Order me Now !! --------")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            text = r.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def show_menu():
    print("Choose an option to run(Speak):")
    print("1. Send an Email")
    print("2. Get Current Location")
    print("3. Scrape Google")
    print("4. Run Shell Command")
    print("5. Send SMS Message")
    print("6. Text to Speech")
    print("7. Send WhatsApp Message")
    print("8. Volume Control")
    print("9. Capture Image")
    print("10. Run Local or Remote Command")

def main():
    while True:
        show_menu()
        print("! ! ------- Voice Command mode Activating ------- !!")
        choice = voice()
        if not choice:
            continue

        if "email" in choice and not "bulk mail" in choice:
            send_email(
                receiver_email=input("Enter the receiver email: "),
                subject=input('Enter the subject: '),
                sender_email="dattaramparab181@gmail.com",
                password="yuwx vzra qtvy rosf",
                body=input("Enter the email body you want to send: ")
            )

        elif "location" in choice:
            latitude, longitude, location = get_current_location()
            print("Latitude:", latitude)
            print("Longitude:", longitude)
            print("Location:", location)

        elif 'search' in choice:
            print("-- Speak what to search ---\n\n")
            query = voice()
            num_results = 5
            search_results = scrape_google(query, num_results)
            print("Top 5 search results:")
            for idx, result in enumerate(search_results, start=1):
                print(f"{idx}. {result}")

        elif "shell" in choice:
            shell_command()

        elif 'sms' in choice:
            send_sms_message()

        elif "speak" in choice:
            text_to_speak = input("Enter what you want me to speak: ")
            speak(text_to_speak)

        elif "send whatsapp" in choice:
            phone_number = input("Enter your phone number (in international format like (+911234567890)): ")
            message = input("Enter the message you want to send: ")
            number_of_messages = 1
            send_whatsapp_message(phone_number, message, number_of_messages)

        elif "volume" in choice:
            current_volume = get_current_volume()
            print(f"Current volume: {current_volume}%")
            try:
                new_volume = int(input("Enter new volume level (0-100): "))
                set_volume(new_volume)
            except ValueError as e:
                print(e)

        elif "selfie" in choice or "my photo" in choice:
            capture_image()

        elif "command" in choice:
            command = input("Enter the command to run: ")
            location = input("Run command locally or remotely? (local/remote): ")
            run_command(location, command)

        elif "voicebot" in choice or "voice bot" in choice:
            voicebot()

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
