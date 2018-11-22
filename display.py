import pygame
import os

class Text:
    def __init__(self):
        self.DISPLAYSURF    = None

        BASICFONTSIZE       = 20

        # Text_Setting  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-
        # Font Categories
        CALISTO_MT          = 'Calisto MT'
        CONSOLAS            = 'consolas'
        ARIAL               = 'Arial'
        CORBEL              = 'Corbel'
        EBRIMA              = 'Ebrima'
        CENTURY             = 'Century'
        LUCIDA_CONSOLE      = 'Lucida Console'

        #WORD Setting
        self.WORD_SIZE_COUNTRY   = 20
        self.WORD_SIZE_DOMAIN    = 20
        self.WORD_SIZE           = 20
        self.WORD_Pos            = (5, 5)
        self.WORD_Pos2           = (5, 17)

        (495, 855)


    def SetDisplaySurface(self, Screen):
        self.DISPLAYSURF = Screen


    def makeText(self, FONT, Message, AntiAliasing, TextColor, TextPosition, ShadowStatus):
        '''
        :param FONT:        Font to Use
        :param Message:     Message to Print
        :param AntiAliasing:Anti-Aliasing Setting
                                - True  : Anti-Aliasing set(recommand)
                                - False : Anti-Aliasing unset
        :param TextColor:   Color of Text
        :param TextPosition:Position of Text(Tuple Data)
        '''

        # Shadow Definition =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        
        if ShadowStatus == True:
            SHADOWSURF          = FONT.render(Message, AntiAliasing, pygame.Color('BLACK'), None)
            SHADOWRect          = SHADOWSURF.get_rect()
            SHADOWRect.topleft  = (TextPosition[0]+1, TextPosition[1]+1)
            
            self.DISPLAYSURF.blit(SHADOWSURF, SHADOWRect)   # Print Shadow

        # Message Difinition=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        TEXTSURF            = FONT.render(Message, AntiAliasing, TextColor, None)
        TEXTRect            = TEXTSURF.get_rect()       
        TEXTRect.topleft    = (TextPosition[0], TextPosition[1])        
                
        self.DISPLAYSURF.blit(TEXTSURF,  TEXTRect)      # Print Message  


    def ChangeTupleData(self, TP, C_Position):
        '''
        Change Tuple's Data.
        C_Position Data is adding value.

        :param TP:          Tuple data
        :param C_Position:  Position to change
            - Tuple Data have to change C_Position Length
        :return:            Modified Tuple Data
        '''
        lst = list(TP)
        
        for i in range(len(C_Position)):
            lst[i] += C_Position[i]
        
        return tuple(lst)




