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

def send_email(subject, body, sender_email, receiver_email, password):
    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email), message)

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

def read_ram():
    memory = psutil.virtual_memory()
    print("Total RAM:", memory.total)
    print("Available RAM:", memory.available)

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

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def volume_control():
    def get_volume():
        current_volume = volume.GetMasterVolumeLevelScalar()
        return current_volume

    def set_volume(level):
        print(f"Setting volume to {level * 100}%")
        volume.SetMasterVolumeLevelScalar(level, None)
        print(f"Volume set to {get_volume() * 100}%")

    def change_volume(delta):
        current_volume = get_volume()
        print(f"Current volume: {current_volume * 100}%")
        new_volume = max(0.0, min(1.0, current_volume + delta))
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        print(f"Volume changed to {get_volume() * 100}%")

    print("Volume Control Options:")
    print("1. Get Volume")
    print("2. Set Volume")
    print("3. Change Volume")
    sub_choice = int(input("Enter your choice: "))

    if sub_choice == 1:
        current_volume = get_volume()
        print(f"Current volume: {current_volume * 100}%")
    elif sub_choice == 2:
        level = float(input("Enter volume level (0.0 to 1.0): "))
        set_volume(level)
    elif sub_choice == 3:
        delta = float(input("Enter volume change (positive or negative): "))
        change_volume(delta)
    else:
        print("Invalid choice. Please try again.")

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

def show_menu():
    print("Choose an option to run:")
    print("1. Send an Email")
    print("2. Get Current Location")
    print("3. Scrape Google")
    print("4. Read RAM Info")
    print("5. Send SMS Message")
    print("6. Text to Speech")
    print("7. Send WhatsApp Message")
    print("8. Volume Control")
    print("9. Capture Image")

def main():
    show_menu()
    choice = int(input("Enter your choice: "))

    if choice == 1:
        send_email("Test Subject", "This is a test email sent from Dattaram.", "dattaramparab181@gmail.com", "bahadkarvivek@gmail.com", "yuwx vzra qtvy rosf")
    elif choice == 2:
        latitude, longitude, location = get_current_location()
        print("Latitude:", latitude)
        print("Longitude:", longitude)
        print("Location:", location)
    elif choice == 3:
        query = input("Enter your search query: ")
        num_results = 5
        search_results = scrape_google(query, num_results)
        print("Top 5 search results:")
        for idx, result in enumerate(search_results, start=1):
            print(f"{idx}. {result}")
    elif choice == 4:
        read_ram()
    elif choice == 5:
        send_sms_message("Hello from Python!")
    elif choice == 6:
        text_to_speak = "Gaurav Tu Madarchod"
        speak(text_to_speak)
    elif choice == 7:
        phone_number = "+919324785325"
        message = "Hello, this is a test message from Python!"
        number_of_messages = 5
        send_whatsapp_message(phone_number, message, number_of_messages)
    elif choice == 8:
        volume_control()
    elif choice == 9:
        capture_image()
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
