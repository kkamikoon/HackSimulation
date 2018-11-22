import pygame
import time
from effectplayer import EffectPlayer
from display import Text, Draw

class Level:
    def __init__(self, Level, Meta):
        '''
        self.levelStatus : Status of completion of level. if complete mission, it will change into True.
        '''

        self.currentLevel   = 0
        self.savedLevel     = Level
        self.currentEquip   = Meta
        self.startTime      = time.time()
        '''
        self.Flags      : Flags for playing game.
        -------------------------------------------------------------
                          [Prompt Alive Flag]   = True
                          [Level Clear Flag]    = False
                          []
        '''
        self.FONT           = pygame.font.Font('Quark-Bold.otf', 16)

        # Set Classes =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.DisplayDraw    = Draw()
        self.DisplayText    = Text()
        self.Load           = Load()
        self.Effects        = EffectPlayer()

        # Metadata of each levels =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.currentEquipLevels             = {}
        self.currentCanLoadDomain           = {}        # Domain can Load in each of levels
        self.currentLoadedDomainInfo        = {}        # Domain Informations of each of Domains
        self.currentLoadedDomainFiles       = {}        # Domain Files of each of Domains
        self.currentLevelCrackStatus        = {}        # Domain Crack and Decrypt Status of each of levels
        self.currentKeys                    = []        # 
        self.currentConnectPos              = []        # Position of line [ [from(x,y), to(x,y)], [from(x,y), to(x,y)] ]
        self.setTarget                      = False
        self.setProcess                     = False
        self.staticProcessCount             = 0.0       # Processing will act. when staticProcessCount is upper then 1.
        self.ProcessingWidth                = 0
        self.ProcessingTime                 = 0.0
        self.ProcessType                    = ''
        self.ProcessHost                    = ''
        self.ProcessFile                    = ''
        self.ProcessStatus                  = ''
        self.Traced                         = False
        self.TracingTime                    = 0.0
        self.TracingTimeLimit               = 0
        self.TracingPos                     = None
        self.TracingLength                  = 0
        self.TracingWidth                   = 0
        self.TracingLengthPer               = 0
        self.TracingWidthPer                = 0
        self.TracingCase                    = 0
        self.GameFlag                       = False
        self.SystemMonitorDomainInfo        = [ 'Domain Name',
                                                'Pos',                  # Doesn't print
                                                'PosText',              # Doesn't print
                                                'Money',
                                                'Number of Files',
                                                'Status']               # Doesn't print
        self.SystemMonitorSecurityInfo      = [ 'Encryption key',
                                                'Password Length']

        # Metadata localhost=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.currentPWD                     = 'localhost'
        self.staticCount                    = 10
        self.countReverse                   = False
        
        # Set Metadata of Equipments=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        


    def SetDisplaySurface(self, Screen):
        self.DisplayDraw.SetDisplaySurface(Screen)
        self.DisplayText.SetDisplaySurface(Screen)


    def Tutorial(self):
        '''
        
        '''
        # Draw the domain if loadStatus is True =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        count       = 0
        FileExist1  = False
        FileExist2  = False

        for i, loadStatus in enumerate(self.currentCanLoadDomain.values()):
            if loadStatus == True:
                if self.currentLevelCrackStatus[self.currentKeys[i]][0] == 0 and self.currentLevelCrackStatus[self.currentKeys[i]][1] == 0:
                    DomainColor = pygame.Color('LIGHTGREEN')
                else:
                    DomainColor = pygame.Color('WHITE')
                # Draw Center Point
                self.DisplayDraw.DrawPoint(self.currentLoadedDomainInfo[self.currentKeys[i]][1],  # Domain Center Point Position
                                           self.currentLoadedDomainInfo[self.currentKeys[i]][5])  # Domain Status
                # Draw Text
                self.DisplayText.makeText( self.FONT,                                             # Font
                                           self.currentLoadedDomainInfo[self.currentKeys[i]][0],  # Domain String.
                                           True,                                                  # Anti-Aliasing
                                           DomainColor,                                           # WHITE Color
                                           self.currentLoadedDomainInfo[self.currentKeys[i]][2],  # Domain Text Position
                                           True)                                                  # Shadow Print True.
            count += 1

        # if hacker deleted [users.db], it is False ------------------------------------------------
        for FileName in self.currentLoadedDomainFiles['www.paradox.com']:
            if FileName == 'contract.docx':
                FileExist1 = True

        # if hacker downloaded [contract.docx], it is True -----------------------------------------
        for FileName in self.currentLoadedDomainFiles['localhost']:
            if FileName == 'users.db':
                FileExist2 = True

        #if FileExist1 == False and FileExist2 == True:
        #    self.LevelClear(1)

        #if FileExist2 == False:
        #    self.LevelFailed()

        


    def TutorialTargetSet(self):
        # Default Domain Status =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        canLoadDomain       = { 'localhost'             : True,
                                'atm.secumaster.net'    : False,
                                'atm.design.net'        : False,
                                'www.design.com'        : False,
                                'www.paradox.com'       : False,
                                'www.tutorial.com'      : True
                            }

        loadedDomainInfo    = { 'localhost'             : [],
                                'atm.secumaster.net'    : [],
                                'atm.design.net'        : [],
                                'www.design.com'        : [],
                                'www.paradox.com'       : [],
                                'www.tutorial.com'      : []
                            }

        loadedDomainFiles   = { 'localhost'             : {},
                                'atm.secumaster.net'    : {},
                                'atm.design.net'        : {},
                                'www.design.com'        : {},
                                'www.paradox.com'       : {},
                                'www.tutorial.com'      : {}
                            }

        levelCrackStatus    = { 'localhost'             : [2048, 16],
                                'atm.secumaster.net'    : [ 256,  4],
                                'atm.design.net'        : [4096,  8],
                                'www.design.com'        : [1024, 32],
                                'www.paradox.com'       : [ 0,  0],
                                'www.tutorial.com'      : [ 0,  0]
                            }
        '''
        [Crack Status, Crack Length, Decrypt Status, Password Length]
        Crack           ==> Cracking System.
        Crack Length    ==> Length of Cracking System(like hash, RSA, DSA)
        Decrypt         ==> Decrypt Password of target.
        Password Length ==> Length of Target's password.(like cipher, AES, DES)
        '''

        canLoadDomainKeys   = list(canLoadDomain)       # Keys of canLoadDomain

        # Load Default Domain Status and each of filesystem =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        for Domain in canLoadDomain:
            loadedDomainInfo[Domain], loadedDomainFiles[Domain] = self.Load.loadDomain(Domain)
        

        # Set metadata of this level=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.currentCanLoadDomain           = canLoadDomain
        self.currentLoadedDomainInfo        = loadedDomainInfo
        self.currentLoadedDomainFiles       = loadedDomainFiles
        self.currentLevelCrackStatus        = levelCrackStatus
        self.currentKeys                    = canLoadDomainKeys


        # Set Localhost and Target=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.currentLoadedDomainInfo['localhost'][5]       = self.DisplayDraw.LOCAL   # localhost
        self.currentLoadedDomainInfo['www.paradox.com'][5] = self.DisplayDraw.TARGET  # target

        #self.currentEquip = tutorialEquip   = 0x02240202
        self.currentEquip = tutorialEquip   = 0x08888888
        self.DisplayDraw.SetEquipStatus(self.currentEquip)

        # Set Localhost money for tutorial mission=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.currentLoadedDomainInfo['localhost'][3]       = 100000



    def LevelOne(self):
        '''
        :param EquipMetaData:   Metadata if Equipment.

        '''
        #



    def LevelTwo(self):
        print("level02")



    def LevelSetup(self):
        # If mission target and mission information is not set up ----------------------------------
        if self.setTarget == False:
            self.setTarget = True

            if self.currentLevel == 0:
                self.TutorialTargetSet()
            elif self.currentLevel == 1:
                pass

        # Printing mission -------------------------------------------------------------------------

        if self.currentLevel == 0:
            self.Tutorial()
        elif self.currentLevel == 1:
            self.LevelOne()
        elif self.currentLevel == 2:
            self.LevelTwo()

        if self.GameFlag == True:
            self.DisplayDraw.DrawGameOver()

        # Draw Equipments =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.DisplayDraw.DrawEquipment()       

        # Draw Processing =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        if self.setProcess == True:
            self.Processing()
            self.Tracing()

        # Draw System Monitor =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.PrintTargetMessage()
        self.PrintSystemMonitor()

        # Printing motion ---------------------------------------------------------------------------
        self.GraphicMotions()


    def GraphicMotions(self):
        self.DisplayDraw.DrawTransparent((self.staticCount, 497), self.DisplayDraw.GREEN, 22, 10)

        if self.countReverse == True:
            self.staticCount -= 4
            if self.staticCount <= 14:
                self.countReverse = False
        else:
            self.staticCount += 4
            if self.staticCount >= 874:
                self.countReverse = True

        if self.currentPWD != 'localhost':
            for Pos in self.currentConnectPos:
                self.DisplayDraw.DrawLine(Pos[0], Pos[1], self.DisplayDraw.DARKCYAN)



    def Processing(self):
        # Draw process bar if Process status is True=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        #time.sleep(self.ProcessingTime)
        self.staticProcessCount += self.ProcessingTime

        # Processing Activation --------------------------------------------------------------------
        
        if self.staticProcessCount >= 1:
            self.staticProcessCount = 0

            # - If Quantom CPU or not

            if self.ProcessingTime > 50:
                self.ProcessingWidth += 30.9
            else:
                self.ProcessingWidth += 3
        

        # - Processing Complete
        if self.ProcessingWidth >= 310:     # If Process complete
            self.ProcessingWidth = 0
            self.setProcess = False

            self.Effects.setEffect('COMPLETE')
            self.Effects.play(None)


        # - Changing cracking status
            if self.ProcessType == 'decrypt':
                self.currentLevelCrackStatus[self.ProcessHost][0] = 0
                
            elif self.ProcessType == 'crack':
                self.currentLevelCrackStatus[self.ProcessHost][1] = 0

            elif self.ProcessType == 'download':
                try:
                    del self.currentLoadedDomainFiles['localhost'][self.ProcessFile]
                    self.currentLoadedDomainFiles['localhost'][self.ProcessFile] = self.currentLoadedDomainFiles[self.currentPWD][self.ProcessFile]
                    self.currentLoadedDomainInfo['localhost'][4]                 = len(self.currentLoadedDomainFiles['localhost'])
                except KeyError:
                    self.currentLoadedDomainFiles['localhost'][self.ProcessFile] = self.currentLoadedDomainFiles[self.currentPWD][self.ProcessFile]
                    self.currentLoadedDomainInfo['localhost'][4]                 = len(self.currentLoadedDomainFiles['localhost'])
            
            elif self.ProcessType == 'upload':
                try:
                    del self.currentLoadedDomainFiles[self.currentPWD][self.ProcessFile]
                    self.currentLoadedDomainFiles[self.currentPWD][self.ProcessFile] = self.currentLoadedDomainFiles['localhost'][self.ProcessFile]
                    self.currentLoadedDomainInfo[self.currentPWD][4]                 = len(self.currentLoadedDomainFiles[self.currentPWD])
                except IndexError:
                    self.currentLoadedDomainFiles[self.currentPWD][self.ProcessFile] = self.currentLoadedDomainFiles['localhost'][self.ProcessFile]
                    self.currentLoadedDomainInfo[self.currentPWD][4]                 = len(self.currentLoadedDomainFiles[self.currentPWD])
            
            elif self.ProcessType == 'transfer':
                self.currentLoadedDomainInfo['localhost'][3]      += self.ProcessMoney
                self.currentLoadedDomainInfo[self.currentPWD][3]  -= self.ProcessMoney


        # Processing abort -------------------------------------------------------------------------
        # - Processing Abort
        elif self.ProcessingWidth < 0:
            self.ProcessingWidth = 0
            self.setProcess = False


        # Print Processing Bar ---------------------------------------------------------------------
        self.DisplayDraw.DrawProcessBar(self.ProcessingWidth)
        self.DisplayDraw.DrawLine(self.currentLoadedDomainInfo[self.currentPWD][1], self.currentLoadedDomainInfo[self.ProcessHost][1], self.DisplayDraw.BROWN)

        if self.ProcessType == 'crack' or self.ProcessType == 'decrypt':
            self.DisplayText.makeText(self.FONT,
                                      self.ProcessType + ' : ' + self.ProcessHost,
                                      True,
                                      pygame.Color('WHITE'),
                                      (510,852),
                                      True)
        elif self.ProcessType == 'download' or self.ProcessType == 'upload':
            self.DisplayText.makeText(self.FONT,
                                      self.ProcessType + ' : ' + self.ProcessFile,
                                      True,
                                      pygame.Color('WHITE'),
                                      (510,852),
                                      True)
        elif self.ProcessType == 'transfer':
            self.DisplayText.makeText(self.FONT,
                                      self.ProcessType + ' : ' + str(self.ProcessMoney),
                                      True,
                                      pygame.Color('WHITE'),
                                      (510,852),
                                      True)


    def ProcessingTimeSet(self, procType, host, money=0, filename=''):
        '''
        :param procType:    Process Type.
        :param host:        Host to activate processing.
        :param money:       Money to transfer.
        :param filename:    File name to download or upload

        Time        = Total Value of process / ( FPS * Total EquipLevels * Overhead )
        Overhead    = Calculation Time Adjustment value

        :comment:
        There is too many processes to execute 'self.Processing'...
        So, i added a little calculation that different of cracking has arithmetic operation.
        It means, each of diffenrecy has pow() calculation function.

        ex > differency :     512 ==>  512 ^ 2 == 65536
             differency :    4096 ==> 4096 ^ 2 == 16777216

        Then all of differency has evident time lag..!!


        Time Val  ==> low value is SLOW!!
        '''
        # Set processing time =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        self.ProcessType = procType     # string
        self.ProcessHost = host         # string
        self.ProcessFile = filename     # string
        self.ProcessMoney= money        # int

        Overhead = 2

        if procType == 'decrypt':
            # Cracking Encryption Key.
            # Using Size of Encryption bit.
            equipLevel          = self.GetCurrentEquipLevel('CPU')
            self.ProcessingTime = ( 30 * equipLevel * Overhead ) / self.currentLevelCrackStatus[host][0]
                                
        elif procType == 'crack':
            # Cracking Password System.
            # Using number of characters.
            equipLevel          = self.GetCurrentEquipLevel('CPU')
            self.ProcessingTime = ( 30 * equipLevel * Overhead ) / (self.currentLevelCrackStatus[host][1] * 128)
                                
        elif procType == 'download':
            # Downloading File from Target System.
            # Using Size of File stored in Target Domain.
            equipLevel          = self.GetCurrentEquipLevel('MODEM')
            self.ProcessingTime = ( 30 * equipLevel * Overhead ) / int(self.currentLoadedDomainFiles[host][self.ProcessFile][1]) * 10
                                
        elif procType == 'upload':
            # Uploading File from Localhost to Target System.
            # Using Size of File stored in localhost.
            equipLevel          = self.GetCurrentEquipLevel('MODEM')
            self.ProcessingTime = ( 30 * equipLevel * Overhead ) / int(self.currentLoadedDomainFiles[host][self.ProcessFile][1]) * 10
                                
        elif procType == 'transfer':
            # Transfer Money to Localhost from Target System.
            # Using Money of Domain.
            equipLevel          = self.GetCurrentEquipLevel('MODEM')
            self.ProcessingTime = ( 30 * equipLevel * Overhead ) / money * 10
                                


    def TracingTimeSet(self):
        '''

        :comment:
        There is too many processes to execute 'self.Processing'...
        And there processing can be traced by.
        The tracing time depend on number of hosts.
        '''

        Time        = 24
        numOfHosts  = len(self.currentConnectPos) + 1
        equipLevel  = self.GetCurrentEquipLevel('FIREWALL')

        # Tracing Time Setting ---------------------------------------------------------------------
        self.TracingTimeLimit   = Time * numOfHosts * equipLevel
        self.TracingTime        = 0.0334 / (self.TracingTimeLimit * 30)
        

        # Calculating Position and Length, Width ---------------------------------------------------
        PosFrom     = self.currentLoadedDomainInfo['localhost'][1]          # Localhost Position
        PosTo       = self.currentLoadedDomainInfo[self.ProcessHost][1]     # Target Position

        PosFromList = list(PosFrom)
        PosToList   = list(PosTo)
        
        if PosFromList[0] > PosToList[0]:
            PosXL   = PosToList[0]      # Position X Left
            PosXR   = PosFromList[0]    # Position X Right
        else:
            PosXL   = PosFromList[0]
            PosXR   = PosToList[0]

        if PosFromList[1] > PosToList[1]:
            PosYT   = PosToList[1]      # Position Y Top
            PosYB   = PosFromList[1]    # Position Y Bottom
        else:
            PosYT   = PosFromList[1]
            PosYB   = PosToList[1]


        # Tracing Case Setting ---------------------------------------------------------------------
        if PosFromList[0] < PosToList[0]   and PosFromList[1] < PosToList[1]:
            self.TracingCase = 1

        elif PosFromList[0] < PosToList[0] and PosFromList[1] > PosToList[1]:
            self.TracingCase = 2

        elif PosFromList[0] > PosToList[0] and PosFromList[1] < PosToList[1]:
            self.TracingCase = 3

        elif PosFromList[0] > PosToList[0] and PosFromList[1] > PosToList[1]:
            self.TracingCase = 4


        # Tracing Values Setting -------------------------------------------------------------------
        self.TracingPos         = (PosXL, PosYT)    # Position of Rectangle

        self.TracingLength      = PosXR - PosXL     # Rectangle Length
        self.TracingWidth       = PosYB - PosYT     # Rectangle Width

        self.TracingLengthPer   = self.TracingLength / (self.TracingTimeLimit * 30)  # Length for decreasing per second
        self.TracingWidthPer    = self.TracingWidth  / (self.TracingTimeLimit * 30)  # Wdith  for decreasing per second
        


    def Tracing(self):
        # DrawTransparent ==> (Position, Color, Length, Width)
        self.DisplayDraw.DrawTransparent(   self.TracingPos,        # Postion of Rectangle
                                            self.DisplayDraw.BROWN, # Color   of Rectangle
                                            self.TracingLength,     # Length  of Rectangle
                                            self.TracingWidth,      # Width   of Rectangle
                                            50)                     # Alpha
        self.DisplayDraw.DrawLine(          self.currentLoadedDomainInfo[self.ProcessHost][1],
                                            self.TracingPos,
                                            self.DisplayDraw.RED)
        if self.TracingCase == 1:
            self.TracingLength -= self.TracingLengthPer
            self.TracingWidth  -= self.TracingWidthPer

        elif self.TracingCase == 2:
            PosList = list(self.TracingPos)
            PosList[1] += self.TracingWidthPer          # increase Y
            self.TracingPos     = tuple(PosList)
            self.TracingLength -= self.TracingLengthPer
            self.TracingWidth  -= self.TracingWidthPer            
        
        elif self.TracingCase == 3:
            PosList     = list(self.TracingPos)
            PosList[0] += self.TracingLengthPer         # increase X
            self.TracingPos     = tuple(PosList)

            self.TracingLength -= self.TracingLengthPer
            self.TracingWidth  -= self.TracingWidthPer

        elif self.TracingCase == 4:
            PosList = list(self.TracingPos)
            PosList[0] += self.TracingLengthPer         # increase X
            PosList[1] += self.TracingWidthPer          # increase Y

            self.TracingPos     = tuple(PosList)
            self.TracingLength -= self.TracingLengthPer
            self.TracingWidth  -= self.TracingWidthPer

        if self.TracingLength <= 0:
            self.setProcess = False
            self.GameFlag   = True



    def GetCurrentEquipLevel(self, equipType):
        if equipType == 'CPU':
            if self.DisplayDraw.EquipLevels[3] >= 4 or self.DisplayDraw.EquipLevels[4] >= 4:
                return 100000
            else:
                return self.DisplayDraw.EquipLevels[3] + self.DisplayDraw.EquipLevels[4]

        elif equipType == 'MODEM':
            return pow(self.DisplayDraw.EquipLevels[5], 2)

        elif equipType == 'FIREWALL':
            return self.DisplayDraw.EquipLevels[6]



    def PrintSystemMonitor(self):
        '''
        
        '''
        x       = 500
        y       = 555
        Data    = ''

        # Print Localhost Domain Info --------------------------------------------------------------
        for i in range(6):
            if i != 1 and i != 2 and i != 5:
                self.DisplayText.makeText(  self.FONT,
                                            self.SystemMonitorDomainInfo[i],
                                            True,
                                            pygame.Color('BLACK'),
                                            (x, y),
                                            False
                                            )

                if i == 3:
                    Data = '$' + format(self.currentLoadedDomainInfo['localhost'][i], ",")
                else:
                    Data = str(self.currentLoadedDomainInfo['localhost'][i])

                self.DisplayText.makeText(  self.FONT,
                                            ':  ' + Data,
                                            True,
                                            pygame.Color('BLACK'),
                                            (x+130, y),
                                            False
                                            )
                y += 20

        for i in range(2):
            self.DisplayText.makeText(      self.FONT,
                                            self.SystemMonitorSecurityInfo[i],
                                            True,
                                            pygame.Color('BLACK'),
                                            (x, y),
                                            False
                                            )

            if i == 0:
                Data = str(self.currentLevelCrackStatus['localhost'][i]) + '  bits'
            else:
                Data = str(self.currentLevelCrackStatus['localhost'][i]) + '  characters'

            self.DisplayText.makeText(      self.FONT,
                                            ':  ' + Data,
                                            True,
                                            pygame.Color('BLACK'),
                                            (x+130, y),
                                            False
                                            )
            y += 20

        # print system time ------------------------------------------------------------------------
        now  = time.time() - self.startTime
        Data = '%02d : %02d : %.01f' % (now / 3600, now / 60, now % 60)

        self.DisplayText.makeText(  self.FONT,
                                    Data,
                                    True,
                                    pygame.Color('WHITE'),
                                    (810, 470),
                                    False
                                    )



    def PrintTargetMessage(self):
        '''

        '''
        TargetMessage = self.returnTargetMessage(self.currentLevel)

        self.PrintMessage(TargetMessage)



    def PrintMessage(self, Msg):
        '''
        :param Msg:         Message to Print.
                            Message Type is list.
        :param Len:         Length of Message(number of lines)

        '''
        x = 35
        y = 555

        for M in Msg:
            self.DisplayText.makeText(self.FONT,
                                      M,
                                      True,
                                      pygame.Color('BLACK'),
                                      (x, y),
                                      False)
            y += 20


    def returnTargetMessage(self, Level):
        '''
        :param Level:       Flag of Target Level.

        1 line ==> 56 characters
        '''

        Level00 = ['Targets : \"www . paradox . com\"',
                   'Mission :  Download user database and delete contract.docx.',
                   '- Download \"users . db\"',
                   '- Delete \"contract . docx\"']
        Level01 = ['Target  : Korea(South) - [Company - Nexon<DB Server>]',
                   'Mission : Confirm that Nexon has \"customer\'s User Data\"',
                   '- find <User Data File> in Nexon Database Server.',
                   '- \"User Data File : \'userdata.db\'']
        Level02 = []
        Level03 = []
        Level04 = []
        Level05 = []
        Level06 = []
        Level07 = []
        Level08 = []
        Level09 = []

        LevelList      = [Level00, Level01, Level02, Level03, Level04,
                          Level05, Level06, Level07, Level08, Level09]

        return LevelList[Level]


    def LevelClear(self, nextLV):
        '''
        :param nextLV:      Next Level Value(Integer)

        '''
        print('LevelClear!!')
        print('Next Level : %d' % nextLV)
        input('press any key')


    def LevelFailed(self):
        print('Level Failed..')


    def GetCurrentLevel(self):
        return self.currentLevel


    def SetCurrentLevel(self, Level):
        '''
        :param Level:       Level data that is choosen from user.
        '''
        self.currentLevel = Level


    #def GetCurrentMissionPos(self):
    #    for Info in self.currentLoadedDomainInfo:


    def PrintGameOver(self):
        
        """
        #Print GameOver Message --------------------------------------------------------------------
        Length      = 739
        Width       = 500
        Position    = [100, 200]
        #((939/2)-Length, (900/2)-Width)
        self.DisplayDraw.DrawTransparent(   (Position[0], Position[1]),
                                            self.DisplayDraw.BLACK,
                                            Length,
                                            Width,
                                            150)

        Length -= 50
        Width  -= 50
        Position[0] += 25
        Position[1] += 25
        self.DisplayDraw.DrawTransparent(   (Position[0], Position[1]),
                                            self.DisplayDraw.DARKGREEN,
                                            Length,
                                            Width,
                                            75
                                            )

        Length -= 50
        Width  -= 50
        Position[0] += 25
        Position[1] += 25
        self.DisplayText.makeText(          pygame.font.Font('Quark-Bold.otf', 16),
                                            'Game Over',
                                            True,
                                            pygame.Color('BLACK'),
                                            (Position[0], Position[1]),
                                            False)
        """
        pass

