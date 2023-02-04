import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import applescript
from sys import platform

# sessions = None

# def setUp():
#     sessions = AudioUtilities.GetAllSessions()
    
def mute():
    if platform == "linux" or platform == "linux2":
        pass
    elif platform == "darwin":
        applescript.AppleScript("set volume with output muted").run()
    elif platform == "win32":
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            print(volume.GetMasterVolume())
            volume.SetMasterVolume(0, None)
            if session.Process and session.Process.name() == "vlc.exe":
                print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
                volume.SetMasterVolume(0.6, None)
        
        
def performAction(gesture):
    if gesture == "LOW_BRIGHTNESS":
        sbc.set_brightness(20)
    elif gesture == "HIGH_BRIGHTNESS":
        sbc.set_brightness(100)
    elif gesture == "MUTE":
        mute()

    