from kivy.app import App
from jnius import autoclass
from  time import strftime
from kivy.clock import Clock
from kivy.core.audio import SoundLoader,Sound
import os
os.environ['KIVY_AUDIO'] = 'sdl2'
MediaPlayer = autoclass("android.media.MediaPlayer")
FileInputStream = autoclass("java.io.FileInputStream")
AudioManager = autoclass("android.media.AudioManager")
#from android.permissions import request_permissions, Permission

#request_permissions([Permission.INTERNET, permissions.CAPTURE_AUDIO_OUTPUT])
class StopWatchApp(App):
    #sw_s = int(self.root.ids.total.text)
    sw_s =  0
    sw_Istarted = False
    #pathfile  = os.getcwd()+'/huuda.wav'
    pathfile  =  './assets/huuda.wav'
    print(pathfile)
    sound = SoundLoader.load(pathfile)
    sound.loop = True
    mediaplayer = MediaPlayer()
    mediaplayer.setAudioStreamType(AudioManager.STREAM_MUSIC);
    mediaplayer.setDataSource(pathfile)
    mediaplayer.prepare()
    #sound = SoundLoader.load('MTP.mp3')
    def updateTime(self, nap):
        if self.sw_Istarted:
            self.sw_s -= nap
        if self.sw_s < 0 :
            self.root.ids.stopwatch.text = self.mediaplayer
            if self.sound :
                #self.sound.play()
                self.mediaplayer.start()
                self.sw_s = 0
                
        hours, minutes = divmod(self.sw_s, 3600)
        minutes, seconds = divmod(minutes, 60)
        part_s = seconds* 100%100
   
        self.root.ids.stopwatch.text = f'{int(hours)}:{int(minutes):02}:{int(seconds):02}:{int(part_s):02}'
        self.root.ids.time.text = strftime('[b]%H[/b]:%M:%S')
    
    def on_start(self):
        print('start')
        Clock.schedule_interval(self.updateTime, 0)
    
    def start_stop(self):
        if not self.sw_Istarted and self.sw_s==0:
            try:
                H = int(self.root.ids.total_H.text)*3600 
            except:
                H = 0
            try:
                M = int(self.root.ids.total_M.text)*60 
            except:
                M = 0
            try:
                S = int(self.root.ids.total_S.text)
            except:
                S  = 0


            total = H + M + S
            self.sw_s = total
        self.root.ids.start_stop.text = 'Start' if self.sw_Istarted else 'Stop'

        self.sw_Istarted = not self.sw_Istarted
         
        if not self.sw_Istarted :
 #           self.sw_Istarted = False
            self.sound.stop()
 #       else :
 #           if self.sw_s< 0 : 
 #               self.sound.play()   
    
    def reset(self):
        if self.sw_Istarted:
            self.root.ids.start_stop.text = 'Start'
            self.sw_Istarted = False
        self.sw_s = 0
        self.sound.stop()
        
if __name__ == '__main__':
    StopWatchApp().run()

