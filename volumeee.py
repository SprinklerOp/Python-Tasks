from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

user_input = input("Enter the volume level (0.0 to 1.0): ")

if user_input.replace('.', '', 1).isdigit() and 0.0 <= float(user_input) <= 1.0:
    volume.SetMasterVolumeLevelScalar(float(user_input), None)
    print(f"Volume set to {float(user_input) * 100}%")
else:
    print("Please enter a numeric value between 0.0 and 1.0.")
