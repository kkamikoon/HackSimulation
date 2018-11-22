'''
Created on 2012. 2. 19.
This module is for playing mp3 (limited) and wav formatted audio file
@author: John
'''
import pygame
import threading

class MusicPlayer(threading.Thread):
    def __init__(self, name='MusicPlayer'):
        self.FileList       = ['Musics\\01.mp3',
                               'Musics\\02.mp3',
                               'Musics\\03.mp3',
                               'Musics\\04.mp3',
                               'Musics\\05.mp3']
        self.threadAlive    = True
        pygame.mixer.music.set_volume(0.05)
        threading.Thread.__init__(self, name=name)

    def playmusic(self, soundfile):
        """Stream music with mixer.music module in blocking manner.
        This will stream the sound from disk while playing.
        """
        pygame.init()
        pygame.mixer.init()
        clock = pygame.time.Clock()
        pygame.mixer.music.load(soundfile)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(1000)
            

    def stopmusic(self):
        """stop currently playing music"""
        pygame.mixer.music.stop()


    def getmixerargs(self):
        pygame.mixer.init()
        freq, size, chan = pygame.mixer.get_init()
        return freq, size, chan


    def initMixer(self):
        BUFFER = 3072  # audio buffer size, number of samples since pygame 1.8.
        FREQ, SIZE, CHAN = self.getmixerargs()
        pygame.mixer.init(FREQ, SIZE, CHAN, BUFFER)


    def run(self):

        while self.threadAlive:
            
            for List in self.FileList:
                try:
                    self.initMixer()
                    self.playmusic(List)
                except KeyboardInterrupt:
                    '''
                    Play Stopped by user.
                    '''
                    self.stopmusic()
                except Exception:
                    '''
                    Unknown Error.
                    '''
                    pass

    