# Load Data that we read=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class Load:
    def __init__(self):
        self.Dir        = 'MetaData\\'
        self.InfoLen    = [    30,     4,     4,     4,     4,    1]
        self.FileLen    = [   256,    19,     4, 10240]


    def loadDomain(self, domain):
        domainData      = b''
        domainInfo      = []
        domainFiles     = []
        domainFileName  = ''
        domainFileDict  = {}

        offset          = 0

        with open(self.Dir + domain + '.meta', 'rb') as rFile:
            domainData = rFile.read()

        for HL in self.InfoLen:
            domainInfo.append(domainData[ offset : offset+HL ])
            offset += HL

        '''
        domainInfo      = [ Domain      (30 Bytes),     # String
                            Position    ( 4 Bytes),     # Tuple
                            PositionTxt ( 4 Bytes),     # Tuple
                            Money       ( 4 Bytes),     # Int
                            NumOfFiles  ( 4 Bytes),     # Int
                            Status      ( 1 Bytes)      # Int ]
        '''

        numOfFiles      = int.from_bytes(domainInfo[4], byteorder='big', signed=True) 


        for Num in range(numOfFiles):
            domainFileInfo  = []

            for FL in self.FileLen:
                tmp     = domainData[ offset : offset+FL ]
                count   = 0
                offset += FL

                if FL == 256:               # For FileName
                    for B in tmp:
                        if B == 0x20:
                            count += 1
                        else:
                            break
                    domainFileName = tmp[count:].decode()
                    #print('domain : ', domain, '   tmp : ', tmp, '  domainNode : ', domainNode, '  status : ', domainInfo[5])
                else:
                    domainFileInfo.append(tmp)

            domainFileDict[domainFileName] = domainFileInfo

        '''
        domainFileDict  = { FileName    :   Each of Files,
                            FileName    :   Each of Files,
                                             FileName,      ( 256 Bytes)    # Sting

                            FileName    :   [Date,          (  19 Bytes)    # String
                                             Size,          (   4 Bytes)    # String
                                             FileData]      (1024 Bytes)    # String
                            ...
                           }
        '''

        self.unPadInfo(domainInfo)
        self.unPadFiles(domainFileDict)

        return domainInfo, domainFileDict



    def unPadInfo(self, Info):
        posX,   posY    = Info[1][:2], Info[1][2:]
        posTX,  posTY   = Info[2][:2], Info[2][2:]

        count = 0

        for i in range(len(Info[0])):
            if Info[0][i] == 0x20:
                count += 1
            else:
                break

        Info[0]     = Info[0][count:].decode()       # bytes to string
        Info[1]     = (int.from_bytes(    posX, byteorder='big', signed=True),
                       int.from_bytes(    posY, byteorder='big', signed=True))
        Info[2]     = (int.from_bytes(   posTX, byteorder='big', signed=True),
                       int.from_bytes(   posTY, byteorder='big', signed=True))
        Info[3]     =  int.from_bytes( Info[3], byteorder='big', signed=True)
        Info[4]     =  int.from_bytes( Info[4], byteorder='big', signed=True)
        Info[5]     =  int.from_bytes( Info[5], byteorder='big', signed=True)



    def unPadFiles(self, FileDict):
        count       = [0, 0, 0]

        # File  : Name of File.

        for File in FileDict:                               # number of files
            for i in range(len(FileDict[File])):            # Information of file( 3 times )
                for j in range(len(FileDict[File][i])):     # length of each file data
                    if FileDict[File][i][j] == 0x20:
                        count[i] += 1
                    else:
                        break
                FileDict[File][i] = FileDict[File][i][count[i]:].decode()
            count       = [0, 0, 0]
                