class Draw:
    def __init__(self):

        self.DISPLAYSURF    = None
        

        # Equipments List =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        '''
        NULL HDD  RAM1 RAM2 CPU1 CPU2 MOD  FW
        0000 0000 0000 0000 0000 0000 0000 0000
            
        Total 4 Byte
    
        LV4 LV3 LV2 LV1 
        0   0   0   0
        '''

        # Equipment Position  =-=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.FIREWALL       = ( 531,  747)
        self.MODEM          = ( 531,  791)
        self.CPU1           = ( 732,  718)
        self.CPU2           = ( 732,  785)
        self.RAM1           = ( 819,  731)
        self.RAM2           = ( 819,  775)
        self.HDD            = ( 819,  845)

        # Status Value =-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-
        self.LOCAL          = 0
        self.NORMAL         = 1
        self.BOUND          = 2
        self.HIDDEN         = 3
        self.TARGET         = 4

        # =-=-=-=-=-=-=-= R    G    B =-=-=-=-=-=-=-=-=-=-
        self.BLACK          = (  0,   0,   0)
        self.GRAY           = (150, 150, 150)
        self.NAVYBLUE       = ( 60,  60, 100)
        self.WHITE          = (255, 255, 255)
        self.RED            = (255,   0,   0)
        self.GREEN          = (  0, 255,   0)
        self.DARKGREEN      = (  0, 100,   0)
        self.BLUE           = (  0,   0, 255)
        self.YELLOW         = (255, 255,   0)
        self.ORANGE         = (255, 128,   0)
        self.PURPLE         = (255,   0, 255)
        self.CYAN           = (  0, 255, 255)
        self.WHITE          = (255, 255, 255)
        self.DARKBROWN      = (150, 100,  50)
        self.DARKCYAN       = (100, 200, 200)

        # Map's Colors -=-=-=-=-=-=-=-=-=-=-=-=-=-
        self.BROWN          = (250, 200, 150)
        self.brownSub       = ( 50,  50,  50)
        self.PURPLE         = (250, 150, 250)
        self.purpleSub      = ( 50,  50,  50)
        self.RED            = (250, 150, 150)
        self.redSub         = (  0,  50,  50)
        self.GREEN          = (150, 250, 150)
        self.greenSub       = ( 50,  50,  50)
        self.BLUE           = (150, 150, 250)
        self.blueSub        = ( 50,  50,   0)

        #self.equipLevels    = {}
        self.EquipNames     = []
        self.EquipLevels    = []
        self.EquipPosition  = []

        self.StaticCount        = 255
        self.DrawPointReverse   = False
        self.CircleSurface      = pygame.Surface((100, 100)) # (width, height)
        self.CircleSurface.set_colorkey((0,0,0))             # make no background color

        self.GameOverImg    = pygame.image.load('.\\Game Image\\Etc\\GameOver.jpg')
        self.TransparentLen = 0


    def SetDisplaySurface(self, Screen):
        self.DISPLAYSURF = Screen



    def getColor(self, status):
        '''
        :param status:      status of color
                            NORMAL, BOUND, HIDDEN, TARGET

        :return:            (Color01, Color02, Color03)
        '''
        if status == 0:   # LOCAL
            returnColor = self.getColorList( self.BROWN, self.brownSub )

        elif status == 1: # NORMAL
            returnColor = self.getColorList( self.GREEN, self.greenSub )

        elif status == 2: # BOUND
            returnColor = self.getColorList(  self.BLUE, self.blueSub  )

        elif status == 3: # HIDDEN
            returnColor = self.getColorList(   self.RED, self.redSub   )

        elif status == 4: # TARGET
            returnColor = self.getColorList(self.PURPLE, self.purpleSub)

        return returnColor



    def getColorList(self, color, sub):
        '''
        :param color:       color tuple data
        :param sub:         data to substract from tuple data

        :return:            (Color01, Color02, Color03)
        '''
        colorTupleList  = list()

        for i in range(3):
            colorList       = list(color)

            for j in range(3):
                colorList[j]   -= (sub[j] * i)

            colorTupleList.append(tuple(colorList))

        return colorTupleList



    def getBlinkPosition(self, pos):
        posList = list(pos)

        for i in range(2):
            posList[i] -= 50

        return tuple(posList)



    def DrawPoint(self, CenterPos, Status):
        '''
        :param CenterPos:       Circle's Center Point(Position of Circle)
        :param Status:          Status of Circle
                                - NORMAL_POINT(BROWN) : Normal Position on the map
                                - BOUND_POINT(PURPLE) : Bound  Position on the map
                                - HIDDEN_POINT(GREEN) : Hidden Position on the map(Default == Hide)
                                - TARGET_POINT(RED)   : Target Position on the map
        '''
        circleSize    = [5, 3, 2, 11]
        colorTuples  = self.getColor(Status)
        blinkPos     = self.getBlinkPosition(CenterPos)

        for i in range(3):
            pygame.draw.circle(self.DISPLAYSURF, colorTuples[i], CenterPos, circleSize[i], 0)


        # Target or Localhost has more effect. -----------------------------------------------------
        if Status == 4 or Status == 0:  
            self.CircleSurface.set_alpha(self.StaticCount)
            pygame.draw.circle(self.CircleSurface, colorTuples[0], (50, 50), circleSize[3], 2)
            self.DISPLAYSURF.blit(self.CircleSurface, blinkPos)
            
        self.StaticCount -= 5

        if self.StaticCount <= -255:
            self.StaticCount = 255




    def DrawTransparent(self, Pos, Color, Length, Width, Alpha=75):
        TransparentRect = pygame.Surface((Length, Width))
        TransparentRect.set_alpha(Alpha)
        TransparentRect.fill(Color)

        self.DISPLAYSURF.blit(TransparentRect, Pos)



    def DrawLine(self, PosFrom, PosTo, Color):
        pygame.draw.aaline(self.DISPLAYSURF, Color, PosFrom, PosTo, True)



    def DrawProcessBar(self, Length, Width=15):
        '''
        Draw Rectangle with transparent.

        :param Length:      Length of Transparent Rectangle(left to right)
        :param Width:       Width  of Transparent Rectangle(top to bottom)
        :param Position:    Position of Transparent Rectangle

        Total Length        ==> 310

        '''
        TransparentRect = pygame.Surface((Length, Width))
        TransparentRect.set_alpha(200)                     #Strength of Transparent 
        TransparentRect.fill(self.DARKGREEN)               #Color of Transparent
        
        self.DISPLAYSURF.blit(TransparentRect, (494, 855))



    def DrawEquipment(self):
        for Index in range(7):
            if self.EquipNames[Index] is None:
                pass
         
            elif self.EquipLevels[Index] is 0:
                pass
            
            elif self.EquipPosition[Index] is (0,0):
                pass

            else:
                ImgName = 'Equipments\\' + self.EquipNames[Index] + str(self.EquipLevels[Index]) + ".jpg"
                EquipImg = pygame.image.load(ImgName)
                self.DISPLAYSURF.blit(EquipImg, self.EquipPosition[Index])



    def DrawDomainInfo(self, FONT, Pos, Message):
        if self.TransparentLen < 300:
            self.TransparentLen += 30

        pygame.draw.rect(self.DISPLAYSURF, self.DARKGREEN, pygame.Rect(Pos[0]-2, Pos[1]-2, self.TransparentLen+2, 102), 2)

        TransparentRect = pygame.Surface((self.TransparentLen, 100))
        TransparentRect.set_alpha(150)                          #Strength of Transparent 
        TransparentRect.fill(self.DARKGREEN)                    #Color of Transparent
        
        self.DISPLAYSURF.blit(TransparentRect, Pos)


    def SetEquipStatus(self, Meta):
        '''
        :param Meta:        Metadata to equipments
                            - What i have
                            - How much i have
                            - ex > 0x01111111 (4Byte)
        '''
        self.EquipNames     = []
        self.EquipLevels    = []
        self.EquipPosition  = []    
                                      
        Comp                        = 0x0000000F

        for CategoryNum in range(7):      #Data Area And
            LvHex = Meta & Comp   
            
            for i in range(CategoryNum):
                LvHex = LvHex >> 4
                
            self.EquipNames.append(   self.GetEquipCategory(CategoryNum))
            self.EquipLevels.append(  self.GetEquipLevel(LvHex))
            self.EquipPosition.append(self.GetEquipPosition(CategoryNum))

            Comp = Comp << 4        
        


    def GetEquipCategory(self, Num):
        '''
        :param Num:         Number of Categories
                            - HDD, RAM2, RAM1, CPU2, CPU1, MODEM, FIREWALL 
                     Array  - 0    1     2     3     4     5      6
                     Hex    - 6    5     4     3     2     1      0
                              

        :return:            Category Value
        '''
        
        return{
            6 : "FIREWALL",
            5 : "MODEM",
            4 : "CPU",
            3 : "CPU",
            2 : "RAM",
            1 : "RAM",
            0 : "HDD",
            }.get(Num, None) # Default Return



    def GetEquipLevel(self, Hex):
        '''
        :param Hex:         Hex Value of Level
                            - 0x1 = Level 1
                            - 0x2 = Level 2
                            - 0x4 = Level 3
                            - 0x8 = Level 4
        :return:            Level Value
        '''
        
        return{
            0x1 : 1,
            0x2 : 2,
            0x4 : 3,
            0x8 : 4,
            }.get(Hex, 0) # Default Return



    def GetEquipPosition(self, Num):
        '''
        :param Num:         Number of Categories
                            - HDD, RAM2, RAM1, CPU2, CPU1, MODEM, FIREWALL 
                     Array  - 0    1     2     3     4     5      6
                     Hex    - 6    5     4     3     2     1      0
        :return:            Category Value
        '''
        
        return{
            6 : self.FIREWALL,
            5 : self.MODEM,
            4 : self.CPU1,
            3 : self.CPU2,
            2 : self.RAM1,
            1 : self.RAM2,
            0 : self.HDD,
            }.get(Num, (0,0)) # Default Return



    def getEquipStatus(self, Meta):
        Comp    = 0x0000000F

        for CategoryNum in range(7):      #Data Area And
            LvHex = Meta & Comp
            
            for i in range(CategoryNum):
                LvHex = LvHex >> 4

            print(self.GetEquipCategory(CategoryNum), self.GetEquipLevel(LvHex))            
            
            Comp = Comp << 4
    


    def DrawGameOver(self):
        self.DISPLAYSURF.blit(self.GameOverImg, (100, 200))
    


class NewExplorer():
    def __init__(self, caption, img):
        '''
        :param caption:     Caption text of your new explorer
        :param img:         Image directory of your new explorer
        '''

        # Set pygame elements =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        pygame.init()
        pygame.display.set_caption(caption)

        self.NewExFPS               = 30
        self.NewExMapImg            = pygame.image.load(img)
        self.NewExMapImgWH          = (self.NewExMapImg.get_width(), self.NewExMapImg.get_height())
                                    # self.MapImgWH[0] = width
                                    # self.MapImgWH[1] = height
        self.NewExFPSCLOCK          = pygame.time.Clock()
        self.NewExDISPLAYSURF       = pygame.display.set_mode(self.NewExMapImgWH, pygame.DOUBLEBUF, 32)



    def Explorer(self):
        Done = False
        
        while not Done:
            
            self.NewExDISPLAYSURF.blit(self.NewExMapImg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Done = True
                elif event.type == pygame.KEYDOWN:
                    Done = True


            pygame.display.flip()
            self.NewExFPSCLOCK.tick(self.NewExFPS)



