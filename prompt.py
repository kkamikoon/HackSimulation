import ctypes
import os, sys
import threading
import level, effectplayer
import time

class Prompt(threading.Thread):
    def __init__(self, cols, lines, gameflag, name='Prompt'):
        self.DISPLAYSURF        = None

        # Thread Initiating =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        threading.Thread.__init__(self, name=name)
        self.threadAlive        = True

        # Set Classes =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.EquipMetaData      = self.getMeta('MetaData\\_equipmetadata')
        self.LevelMetaData      = self.getMeta('MetaData\\_levelmetadata')

        if self.EquipMetaData == None:
            print('EquipMetaData has Error')
            sys.exit(0)
        elif self.LevelMetaData == None:
            print('LevelMetaData has Error')
            sys.exit(0)

        self.Level              = level.Level(self.LevelMetaData, self.EquipMetaData)
        self.Effects            = effectplayer.EffectPlayer()

        # Set Current Level =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.Level.SetCurrentLevel(self.LevelMetaData)

        # Set prompt elements =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.STD_INPUT_HANDLE   = -10
        self.STD_OUTPUT_HANDLE  = -11
        self.STD_ERROR_HANDLE   = -12
        self.StdOutHandle       = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        
        self.PWD                = '@ ' + self.Level.currentPWD + ' :> '
        self.DomainInfo         = ['Domain Name      - ',
                                   'Pos',                   # Doesn't print
                                   'PosText',               # Doesn't print
                                   'Money            - ',
                                   'Number of Files  - ',
                                   'Status           - ']   # Doesn't print
        self.SecurityInfo       = ['Encryption key   - ',
                                   'Password Length  - ']
        self.GameFlag           = gameflag
        self.EquipNameFlag      = ['FIREWALL', 'MODEM', 'CPU1', 'CPU2', 'RAM1', 'RAM2', 'HDD']
        self.EquipNotExistFlag  = True

        # Foreground Color=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.FG         = {
        'BLACK'         : 0x0000, # text color contains black.
        'BLUE'          : 0x0001, # text color contains blue.
        'GREEN'         : 0x0002, # text color contains green.
        'CYAN'          : 0x0003, # text color contains cyan.
        'RED'           : 0x0004, # text color contains red.
        'MAGENTA'       : 0x0005, # text color contains magenta.
        'YELLOW'        : 0x0006, # text color contains yellow.
        'LIGHTGRAY'     : 0x0007, # text color contains gray.
        'GRAY'          : 0x0008, # text color contains gray.(light)
        'LIGHTBLUE'     : 0x0009, # text color contains blue.(light)
        'LIGHTGREEN'    : 0x000A, # text color contains green.(light)
        'LIGHTCYAN'     : 0x000B, # text color contains cyan.(light)
        'LIGHTRED'      : 0x000C, # text color contains red.(light)
        'LIGHTMAGENTA'  : 0x000D, # text color contains magenta.(light)
        'LIGHTYELLOW'   : 0x000E, # text color contains yellow.(light)
        'WHITE'         : 0x000F  # text color contains white.(light)
        }

        # Background Color=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.BG         = {
        'BLACK'         : 0x0000, # background color contains black.
        'BLUE'          : 0x0010, # background color contains blue.
        'GREEN'         : 0x0020, # background color contains green.
        'CYAN'          : 0x0030, # background color contains cyan.
        'RED'           : 0x0040, # background color contains red.
        'MAGENTA'       : 0x0050, # background color contains magenta.
        'YELLOW'        : 0x0060, # background color contains yellow.
        'LIGHTGRAY'     : 0x0070, # background color contains gray.(light)
        'GRAY'          : 0x0080, # background color contains gray.
        'LIGHTBLUE'     : 0x0090, # background color contains blue.(light)
        'LIGHTGREEN'    : 0x00A0, # background color contains green.(light)
        'LIGHTCYAN'     : 0x00B0, # background color contains cyan.(light)
        'LIGHTRED'      : 0x00C0, # background color contains red.(light)
        'LIGHTMAGENTA'  : 0x00D0, # background color contains magenta.(light)
        'LIGHTYELLOW'   : 0x00E0, # background color contains yellow.(light)
        'WHITE'         : 0x00F0  # background color contains white.(light)
        }
        
        self.setDefault(cols, lines)    # set default console color
        

    def SetDisplaySurface(self, Screen):
        self.DISPLAYSURF = Screen
        self.Level.SetDisplaySurface(self.DISPLAYSURF)


    def getMeta(self, Dir):
        try:
            with open(Dir, 'r') as rMeta:
                strData = rMeta.read()
                intData = int(strData)
            return intData

        except FileNotFoundError:
            with open(Dir, 'w') as wMeta:
                if Dir   == 'MetaData\\_equipmetadata':
                    wMeta.write(str(0x01101001))    # write Default Equipment metadata
                elif Dir == 'MetaData\\_levelmetadata':
                    wMeta.write(str(0))             # write Default Level(Tutorial)

            try:
                with open(Dir, 'r') as rMeta:
                    strData = rMeta.read()
                    intData = int(strData)
                return intData

            except FileNotFoundError:
                return None



    def setStringColor(self, Usage):
        '''
        :param Usage:       Usage of printing.
        '''
        if Usage == 'DEFAULT':
            # BackgroundColor : BLACK,     StringColor : GREEN
            ctypes.windll.kernel32.SetConsoleTextAttribute(self.StdOutHandle, self.BG['BLACK'] or self.FG['GREEN'])

        elif Usage == 'COMMAND':
            # BackgroundColor : BLACK,     StringColor : LIGHTGREEN
            ctypes.windll.kernel32.SetConsoleTextAttribute(self.StdOutHandle, self.BG['BLACK'] or self.FG['LIGHTGREEN'])

        elif Usage == 'CMDRESULT':
            # BackgroundColor : BLACK,     StringColor : YELLOW
            ctypes.windll.kernel32.SetConsoleTextAttribute(self.StdOutHandle, self.BG['BLACK'] or self.FG['YELLOW'])

        elif Usage == 'CONNECT':
            # BackgroundColor : GRAY,     StringColor : YELLOW
            ctypes.windll.kernel32.SetConsoleTextAttribute(self.StdOutHandle, self.BG['GRAY'] or self.FG['YELLOW'])

        elif Usage == 'DOMAININFO':
            # BackgroundColor : BLACK,     StringColor : GRAY
            ctypes.windll.kernel32.SetConsoleTextAttribute(self.StdOutHandle, self.BG['BLACK'] or self.FG['GRAY'])

        elif Usage == 'DOMAINFILES':
            # BackgroundColor : BLACK,     StringColor : LIGHTGRAY
            ctypes.windll.kernel32.SetConsoleTextAttribute(self.StdOutHandle, self.BG['BLACK'] or self.FG['LIGHTGRAY'])

        elif Usage == 'ALERT':
            # BackgroundColor : YELLOW,     StringColor : WHITE
            ctypes.windll.kernel32.SetConsoleTextAttribute(self.StdOutHandle, self.BG['YELLOW'] or self.FG['WHITE'])



    def setDefault(self, cols, lines):
        '''
        'BLACK'       : '0',  'BLUE'        : '1',  'GREEN'       : '2',  'CYAN'        : '3',
        'RED'         : '4',  'PURPLE'      : '5',  'YELLOW'      : '6',  'LIGHTGRAY'   : '7', 
        'GRAY'        : '8',  'LIGHTBLUE'   : '9',  'LIGHTGREEN'  : 'A',  'LIGHTCYAN'   : 'B',
        'LIGHTRED'    : 'C',  'LIGHTPURPLE' : 'D',  'LIGHTYELLOW' : 'E',  'WHITE'       : 'F'
        '''
        os.system('color 02')                               # color setting
        os.system('mode con: cols='+cols+' lines='+lines)   # console size setting



    def parseOption(self):
        '''
        Parsing Option.
    
        :return:        option data(list type)
        '''
        try:
            self.setStringColor('DEFAULT')
            cmd = input(self.PWD)

            cmd = " ".join(cmd.split())     # delete multiple space
            cmd = cmd.split()               # command split into list

            if cmd == []:                   # if you input 'Enter' without any message.
                return ['.']

            return cmd

        except KeyboardInterrupt:
            pass

        except EOFError:
            pass

 

    def run(self):
        '''
        Prompt Main Loop.

        :param GameFlag:        Flag for playing game.
        -------------------------------------------------------------
                                [Prompt Alive Flag]   = True
                                [Level Clear Flag]    = False
                                []                  
        '''

        while self.threadAlive:  # main prompt loop
            '''
            
            '''
            try:
                command = self.parseOption()

                if command[0] == '.':
                    pass

                # Hacker Commands =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                # abort --------------------------------------------------------------------------------
                elif command[0] == 'abort':
                    if self.Level.setProcess == True:
                        self.setStringColor('CMDRESULT')
                        print('Abort', self.Level.ProcessType)

                        self.Level.ProcessingWidth = -10
                        self.setStringColor('DEFAULT')

                        self.Effects.setEffect('ENDATTACK')
                        self.Effects.play(None)
                    else:
                        self.setStringColor('ALERT')
                        print('No process to abort is exist.                                         ')
                        print('Suspend Operation : Abort                                             ')
                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)


                # clear --------------------------------------------------------------------------------
                elif command[0] == 'clear':
                    os.system('cls')

                # config -------------------------------------------------------------------------------
                elif command[0] == 'config':
                    try:
                        self.setStringColor('CMDRESULT')
                        if command[1] == 'current':
                            self.Level.DisplayDraw.getEquipStatus(self.Level.currentEquip)
                            self.Effects.setEffect('COMPLETE')
                            self.Effects.play(None)
                            raise PassCommand

                        elif command[1] == 'help':
                            print('----------------------------------------------------------------------')
                            print('|  EQUIPMENT    |   LEVEL   |   MONEY   |           COMMENT          |')
                            print('----------------------------------------------------------------------')
                            print('|  FIREWALL     |       1   |   1,000   |                            |')
                            print('|  -            |       2   |   2,000   |                            |')
                            print('|  -            |       3   |   4,000   |                            |')
                            print('|  -            |       4   |   8,000   |                            |')
                            print('----------------------------------------------------------------------')
                            print('|  MODEM        |       1   |   2,000   |                            |')
                            print('|  -            |       2   |   4,000   |                            |')
                            print('|  -            |       3   |   8,000   |                            |')
                            print('|  -            |       4   |  16,000   |                            |')
                            print('----------------------------------------------------------------------')
                            print('|  CPU1, CPU2   |       1   |   2,000   |                            |')
                            print('|  -            |       2   |   4,000   |                            |')
                            print('|  -            |       3   |   8,000   |                            |')
                            print('|  -            |       4   |  16,000   |                            |')
                            print('----------------------------------------------------------------------')
                            print('|  RAM1, RAM2   |       1   |   2,000   |                            |')
                            print('|  -            |       2   |   4,000   |                            |')
                            print('|  -            |       3   |   8,000   |                            |')
                            print('|  -            |       4   |  16,000   |                            |')
                            print('----------------------------------------------------------------------')
                            print('|  HDD          |       1   |   1,000   |                            |')
                            print('|  -            |       2   |   2,000   |                            |')
                            print('|  -            |       3   |   4,000   |                            |')
                            print('|  -            |       4   |   8,000   |                            |')
                            print('----------------------------------------------------------------------')
                            raise PassCommand

                        for Name in self.EquipNameFlag:
                            if command[1] == Name:
                                self.EquipNotExistFlag = False

                        if self.EquipNotExistFlag == True:
                            raise EquipNotExist

                        if int(command[2]) < 1 or int(command[2]) > 4:
                            raise LevelNotExist
                        
                        self.configEquipment(command[1], int(command[2]))
                        

                    except IndexError:
                        self.setStringColor('ALERT')
                        print('Please enter equipment level or equipment name.                       ')
                        print(' ex > config [equipment name] [equipment level]                       ')
                        self.setStringColor('CMDRESULT')
                        print('Config command Usage.                                                 ')
                        print('')
                        print('- Check Current Equipment Status.                                     ')
                        print(' ex > config current                                                  ')
                        print('')
                        print('- Check Equipment Requirements.                                       ')
                        print(' ex > config help                                                     ')

                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except LevelNotExist:
                        self.setStringColor('ALERT')
                        print('Equipment Level Doesn\'t exist.                                       ')
                        print('Level : 1 ~ 4                                                          ')
                        
                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None) 

                    except EquipNotExist:
                        self.setStringColor('ALERT')
                        print('Equipment Doesn\'t exist.                                             ')
                        print('Equipment : FIREWALL, MODEM, CPU1, CPU2, RAM1, RAM2, HDD              ')
                        
                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)

                    except PassCommand:
                        pass
                    
                    self.setStringColor('DEFAULT')


                # connect ------------------------------------------------------------------------------
                elif command[0] == 'connect':
                    try:
                        if self.Level.currentCanLoadDomain[command[1]] == False:
                            self.Level.currentCanLoadDomain[command[1]] = True

                        if self.Level.currentCanLoadDomain[command[1]] == True and self.Level.currentLevelCrackStatus[command[1]][0] == 0:
                            self.Level.currentConnectPos.append((self.Level.currentLoadedDomainInfo[self.Level.currentPWD][1], self.Level.currentLoadedDomainInfo[command[1]][1]))

                            self.Level.currentPWD = command[1]
                            self.PWD = '@ ' + self.Level.currentPWD + ' :> '

                            self.setStringColor('CMDRESULT')
                            print('Connect Successfully Done!')
                            print('current working directory : ', self.Level.currentPWD)

                            self.Effects.setEffect('SYSTEMONLINE')
                            self.Effects.play(None)

                        elif command[1] == self.Level.currentPWD:
                            self.setStringColor('ALERT')
                            print('You are already in there. Please select another domain to connect.    ')
                            print('current working directory : ', self.Level.currentPWD)

                            self.Effects.setEffect('WARNING')
                            self.Effects.play(None)

                        elif self.Level.currentLevelCrackStatus[command[1]][0] != 0 or self.Level.currentLevelCrackStatus[command[1]][1] != 0:
                            self.setStringColor('ALERT')
                            print('You have to hack your target system first.                            ')
                            self.setStringColor('CMDRESULT')

                            if self.Level.currentLevelCrackStatus[command[1]][1] != 0:
                                print('command : crack ', command[1], (45 - len(command[1])) * ' '        )

                            if self.Level.currentLevelCrackStatus[command[1]][0] != 0:
                                print('command : decrypt', command[1], (44 - len(command[1])) * ' '       )

                            self.Effects.setEffect('WARNING')
                            self.Effects.play(None)                        

                        else:
                            self.setStringColor('ALERT')
                            print('System Undetected.                                                    ')
                            print('Please scan system to confirm exist.                                  ')
                            print(' ex > scan [www.example.com]                                          ')
                            
                            self.Effects.setEffect('WARNING')
                            self.Effects.play(None)

                    except IndexError:
                        self.setStringColor('ALERT')
                        print('Please enter domain for connect.                                      ')
                        print(' ex > connect [www.example.com]                                       ')

                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except KeyError:
                        self.setStringColor('ALERT')
                        print('Domain doesn\'t exist  :', command[1], (45 - len(command[1])) * ' ')
                        
                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)

                    self.setStringColor('DEFAULT') 

                # crack --------------------------------------------------------------------------------
                elif command[0] == 'crack':
                    try:
                        if self.Level.currentCanLoadDomain[command[1]] == False:
                            self.Level.currentCanLoadDomain[command[1]] = True

                        if command[1] == 'localhost':
                            raise YouAreInLocalhost

                        if self.Level.currentLevelCrackStatus[command[1]][1] != 0:
                            if self.Level.setProcess == True:
                                raise ProcessOnWorkingError

                            self.setStringColor('CMDRESULT')
                            print('Cracking [', command[1], '] Passwords')
                            self.Level.ProcessingTimeSet(command[0], command[1]) 
                            self.Level.TracingTimeSet()

                            self.Effects.setEffect('LAUNCHATTACK')
                            self.Effects.play(None)                    

                            self.Level.setProcess = True

                        else:
                            self.setStringColor('ALERT')
                            print('[', command[1], '] is already cracked.', (45 - len(command[1])) * ' ')

                            self.Effects.setEffect('WARNING')
                            self.Effects.play(None)

                    except IndexError:
                        self.setStringColor('ALERT')
                        print('Please enter domain for crack.                                        ')
                        print(' ex > crack [www.example.com]                                         ')

                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except KeyError:
                        self.setStringColor('ALERT')
                        print('Domain doesn\'t exist  :', command[1], (45 - len(command[1])) * ' ')
                        print('Please check domain to crack.                                     ')

                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)

                    except ProcessOnWorkingError:
                        self.setStringColor('ALERT')
                        print('Process already on working.                                           ')
                        print('Processing :', self.Level.ProcessType, self.Level.ProcessHost, (55 - len(self.Level.ProcessType) - len(self.Level.ProcessHost)) * ' ')
                        
                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except YouAreInLocalhost:
                        self.setStringColor('ALERT')
                        print('You are in your localhost.                                            ')
                        print('You cannot crack your own system.                                     ')
                        
                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)                        


                    self.setStringColor('DEFAULT')                 

                # decrypt ------------------------------------------------------------------------------
                elif command[0] == 'decrypt':
                    try:
                        
                        if self.Level.currentCanLoadDomain[command[1]] == False:
                            self.Level.currentCanLoadDomain[command[1]] = True
                        
                        if command[1] == 'localhost':
                            raise YouAreInLocalhost

                        if self.Level.currentLevelCrackStatus[command[1]][0] != 0:
                            if self.Level.setProcess == True:
                                raise ProcessOnWorkingError

                            self.setStringColor('CMDRESULT')
                            print('Decrypting [', command[1], '] Encryption Key')
                            self.Level.ProcessingTimeSet(command[0], command[1]) 
                            self.Level.TracingTimeSet()
                            
                            self.Effects.setEffect('LAUNCHATTACK')
                            self.Effects.play(None)     

                            self.Level.setProcess = True

                        else:
                            self.setStringColor('ALERT')
                            print('[', command[1], '] is already decrypted.', (43 - len(command[1])) * ' ')

                            self.Effects.setEffect('WARNING')
                            self.Effects.play(None)

                    except IndexError:
                        self.setStringColor('ALERT')
                        print('Please enter domain for decrypt.                                      ')
                        print(' ex > crack [www.example.com]                                         ')

                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except KeyError:
                        self.setStringColor('ALERT')
                        print('Domain doesn\'t exist  :', command[1], (45 - len(command[1])) * ' ')
                        print('Please check domain to decrypt.                                   ')

                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)

                    except ProcessOnWorkingError:
                        self.setStringColor('ALERT')
                        print('Process already on working.                                           ')
                        print('Processing :', self.Level.ProcessType, self.Level.ProcessHost, (55 - len(self.Level.ProcessType) - len(self.Level.ProcessHost)) * ' ')
                        
                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except YouAreInLocalhost:
                        self.setStringColor('ALERT')
                        print('You are in your localhost.                                            ')
                        print('You cannot decrypt your own system.                                   ')
                        
                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    self.setStringColor('DEFAULT')                

                # delete -------------------------------------------------------------------------------
                elif command[0] == 'delete':# Add Processing
                    try:
                        del self.Level.currentLoadedDomainFiles[self.Level.currentPWD][command[1]]
                        self.Level.currentLoadedDomainInfo[self.Level.currentPWD][4] = len(self.Level.currentLoadedDomainFiles[self.Level.currentPWD])

                        self.Effects.setEffect('COMPLETE')
                        self.Effects.play(None)

                    except IndexError:
                        self.setStringColor('ALERT')
                        print('Please enter file name for delete.                                    ')
                        print(' ex > delete [file name]                                              ')

                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except KeyError:
                        self.setStringColor('ALERT')
                        print('File doesn\'t exist    :', command[1], (45 - len(command[1])) * ' ')
                        print('Please check file name to delete.                                 ')

                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)

                    self.setStringColor('DEFAULT')                   

                # download -----------------------------------------------------------------------------
                elif command[0] == 'download':
                    try:
                        localFiles      = self.Level.currentLoadedDomainFiles['localhost']
                        localFileNames  = list(localFiles)

                        for LFN in localFileNames:
                            if command[1] == LFN:
                                raise FileAlreadyExist

                        self.Level.ProcessingTimeSet(command[0], self.Level.currentPWD, 0, command[1])
                        self.Level.TracingTimeSet()

                        self.Effects.setEffect('LOADING')
                        self.Effects.play(None)     

                        self.Level.setProcess = True

                        self.setStringColor('CMDRESULT')
                        print('Downloading Start')
                        print('Download Filename : ', command[1])
                        
                    except IndexError:
                        self.setStringColor('ALERT')
                        print('Please enter file name for download.                                  ')
                        print(' ex > download [file name]                                            ')

                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except KeyError:
                        self.setStringColor('ALERT')
                        print('File doesn\'t exist    :', command[1], (45 - len(command[1])) * ' ')
                        print('Please check file name to download.                               ')

                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)

                    except FileAlreadyExist:
                        self.setStringColor('ALERT')
                        print('File already exist on your directory.                                 ')
                        print('If you download forcely, this file will cover the original file.      ')
                        self.setStringColor('DEFAULT')
                        AnswerDone = False

                        while not AnswerDone:
                            self.setStringColor('DEFAULT')
                            Answer = input('Do you want to download it forcely?(Y/N) : ')

                            if Answer == 'y' or Answer == 'Y':
                                self.Level.ProcessingTimeSet(command[0], self.Level.currentPWD, 0, command[1])
                                self.Level.TracingTimeSet()

                                self.Effects.setEffect('LOADING')
                                self.Effects.play(None)     

                                self.Level.setProcess = True
                                AnswerDone = True

                            elif Answer == 'n' or Answer == 'N':
                                self.setStringColor('ALERT')
                                print('Suspend Operation : Download                                          ')
                                AnswerDone = True

                            else:
                                self.setStringColor('ALERT')
                                print('Please Enter Y or y / N or n.                                        ')

                                self.Effects.setEffect('WARNING')
                                self.Effects.play(None)
                        
                    self.setStringColor('DEFAULT')                

                # exit ---------------------------------------------------------------------------------
                elif command[0] == 'exit':
                    if self.Level.currentPWD == 'localhost':
                        self.setStringColor('ALERT')
                        print('You are in your local system.                                         ')
                        print('Suspend Operation : Exit                                              ')
                        self.setStringColor('CMDRESULT')
                        print('current working directory : ', self.Level.currentPWD)

                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)

                    else:
                        self.setStringColor('CMDRESULT')
                        print('disconnect from ', self.Level.currentPWD)
                        self.Level.currentPWD = 'localhost'
                        self.Level.currentConnectPos = []
                        print('current working directory : ', self.Level.currentPWD)
                        
                        self.PWD = '@ ' + self.Level.currentPWD + ' :> '

                        self.Effects.setEffect('SYSTEMOFFLINE')
                        self.Effects.play(None)

                    self.setStringColor('DEFAULT')
                    
                # help ---------------------------------------------------------------------------------
                elif command[0] == 'help':
                    self.setStringColor('CMDRESULT')
                    self.printOption()
                    self.setStringColor('DEFAULT')

                # scan ---------------------------------------------------------------------------------
                elif command[0] == 'scan':
                    try:
                        self.setStringColor('CMDRESULT')
                        
                        if self.Level.currentCanLoadDomain[command[1]] == False:
                            self.Level.currentCanLoadDomain[command[1]] = True

                        # print Domain Information -----------------------------------------------------
                        for i, DomainInfo   in enumerate(self.Level.currentLoadedDomainInfo[command[1]]):
                            # Position, Text_Position, Status_of_Domain(NORMAL, TARGET ...)
                            if i == 3:
                                print(self.DomainInfo[i], format(DomainInfo, ","), '$')
                            elif i != 1 and i != 2 and i != 5:
                                print(self.DomainInfo[i], DomainInfo)
                            
                        # print Security Information ---------------------------------------------------
                        for i, SecurityInfo in enumerate(self.Level.currentLevelCrackStatus[command[1]]):
                            if i == 0 and SecurityInfo != 0:
                                print(self.SecurityInfo[i], SecurityInfo, 'bits')

                            elif i == 0 and SecurityInfo == 0:
                                print(self.SecurityInfo[i], 'None')

                            elif i == 1 and SecurityInfo != 0:
                                print(self.SecurityInfo[i], SecurityInfo, 'characters')
                                    
                            elif i == 1 and SecurityInfo == 0:
                                print(self.SecurityInfo[i], 'None')

                        self.Effects.setEffect('SCANNING')
                        self.Effects.play(None)
                        
                    except IndexError:
                        self.setStringColor('ALERT')
                        print('Please enter domain for scan.                                         ')
                        print(' ex > scan [www.example.com]                                          ')

                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except KeyError:
                        self.setStringColor('ALERT')
                        print('Domain doesn\'t exist  :', command[1], (45 - len(command[1])) * ' ')
                        print('Please check domain to scan.                                          ')

                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)

                    self.setStringColor('DEFAULT')                

                # transfer -----------------------------------------------------------------------------
                elif command[0] == 'transfer':
                    # IndexError가 계속 일어남... 왜지...
                    try:
                        if (self.Level.currentLoadedDomainInfo[self.Level.currentPWD][3] - int(command[1])) < 0:
                            raise KeyError

                        if self.Level.currentPWD == 'localhost':
                            raise YouAreInLocalhost

                        self.Level.ProcessingTimeSet(command[0], self.Level.currentPWD, int(command[1]))
                        self.Level.TracingTimeSet()
                        
                        self.Effects.setEffect('LOADING')
                        self.Effects.play(None)     

                        self.Level.setProcess = True

                    except IndexError:
                        self.setStringColor('ALERT')
                        print('Please enter how much do you transfer.                                ')
                        print(' ex > transfer [money]                                                ')

                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except KeyError:
                        self.setStringColor('ALERT')
                        print('There are no enough money to transfer.                                ')
                        print('Please check how much have some money your target.                    ')

                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)

                    except YouAreInLocalhost:
                        self.setStringColor('ALERT')
                        print('You are in your localhost.                                            ')
                        print('You cannot transfer money that you already have.                      ')

                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)                        


                # upload -------------------------------------------------------------------------------
                elif command[0] == 'upload':
                    try:
                        localFiles      = self.Level.currentLoadedDomainFiles['localhost']
                        localFileNames  = list(localFiles)
                        PWDFiles        = self.Level.currentLoadedDomainFiles[self.Level.currentPWD]
                        PWDFileNames    = list(PWDFiles)
                        ExistFlag        = False

                        for LFN in localFileNames:  # Check Local system has the file.
                            if command[1] == LFN:
                                ExistFlag = True

                        if ExistFlag == False:
                            raise FileNotFoundError

                        for PFN in PWDFileNames:    # Check Destination system has the file.
                            if command[1] == PFN:
                                raise FileAlreadyExist

                        self.Level.ProcessingTimeSet(command[0], 'localhost', 0, command[1])
                        self.Level.TracingTimeSet()

                        self.Effects.setEffect('LOADING')
                        self.Effects.play(None)     

                        self.Level.setProcess = True
                        
                        print('Uploading Start')
                        print('Upload Filename : ', command[1])
                        
                    except IndexError:
                        self.setStringColor('ALERT')
                        print('Please enter file name for upload.                                    ')
                        print(' ex > upload [file name]                                              ')

                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except KeyError:
                        self.setStringColor('ALERT')
                        print('File doesn\'t exist    :', command[1], (45 - len(command[1])) * ' ')
                        print('Please check file name to upload.                                 ')

                        self.Effects.setEffect('ERROR')
                        self.Effects.play(None)

                    except FileNotFoundError:
                        self.setStringColor('ALERT')
                        print('File doesn\'t exist on your directory.                                 ')
                        print('Suspend Operation : Upload                                            ')
                        self.setStringColor('DEFAULT')
                        
                        self.Effects.setEffect('WARNING')
                        self.Effects.play(None)

                    except FileAlreadyExist:
                        self.setStringColor('ALERT')
                        print('File already exist on your destination.                               ')
                        print('If you upload it forcely, the file will be covered the original file. ')
                        self.setStringColor('DEFAULT')
                        AnswerDone = False

                        while not AnswerDone:
                            self.setStringColor('DEFAULT')
                            Answer = input('Do you want to upload it forcely?(Y/N) : ')

                            if Answer == 'y' or Answer == 'Y':
                                self.Level.ProcessingTimeSet(command[0], 'localhost', 0, command[1])
                                self.Level.TracingTimeSet()

                                self.Effects.setEffect('LOADING')
                                self.Effects.play(None)     

                                self.Level.setProcess = True
                                AnswerDone = True

                            elif Answer == 'n' or Answer == 'N':
                                self.setStringColor('ALERT')
                                print('Suspend Operation : Upload                                            ')
                                AnswerDone = True

                            else:
                                self.setStringColor('ALERT')
                                print('Please Enter Y or y / N or n.                                        ')
                        
                                self.Effects.setEffect('WARNING')
                                self.Effects.play(None)

                    self.setStringColor('DEFAULT') 



                # Console Commands=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                # cat ----------------------------------------------------------------------------------
                elif command[0] == 'cat':
                    # command[1] == filename
                    try:
                        self.setStringColor('DOMAINFILES')
                        print(self.Level.currentLoadedDomainFiles[self.Level.currentPWD][command[1]][2])
                    
                    except IndexError:
                        self.setStringColor('ALERT')
                        print('Please enter filename.                                                ')
                        print(' ex > cat [filename]                                                  ')
                    
                    except KeyError:
                        self.setStringColor('ALERT')
                        print('File doesn\'t exist.   :', command[1], (45 - len(command[1])) * ' ')
                        print('Please check file name to catch.                                      ')

                    self.setStringColor('DEFAULT')
                    
                # ls -----------------------------------------------------------------------------------
                elif command[0] == 'ls':
                    # print domainFileDict in self.Level.currentPWD
                    self.setStringColor('DOMAINFILES')
                    
                    print('FileName\t\tDate\t\t\tSize(MB)')
                    print('----------------------------------------------------------------------')

                    FileName    = list(self.Level.currentLoadedDomainFiles[self.Level.currentPWD])
                    FileInfo    = list(self.Level.currentLoadedDomainFiles[self.Level.currentPWD].values())
                    FileList    = []

                    for Index in range(len(FileName)):
                        tmpData = FileName[Index] + '\t\t' + FileInfo[Index][0] + '\t' + FileInfo[Index][1] + ' MB'

                        if len(FileName[Index]) > 20:
                            tmpData = FileName[Index] + '\t' + FileInfo[Index][0] + '\t' + FileInfo[Index][1] + ' MB'

                        FileList.append(tmpData)

                    for File  in FileList:
                        print(File)

                    print('\n')
                    
                    self.setStringColor('DEFAULT')

                # whoami -------------------------------------------------------------------------------
                elif command[0] == 'whoami':
                    self.setStringColor('CMDRESULT')
                    print('current working directory : ', self.Level.currentPWD)
                    self.setStringColor('DEFAULT')

                # test ---------------------------------------------------------------------------------
                elif command[0] == 'test':
                    pass

                # not a command ------------------------------------------------------------------------
                else:
                    self.setStringColor('ALERT')
                    print('Alert : Wrong Command Inputted.                                       ')
                    print('        Please Check Commands.                                        ')
                    self.setStringColor('CMDRESULT')
                    print('        command : help                                                ')
                    self.setStringColor('DEFAULT')
                    
                    self.Effects.setEffect('WARNING')   
                    self.Effects.play(None)


            except TypeError:
                os.system('cls')

            

    def configEquipment(self, Equip, Level):
        '''
        :param Equip:       Name of Equipment.
        '''
        try:
            count   = 0
            Comp    = 0x0000000F
            LvHex   = 0x0

            if Level == 1:
                LvHex = 0x1
            elif Level == 2:
                LvHex = 0x2
            elif Level == 3:
                LvHex = 0x4
            elif Level == 4:
                LvHex = 0x8

            if Equip == 'FIREWALL':
                if self.Level.currentLoadedDomainInfo['localhost'][3] < (LvHex * 1000):
                    raise MoneyNotEnough
                else:
                    count = 6
            elif Equip == 'MODEM':
                if self.Level.currentLoadedDomainInfo['localhost'][3] < (LvHex * 2000):
                    raise MoneyNotEnough
                else:
                    count = 5
            elif Equip == 'CPU1':
                if self.Level.currentLoadedDomainInfo['localhost'][3] < (LvHex * 2000):
                    raise MoneyNotEnough
                else:
                    count = 4
            elif Equip == 'CPU2':
                if self.Level.currentLoadedDomainInfo['localhost'][3] < (LvHex * 2000):
                    raise MoneyNotEnough
                else:
                    count = 3
            elif Equip == 'RAM1':
                if self.Level.currentLoadedDomainInfo['localhost'][3] < (LvHex * 2000):
                    raise MoneyNotEnough
                else:
                    count = 2
            elif Equip == 'RAM2':
                if self.Level.currentLoadedDomainInfo['localhost'][3] < (LvHex * 2000):
                    raise MoneyNotEnough
                else:
                    count = 1
            elif Equip == 'HDD':
                if self.Level.currentLoadedDomainInfo['localhost'][3] < (LvHex * 1000):
                    raise MoneyNotEnough
                else:
                    count = 0


            for i in range(count):
                Comp  = Comp  << 4
                LvHex = LvHex << 4


            DeleteEquip = self.Level.currentEquip & Comp

            self.Level.currentEquip -= DeleteEquip
            self.Level.currentEquip += LvHex

            self.Level.DisplayDraw.SetEquipStatus(self.Level.currentEquip)
            print('Change Equipment Status : ', Equip, Level)

            self.Effects.setEffect('COMPLETE')   
            self.Effects.play(None)


        except MoneyNotEnough:
            self.setStringColor('ALERT')
            print('Your money is not enough to buy equipment.                            ')
            print('Money  :', self.Level.currentLoadedDomainInfo['localhost'][3], (60-len(str(self.Level.currentLoadedDomainInfo['localhost'][3])))*' ')
            self.setStringColor('DEFAULT')
            
            self.Effects.setEffect('WARNING')   
            self.Effects.play(None)
            



    def printOption(self):
        optionString = ('\nHacker Commands' +
                        '\n----------------------------------------------------------------------'+
                        '\n' + 
                        '\nabort            - Abort an ongoing transfer, download, crack, etc.' +
                        '\nclear            - Clears the command console window.' +
                        '\nconfig           - Display the current hardware configuration.' +
                        '\n                   ex > config current' +
                        '\n                        show current equipment levels.' +
                        '\n                   ex > config [equipment name] [equipment level]' +
                        '\n                        set current equipment level.' +
                        '\nconnect          - Connect to your target.' +
                        '\n                   ex > connect [Server Address] [Port]'
                        '\n                   ex > connect test.com 80' +
                        '\ncrack            - Crack your target sysytem.' + 
                        '\ndecrypt          - Decrypts the encryption key of a server.' +
                        '\ndelete           - Delete a file.' +
                        '\n                   ex > delete [FileName]' +
                        '\ndownload         - download target\'s data that you want.' +
                        '\n                   ex > download [Target\'s FileName]' +
                        '\ngameover         - Exit Game.' +
                        '\nhelp             - Displays a list of commands and their meaning.' +
                        '\nscan             - Scan a host for open ports.' +
                        '\n                   ex > scan [host Address]' +
                        '\n                   ex > scan test.com' +
                        '\nupload           - upload your data to target that you connected.' +
                        '\n                   ex > upload [My FileName]' +
                        '\ntransfer         - transfer money to your localhost system.' +
                        '\n                   ex > transfer [Money]' +
                        '\n                   ex > transfer 10000' +
                        '\n' +
                        '\n' +
                        '\nConsole Commands' +
                        '\n----------------------------------------------------------------------'+
                        '\ncat              - Displays the contents of a file.' +
                        '\n                   ex > cat [FileName]' +
                        '\nls               - Display All directory Files.' +
                        '\nwhoami           - Display who am i.' +
                        '\n'
                        )

        print(optionString)


class ProcessOnWorkingError(Exception):
    pass

class FileAlreadyExist(Exception):
    pass

class YouAreInLocalhost(Exception):
    pass

class LevelNotExist(Exception):
    pass

class EquipNotExist(Exception):
    pass

class PassCommand(Exception):
    pass

class MoneyNotEnough(Exception):
    pass