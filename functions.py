import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import applescript
from sys import platform

# sessions = None

# def setUp():
#     sessions = AudioUtilities.GetAllSessions()
    
def mute(muteOn=True):
    if platform == "linux" or platform == "linux2":
        pass
    elif platform == "darwin":
        applescript.AppleScript("set volume with output muted").run()
    elif platform == "win32":
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        mute = 1 if muteOn else 0
        volume.SetMute(muteOn, None)
        
        
def performAction(gesture, fingerTouchingEar, withInFace):
    if gesture == "LOW_BRIGHTNESS":
        sbc.set_brightness(20)
    elif gesture == "HIGH_BRIGHTNESS":
        sbc.set_brightness(100)
    elif gesture == "MUTE" and withInFace:
        mute()
    elif gesture == "MUTE" and fingerTouchingEar:
        mute(False)

    