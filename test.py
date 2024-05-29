from win32com.client import Dispatch
from time import sleep

mp = Dispatch("WMPlayer.OCX")
tune = mp.newMedia("./plays.wav")
mp.currentPlaylist.appendItem(tune)
mp.controls.play()
sleep(1)
mp.controls.playItem(tune)
raw_input("Press Enter to stop playing")
mp.controls.stop()