# Node and BinarySearchTree Class Definition =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class Node(object):
    def __init__(self, data):
        self.data = data
        self.left = self.right = None


class BinarySearchTree(object):
    def __init__(self):
        self.root = None

    # Insert Method =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def insert(self, data):
        self.root = self._insert_value(self.root, data)
        return self.root is not None

    def _insert_value(self, node, data):
        if node is None:
            node = Node(data)
        else:
            if data <= node.data:
                node.left = self._insert_value(node.left, data)
            else:
                node.right = self._insert_value(node.right, data)
        return node

    # Search Method =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def find(self, key):
        return self._find_value(self.root, key)

    def _find_value(self, root, key):
        if root is None or root.data == key:
            return root is not None
        elif key < root.data:
            return self._find_value(root.left, key)
        else:
            return self._find_value(root.right, key)

    # Delete Method =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def delete(self, key):
        self.root, deleted = self._delete_value(self.root, key)
        return deleted

    def _delete_value(self, node, key):
        if node is None:
            return node, False

        deleted = False
        if key == node.data:
            deleted = True
            if node.left and node.right:
                # replace the node to the leftmost of node.right
                parent, child = node, node.right
                while child.left is not None:
                    parent, child = child, child.left
                child.left = node.left
                if parent != node:
                    parent.left = child.right
                    child.right = node.right
                node = child
            elif node.left or node.right:
                node = node.left or node.right
            else:
                node = None
        elif key < node.data:
            node.left, deleted  = self._delete_value(node.left, key)
        else:
            node.right, deleted = self._delete_value(node.right, key)
        return node, deleted