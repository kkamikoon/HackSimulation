import pygame
import time, sys, os

from pygame.locals import *

import display, prompt, musicplayer, effectplayer

class Main():
    def __init__(self):
        
        # Set pygame elements =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        pygame.init()
        pygame.display.set_caption('kkamikoon game')    # set caption name.

        self.FPS                = 30
        self.MapImg             = pygame.image.load('.\\Game Image\\Maps\\GameBackgroundImg05_939_900.jpg')
        self.MapImgWH           = (self.MapImg.get_width(), self.MapImg.get_height())
                                  # self.MapImgWH[0] = width
                                  # self.MapImgWH[0] = height
        self.FPSCLOCK           = pygame.time.Clock()
        self.DISPLAYSURF        = pygame.display.set_mode(self.MapImgWH, pygame.DOUBLEBUF, 32)
        self.FONT               = pygame.font.Font('Quark-Bold.otf', 15)

        self.Flag               = [True, False]
    
        self.DrawLineX          = 0
        self.DrawLineY          = 0

        # Set Classes =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.Prompt             = prompt.Prompt('70', '56', self.Flag)
        self.Music              = musicplayer.MusicPlayer()
        self.Effect             = effectplayer.EffectPlayer()

        self.DisplayDraw        = display.Draw()
        self.DisplayText        = display.Text()
        self.DisplayDraw.SetDisplaySurface(self.DISPLAYSURF)
        self.DisplayText.SetDisplaySurface(self.DISPLAYSURF)

        self.Prompt.SetDisplaySurface(self.DISPLAYSURF)

        # Music and Prompt Thread Start =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.Music.start()
        self.Prompt.start()
       


    def mainRun(self):
        '''
        MissionClear    : Clear status of Mission.
        '''
        Run             = True
        MissionClear    = False
        MissionSet      = False
        MissionPos      = []
        DomainScanStat  = []
        MouseClicked    = False
        ClickedPos      = ()
        ClickedDomain   = ''
        DrawLineDone    = False

        

        '''
        self.Effect.setEffect('SYSTEMSTARTINGUP')
        self.Effect.play(None)
        '''
        while Run:     # main game loop
            padX = 50
            padY = 120

            # Display Graphic and Level =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            self.DISPLAYSURF.blit(self.MapImg, (0, 0))  # Display Map Image.
            
            if MissionClear == False:                   # Display Level if it is not cleared.
                self.Prompt.Level.LevelSetup()
            else:
                pass # Mission Clear Message Box Up!

            if MissionSet   == False:
                MissionSet  = True
                for Domain in self.Prompt.Level.currentKeys:
                    MissionPos.append(self.Prompt.Level.currentLoadedDomainInfo[Domain][1])
                    DomainScanStat.append(self.Prompt.Level.currentCanLoadDomain[Domain])
                    

            # Event Check and Activate=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            for event in pygame.event.get():    # event handling loop
                if event.type == pygame.QUIT:
                    pass

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    posX, posY   = event.pos
                    MouseClicked = False
                    DrawLineDone = False
                    self.DrawLineX = 0
                    self.DrawLineY = 0

                    for Domain in self.Prompt.Level.currentKeys:
                        if self.Prompt.Level.currentCanLoadDomain[Domain] == True:
                            if ((posX - self.Prompt.Level.currentLoadedDomainInfo[Domain][1][0] < 5)  and
                                (posX - self.Prompt.Level.currentLoadedDomainInfo[Domain][1][0] > -5) and
                                (posY - self.Prompt.Level.currentLoadedDomainInfo[Domain][1][1] < 5)  and
                                (posY - self.Prompt.Level.currentLoadedDomainInfo[Domain][1][1] > -5) ):

                                self.DisplayDraw.TransparentLen = 0
                                MouseClicked    = True
                                ClickedPos      = self.Prompt.Level.currentLoadedDomainInfo[Domain][1]
                                ClickedDomain   = Domain
               

            # If MouseClicked ==> Clicked correct Position of Domain=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            #                     and If The Domain Scan Status is True, The Scan Data will Printed.
            if MouseClicked == True:
                if ClickedPos[0] > 500:
                    padX = 320

                self.DisplayDraw.DrawLine(  ClickedPos,
                                            (ClickedPos[0]-self.DrawLineX, ClickedPos[1]-self.DrawLineY),
                                            self.DisplayDraw.DARKGREEN)

                if DrawLineDone == False:
                    self.DrawLineX += (padX / 10)
                    self.DrawLineY += (padY - 100) / 10

                    if self.DrawLineX >= padX:
                        DrawLineDone = True

                else:
                    self.DisplayDraw.DrawDomainInfo(self.FONT,
                                                    (ClickedPos[0]-padX, ClickedPos[1]-padY),
                                                    self.Prompt.Level.currentLoadedDomainInfo)

                    if self.DisplayDraw.TransparentLen >= 300:
                        for i in range(6):
                            if i != 1 and i != 2 and i != 5:
                                self.DisplayText.makeText(  self.FONT,
                                                            self.Prompt.Level.SystemMonitorDomainInfo[i],
                                                            True,
                                                            pygame.Color('WHITE'),
                                                            (ClickedPos[0]-padX, ClickedPos[1]-padY),
                                                            True
                                                            )
                                if i == 3:
                                    Data = '$' + format(self.Prompt.Level.currentLoadedDomainInfo[ClickedDomain][i], ",")
                                else:
                                    Data = str(self.Prompt.Level.currentLoadedDomainInfo[ClickedDomain][i])

                                self.DisplayText.makeText(  self.FONT,
                                                            ':  ' + Data,
                                                            True,
                                                            pygame.Color('WHITE'),
                                                            (ClickedPos[0]-padX+130, ClickedPos[1]-padY),
                                                            True)
                                padY -= 20

                        for i in range(2):
                            self.DisplayText.makeText(      self.FONT,
                                                            self.Prompt.Level.SystemMonitorSecurityInfo[i],
                                                            True,
                                                            pygame.Color('WHITE'),
                                                            (ClickedPos[0]-padX, ClickedPos[1]-padY),
                                                            True
                                                            )

                            if i == 0:
                                Data = str(self.Prompt.Level.currentLevelCrackStatus[ClickedDomain][i]) + '  bits'
                            else:
                                Data = str(self.Prompt.Level.currentLevelCrackStatus[ClickedDomain][i]) + '  characters'

                            self.DisplayText.makeText(      self.FONT,
                                                            ':  ' + Data,
                                                            True,
                                                            pygame.Color('WHITE'),
                                                            (ClickedPos[0]-padX+130, ClickedPos[1]-padY),
                                                            True
                                                            )
                            padY -= 20
            
                '''
                self.DisplayText.makeText(  self.FONT,
                                            'hahaha',
                                            True,
                                            pygame.Color('WHITE'),
                                            ClickedPos,
                                            False)                                    
                '''
            pygame.display.flip()
            self.FPSCLOCK.tick(self.FPS)




if __name__ == "__main__":
    main = Main()
    main.mainRun()


