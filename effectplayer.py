'''
Created on 2012. 2. 19.
This module is for playing mp3 (limited) and wav formatted audio file
@author: John
'''
import pygame
import time

class EffectPlayer():
    def __init__(self):
        self.EffectDict     = { 'ANALYZING'         : 'Analyzing.wav',
                                'COMPLETE'          : 'Complete.wav',
                                'DELETED'           : 'Deleted.wav',
                                'ENDATTACK'         : 'EndingAttack.wav',
                                'ERROR'             : 'Error.wav',
                                'GAMEOVER'          : 'GameOver.wav',
                                'LAUNCHATTACK'      : 'LaunchingAttack.wav',
                                'LOADING'           : 'Loading.wav',
                                'PROCESSING'        : 'Processing.wav',
                                'SCANNING'          : 'Scanning.wav',
                                'SYSTEMOFFLINE'     : 'SystemOffline.wav',
                                'SYSTEMONLINE'      : 'SystemOnline.wav',
                                'SYSTEMSECURE'      : 'SystemSecure.wav',
                                'SYSTEMSTARTINGUP'  : 'SystemStartingUp.wav',
                                'UPDATECOMPLETE'    : 'UpdateComplete.wav',
                                'WARNING'           : 'Warning.wav',
                                'WELCOME'           : 'Welcome.wav',
                                }
        self.SelectedEffect = ''
        self.effectAlive    = True


    def play(self, timelimit):
        if timelimit == None:       
            timelimit = 99999

        effect = pygame.mixer.Sound(self.SelectedEffect)
        effect.set_volume(0.3)
        status = effect.play()
        startTime = time.time()

        while status.get_busy():
            pygame.time.delay(50)
            if (time.time() - startTime) >= timelimit:
                status.stop()


    def setEffect(self, effect):
        self.SelectedEffect = 'Effects\\' + self.EffectDict[effect]
