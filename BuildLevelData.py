def domainInfo(domain, position, positiontxt, money, files, dates, sizes):
    '''
    :param domain:      Domain Name             (ex > www.naver.com)
    :param position:    Domain Position         (ex > ( 123, 123 ))
    :param positiontxt: Domain Text Position    (ex > ( 123, 123 ))
    :param money:       Money that domain has.  (ex > 1234)
    :param files:       File Dictionary Data    (ex > {'filename' : 'filedata', ...})
    :param dates:       Date of each Files      (ex > ['date1', 'date2', ... ])
    :param sizes:       Size of each Files      (ex > [1234, 1234, ... ])
    '''

    '''
    Domain      (   30 Bytes)        # String
    Position    (    4 Bytes)        # Tuple - Center Point Position
    PositionTxt (    4 Bytes)        # Tuple - Text Position
    Money       (    4 Bytes)        # Int
    NumOfFiles  (    4 Bytes)        # Int
    Status      (    1 Bytes)        # Int
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Domain Data
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    '''
    Domain      = getDomain(domain)             # b''
    Position    = getPosition(position)         # b''
    PositionTxt = getPosition(positiontxt)      # b''
    Money       = getMoney(money)               # b''
    NumOfFiles  = getNumOfFiles(len(files))     # b''
    Status      = b'\x01'                       # b'' hard coded status number.

    '''
    FileName    (  256 Bytes)        # String
    Date        (   19 Bytes)        # String
    size        (    4 Bytes)        # String
    FileData    (10240 Bytes)        # String

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # File System Data
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    '''
    FileSystem  = getFileSystemData(files, dates, sizes)

    sumData     = Domain + Position + PositionTxt + Money + NumOfFiles + Status + FileSystem

    tmpName     = Domain.split()
    wFileName   = b''

    for i, Word in enumerate(tmpName):
        wFileName += Word

    with open(b'MetaData\\' + wFileName + b'.meta', 'wb') as wFile:
        wFile.write(sumData)


def getDomain(d):
    d = PadData(d, 30, ' ')

    return d.encode()


def getPosition(p):
    posX = hex(p[0])[2:]
    posY = hex(p[1])[2:]

    posX = PadData(posX, 4, '0')    # 8 Bytes of Hex
    posY = PadData(posY, 4, '0')    # 8 Bytes of Hex

    return bytes.fromhex(posX) + bytes.fromhex(posY)


def getMoney(m):
    m = hex(m)[2:]
    m = PadData(m, 8, '0')          # 8 Bytes of Hex
    
    return bytes.fromhex(m)


def getNumOfFiles(n):
    n = hex(n)[2:]
    n = PadData(n, 8, '0') # 8 Bytes of Hex

    return bytes.fromhex(n)


def getFileSystemData(fileDictionary, dateList, sizeList):
    fileNames   = list(fileDictionary)
    fileData    = list(fileDictionary.values())
    fileSystem  = b''

    for i in range(len(fileDictionary)):
        padedFileName   = PadData(fileNames[i], 256, ' ')
        padedFileData   = PadData(fileData[i], 10240, ' ')
        padedFileSize   = PadData(sizeList[i], 4, ' ')
        
        Name            = padedFileName.encode()        # Padded Filename 256 Bytes
        Date            = dateList[i].encode()          # Date(string data).
        Size            = padedFileSize.encode()        # ~~MB 
        Data            = padedFileData.encode()        # Paded Filedata 1024 Bytes

        fileSystem     += Name + Date + Size + Data

    return fileSystem


def PadData(Data, Len, Pad):
    if len(Data) < Len:
        Data = ((Len - len(Data)) * Pad) + Data
    
    return Data



def metaData():
    '''
    need information
    1. domain       => actual domain name.  (string data)
    2. position     => position data        (tuple data)
    3. money        => actual money number  (integer data)
    4. files        => files of domain      (dictionary data)
    5. dates        => date of each files   (list of strings data)
    6. sizes        => size of each files

    '''    

    '''
    Localhost =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    '''

    # << localhost >> ----------------------------------------------------------------------------------------------------------    
    localhost_domain    = 'localhost'
    localhost_pos       = (739, 364)
    localhost_posT      = (744, 369)
    localhost_money     = 2000
    localhost_files     = { 'sysinfo.txt'               : ( 'Owner       : SecuMaster\n'+
                                                            'Univ. Addr  : South Korea, Mokpo National University\n'+
                                                            'OS          : Windows 7\n'),
                            'capital.docx'              : ( 'Classification - Capital No.01\n'+
                                                            'URL(Domain)    - atm.secumaster.net\n'+
                                                            'Location       - South Korea, Mokpo National University\n')
                        }
    localhost_dates     = [ '2018-05-17 02:20:13',
                            '2016-04-03 14:50:37']
    localhost_sizes     = [ '100',
                            '6000']



    '''
    Bank Domains  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
    secumaster ATM
    design ATM
    design ATM2
    whoami ATM
    whoami ATM2
    '''

    # << secumaster atm >> -----------------------------------------------------------------------------------------------------
    secumaster_atm_domain   = 'atm . secumaster . net'
    secumaster_atm_pos      = (725, 230)
    secumaster_atm_posT     = (730, 235)
    secumaster_atm_money    = 10000
    secumaster_atm_files    = { 'sysinfo.txt'               : ( 'Owner       : SecuMaster\n'+
                                                                'Univ. Addr  : South Korea, Mokpo National University\n'+
                                                                'OS          : Windows 7\n'),
                                'customers.db'              : ( '-----------------------------------------------------------\n'+
                                                                '| Index     | User Name             | Transaction Date    |\n'+
                                                                '-----------------------------------------------------------\n'+
                                                                '| 001       | kkamikoon             | 2014-10-08 13:26:33 |\n'+
                                                                '| 002       | 3210w0                | 2016-09-18 09:36:21 |\n'+
                                                                '| 003       | Zairo                 | 2016-09-21 17:50:01 |\n'+
                                                                '| 004       | Nirone7               | 2016-11-13 19:13:43 |\n'+
                                                                '| 005       | UBUN                  | 2016-11-13 19:05:31 |\n'+
                                                                '| 006       | liberte97             | 2017-04-06 11:21:08 |\n'+
                                                                '| 007       | clon3                 | 2017-07-30 21:02:50 |\n'+
                                                                '| 008       | beee44                | 2017-08-01 07:31:18 |\n'+
                                                                '| 009       | hmn2218               | 2018-07-05 20:15:27 |\n'+
                                                                '-----------------------------------------------------------\n')
                            }
    secumaster_atm_dates    = [ '2016-08-19 12:10:53',
                                '2017-07-05 20:15:27' ]
    secumaster_atm_sizes    = [ '100',
                                '900' ]


    # << design atm >> ---------------------------------------------------------------------------------------------------------
    design_atm_domain       = 'atm . design . net'
    design_atm_pos          = (185, 250)
    design_atm_posT         = (190, 255)
    design_atm_money        = 30000
    design_atm_files        = { 'sysinfo.txt'               : ( 'Owner       : Design firm, Inc.\n'+
                                                                'Inc Addr    : United States(America), Los Angeles\n'+ 
                                                                'OS          : Windows 7\n'),
                                'customers.db'              : ( '-----------------------------------------------------------\n'+
                                                                '| Index     | User Name             | Transaction Date    |\n'+
                                                                '-----------------------------------------------------------\n'+
                                                                '| 001       | Coco Chanel           | 1994-06-13 14:13:51 |\n'+
                                                                '| 002       | Donna Karan           | 1997-02-18 05:27:52 |\n'+
                                                                '| 003       | Giorgio Armani        | 2002-09-17 03:29:34 |\n'+
                                                                '| 004       | Calvin Klein          | 2005-09-23 06:57:07 |\n'+
                                                                '| 005       | Donatella Versace     | 2007-12-27 16:21:36 |\n'+
                                                                '| 006       | Ralph Lauren          | 2007-12-27 16:21:36 |\n'+
                                                                '| 007       | Christian Dior        | 2008-02-13 03:23:05 |\n'+
                                                                '| 008       | Tom Ford              | 2010-12-05 16:05:44 |\n'+
                                                                '| 009       | Pierre Cardin         | 2012-01-17 18:20:02 |\n'+
                                                                '| 010       | Yves Saint Laurent    | 2012-06-14 18:53:01 |\n'+
                                                                '| 011       | Christian Louboutin   | 2012-07-25 23:48:48 |\n'+
                                                                '| 012       | Karl Lagerfeld        | 2013-06-17 23:15:50 |\n'+
                                                                '| 013       | Roberto Cavalli       | 2013-10-17 01:34:41 |\n'+
                                                                '| 014       | Marc Jacobs           | 2014-06-19 18:14:26 |\n'+
                                                                '| 015       | Betsey Johnson        | 2014-07-01 21:46:29 |\n'+
                                                                '| 016       | Sandy Powell          | 2016-05-11 09:13:33 |\n'+
                                                                '| 017       | Domenico Dolce (R)    | 2017-02-03 16:34:31 |\n'+
                                                                '| 018       | Stefano Gabbana       | 2017-12-28 00:48:19 |\n'+
                                                                '-----------------------------------------------------------\n')
                            }
    design_atm_dates        = [ '2014-01-13 11:59:13',
                                '2017-12-28 00:48:19' ]
    design_atm_sizes        = [ '100',
                                '1800' ]


    # << design atm2 >> --------------------------------------------------------------------------------------------------------
    design2_atm_domain      = 'atm2 . design . net'
    design2_atm_pos         = (285, 230)
    design2_atm_posT        = (290, 235)
    design2_atm_money       = 85000
    design2_atm_files       = { 'sysinfo.txt'               : ( 'Owner       : Design Corperation, Inc.\n'+
                                                                'Inc Addr    : United States(America), New York\n'+ 
                                                                'OS          : Windows XP'),
                                'customers.db'              : ( '-----------------------------------------------------------\n'+
                                                                '| Index     | User Name             | Transaction Date    |\n'+
                                                                '-----------------------------------------------------------\n'+
                                                                '| 001       | Alexander McQueen     | 1995-10-17 19:33:40 |\n'+
                                                                '| 002       | Valentino Garavani    | 1996-01-06 10:58:13 |\n'+
                                                                '| 003       | Miuccia Prada         | 1997-04-06 07:56:50 |\n'+
                                                                '| 004       | Tommy Hilfiger        | 1997-09-12 23:33:00 |\n'+
                                                                '| 005       | Carolina Herrera      | 1999-03-08 13:52:02 |\n'+
                                                                '| 006       | Jean-Paul Gaultier    | 1999-06-09 01:26:26 |\n'+
                                                                '| 007       | Herve Leger           | 2000-02-23 09:09:06 |\n'+
                                                                '| 008       | Stella McCartney      | 2001-10-28 03:44:30 |\n'+
                                                                '| 009       | Ralph Rucci           | 2003-12-25 10:33:32 |\n'+
                                                                '| 010       | Salvatori Ferragamo   | 2004-07-11 03:02:28 |\n'+
                                                                '| 011       | Jimmy Choo            | 2005-11-30 20:06:02 |\n'+
                                                                '| 012       | Alexandre Herchovitch | 2006-03-31 08:25:01 |\n'+
                                                                '| 013       | Mossimo Giannulli     | 2007-06-30 22:51:29 |\n'+
                                                                '| 014       | John Varvatos         | 2008-10-18 08:59:49 |\n'+
                                                                '| 015       | Jonathan Jony Ive     | 2010-05-01 21:09:48 |\n'+
                                                                '| 016       | Kate Spade            | 2010-11-03 13:38:37 |\n'+
                                                                '| 017       | Christian Audigier    | 2011-01-13 05:53:33 |\n'+
                                                                '| 018       | Allegra Versace       | 2011-08-06 19:53:53 |\n'+
                                                                '-----------------------------------------------------------\n')
                            }
    design2_atm_dates       = [ '2004-03-01 05:10:43',
                                '2011-08-06 19:53:53' ]
    design2_atm_sizes       = [ '100',
                                '1800' ]


    # << whoami atm >> ---------------------------------------------------------------------------------------------------------
    whoami_atm_domain       = 'atm . whoami . net'
    whoami_atm_pos          = (460, 205)
    whoami_atm_posT         = (465, 210)
    whoami_atm_money        = 70000
    whoami_atm_files        = { 'sysinfo.txt'               : ( 'Owner       : Whoami Hacker-group.\n'+
                                                                'Inc Addr    : German, Berlin\n'+ 
                                                                'OS          : Ubuntu_18.04_i386\n'),
                                'customers.db'              : ( '-----------------------------------------------------------\n'+
                                                                '| Index     | User Name             | Transaction Date    |\n'+
                                                                '-----------------------------------------------------------\n'+
                                                                '| 001       | Benjamin Engel        | 2013-12-13 13:01:40 |\n'+
                                                                '| 002       | Max                   | 2013-12-31 21:33:08 |\n'+
                                                                '| 003       | Stefan                | 2014-01-27 05:01:22 |\n'+
                                                                '| 004       | Tommy Hilfiger        | 2014-01-30 19:30:13 |\n'+
                                                                '| 005       | Paul                  | 2014-02-23 04:23:20 |\n'+
                                                                '-----------------------------------------------------------\n')
                            }

    whoami_atm_dates        = [ '2018-06-13 18:15:32',
                                '2014-02-23 04:23:20' ]
    whoami_atm_sizes        = [ '100',
                                '500' ]


    # << whoami atm2 >> --------------------------------------------------------------------------------------------------------
    whoami2_atm_domain      = 'atm2 . whoami . net'
    whoami2_atm_pos         = (455, 190)
    whoami2_atm_posT        = (460, 195)
    whoami2_atm_money       = 95000
    whoami2_atm_files       = { 'sysinfo.txt'               : ( 'Owner       : Whoami Hacker-group.\n'+
                                                                'Inc Addr    : German, Hamburg\n'+ 
                                                                'OS          : Ubuntu 18:04\n'),
                                'customers.db'              : ( '-----------------------------------------------------------\n'+
                                                                '| Index     | User Name             | Transaction Date    |\n'+
                                                                '-----------------------------------------------------------\n'+
                                                                '| 001       | Marie                 | 2013-12-21 07:02:57 |\n'+
                                                                '| 002       | Hannah Lindbergh      | 2014-01-01 12:34:13 |\n'+
                                                                '-----------------------------------------------------------\n')
                            }
    whoami2_atm_dates       = [ '2018-06-19 17:26:10',
                                '2014-01-01 12:34:13' ]
    whoami2_atm_sizes       = [ '100',
                                '200' ]


    ATM = [  [secumaster_atm_domain,    secumaster_atm_pos,     secumaster_atm_posT,    secumaster_atm_money,   secumaster_atm_files,   secumaster_atm_dates,   secumaster_atm_sizes],
             [design_atm_domain,        design_atm_pos,         design_atm_posT,        design_atm_money,       design_atm_files,       design_atm_dates,       design_atm_sizes],
             [design2_atm_domain,       design2_atm_pos,        design2_atm_posT,       design2_atm_money,      design2_atm_files,      design2_atm_dates,      design2_atm_sizes],
             [whoami_atm_domain,        whoami_atm_pos,         whoami_atm_posT,        whoami_atm_money,       whoami_atm_files,       whoami_atm_dates,       whoami_atm_sizes],
             [whoami2_atm_domain,       whoami2_atm_pos,        whoami2_atm_posT,       whoami2_atm_money,      whoami2_atm_files,      whoami2_atm_dates,      whoami2_atm_sizes],
          ]


    '''
    Company Domains =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
    Design
    Paradox
    Phantasm
    '''

    # << design company >> -----------------------------------------------------------------------------------------------------
    design_company_domain   = 'www . design . com'
    design_company_pos      = (275, 240)
    design_company_posT     = (280, 245)
    design_company_money    = 5000
    design_company_files    = { 'sysinfo.txt'               : ( 'Owner       : Design firm, Inc.\n'+
                                                                'Inc Addr    : United States(America), Washington D.C.\n'+ 
                                                                'OS          : Debian-9.5.0-amd64\n'),
                                'users.db'                  : ( '-----------------------------------------------------------\n'+
                                                                '| Index     | User Name             | Sign-Up Date        |\n'+
                                                                '-----------------------------------------------------------\n'+
                                                                '| 001       | Pamella Homovec       | 2016-01-03 03:15:37 |\n'+
                                                                '| 002       | Simonne Ottie         | 2016-02-27 10:29:35 |\n'+
                                                                '| 003       | Lilla Leonardi        | 2016-03-02 11:18:34 |\n'+
                                                                '| 004       | Karylin Flory         | 2016-03-19 00:28:47 |\n'+
                                                                '| 005       | Nari Hofmann          | 2016-03-22 09:46:48 |\n'+
                                                                '| 006       | Jaquenette Elisabet   | 2016-04-08 12:32:58 |\n'+
                                                                '| 007       | Goldi Novak           | 2016-05-29 12:52:34 |\n'+
                                                                '| 008       | Lusa Abernathy        | 2016-06-08 09:25:47 |\n'+
                                                                '| 009       | Pauly Dupin           | 2016-06-08 17:10:29 |\n'+
                                                                '| 010       | Callida Fulbright     | 2016-06-20 08:47:55 |\n'+
                                                                '| 011       | Trix Livia            | 2016-07-06 16:29:28 |\n'+
                                                                '| 012       | Valina Sassan         | 2016-08-09 22:20:47 |\n'+
                                                                '| 013       | Kyla Nisse            | 2016-09-09 19:29:12 |\n'+
                                                                '| 014       | Ana Matejka           | 2016-09-28 15:57:52 |\n'+
                                                                '| 015       | Mireielle Yorker      | 2016-11-03 14:36:18 |\n'+
                                                                '| 016       | Katleen Haskell       | 2016-11-11 13:03:29 |\n'+
                                                                '| 017       | Ivett Groark          | 2016-12-22 09:25:55 |\n'+
                                                                '| 018       | Miquela Kelci         | 2017-01-13 12:41:05 |\n'+
                                                                '| 019       | Martica Arnulfo       | 2017-02-17 11:38:22 |\n'+
                                                                '| 020       | Ulrikaumeko Spense    | 2017-02-28 16:42:17 |\n'+
                                                                '| 021       | Sofie Golter          | 2017-03-14 00:54:52 |\n'+
                                                                '| 022       | Quentin Craig         | 2017-04-21 18:57:10 |\n'+
                                                                '| 023       | Phylys Rick           | 2017-04-28 07:29:56 |\n'+
                                                                '| 024       | Lissa Hacker          | 2017-04-28 18:28:50 |\n'+
                                                                '| 025       | Henrieta Hintze       | 2017-04-29 06:08:30 |\n'+
                                                                '| 026       | Gennie Suk            | 2017-05-15 09:01:11 |\n'+
                                                                '| 027       | Saidee Dev            | 2017-05-23 03:15:42 |\n'+
                                                                '| 028       | Ailene Padget         | 2017-06-03 05:03:14 |\n'+
                                                                '| 029       | Waly Strader          | 2017-06-11 09:13:17 |\n'+
                                                                '| 030       | Ethelin Nadya         | 2017-06-24 03:49:01 |\n'+
                                                                '| 031       | Janice Bridges        | 2017-07-03 08:38:24 |\n'+
                                                                '| 032       | Karly Amund           | 2017-07-14 13:09:28 |\n'+
                                                                '| 033       | Amy Ciri              | 2017-08-12 02:12:56 |\n'+
                                                                '| 034       | Ruthi Pittel          | 2017-09-15 13:01:35 |\n'+
                                                                '| 035       | Constantine Fortna    | 2017-10-29 03:26:49 |\n'+
                                                                '| 036       | Simonette Juli        | 2017-12-04 08:16:52 |\n'+
                                                                '| 037       | Wylma Hicks           | 2018-01-03 01:48:52 |\n'+
                                                                '| 038       | Anderea Meisel        | 2018-01-11 08:49:27 |\n'+
                                                                '| 039       | Cathi Whitaker        | 2018-02-05 03:14:35 |\n'+
                                                                '| 040       | Emmaline Brigid       | 2018-02-16 16:43:56 |\n'+
                                                                '| 041       | Shirlene Millwater    | 2018-02-26 09:51:43 |\n'+
                                                                '| 042       | Rosalind McCulloch    | 2018-03-13 05:00:32 |\n'+
                                                                '| 043       | Dawn Coussoule        | 2018-03-13 11:57:14 |\n'+
                                                                '| 044       | Albina Mariele        | 2018-03-23 23:24:45 |\n'+
                                                                '| 045       | Korie Timmons         | 2018-04-14 03:59:04 |\n'+
                                                                '| 046       | Roanna Wilmott        | 2018-04-19 15:16:55 |\n'+
                                                                '| 047       | Barbra Pestana        | 2018-04-28 07:36:19 |\n'+
                                                                '| 048       | Katrinka Bucella      | 2018-05-20 13:49:48 |\n'+
                                                                '| 049       | Lauryn Binnie         | 2018-06-08 06:21:21 |\n'+
                                                                '| 050       | Joice Sonstrom        | 2018-06-17 07:36:20 |\n'+
                                                                '-----------------------------------------------------------\n'),
                                'cooperative_firm.docx'     : ( 'Brand          - Paradox, Inc.\n'+
                                                                'URL(Domain)    - www.paradox.com\n'+
                                                                'Brand Value    - 190 million $\n'+
                                                                'Brand Location - German, Munchen.\n'
                                                                '\n'+
                                                                'Brand          - Phantasm-film, Inc.\n'+
                                                                'URL(Domain)    - www.phantasm.com\n'+
                                                                'Brand Value    - 36 million $\n'+
                                                                'Brand Location - United Kingdom(England), Birmingham.\n'
                                                                ),    
                                'capital.docx'              : ( 'Classification - Capital No.01\n'+
                                                                'URL(Domain)    - atm.design.net\n'+
                                                                'Location       - United States(America), Los Angeles\n'+
                                                                '\n'+
                                                                'Classification - Capital No.02\n'+
                                                                'URL(Domain)    - atm2.design.net\n'+
                                                                'Location       - United States(America), New York\n'
                                                                ),
                                'classfied.docx'            : ( 'Project Name   : < Social Artistry >\n'+
                                                                '\n'+
                                                                'Project Date   : 2017-12-17 08:59:53\n'+
                                                                '\n'+
                                                                'Capital From   : atm2.design.net\n'+
                                                                'Contents       : Social Artistry is the attempt to address or re\n'+
                                                                '                 cognize a particular social issue using art and\n'+
                                                                '                 creativity. Social artists are people who use c\n'+
                                                                '                 reative skills to work with people or organizat\n'+
                                                                '                 ions in their community to affect change. While\n'+
                                                                '                 a traditional artist uses their creative skills\n'+
                                                                '                 to express their take on the world, a social ar\n'+
                                                                '                 tist puts their skills to use to help promote  \n'+
                                                                '                 and improve communities. Thus, the main aim of \n'+
                                                                '                 a social artist is to improve society as a whol\n'+ 
                                                                '                 e and to help other people find their own means\n'+
                                                                '                 of creative expression.\n'
                                                                )
                            }
    design_company_dates    = [ '2017-05-26 10:50:12',
                                '2018-06-17 07:36:20',
                                '2018-01-11 20:17:51',
                                '2016-10-31 08:16:43',
                                '2017-12-17 08:59:53' ]
    design_company_sizes    = [ '100',
                                '5000',
                                '9000',
                                '1500',
                                '6000' ]


    # << paradox company >> ----------------------------------------------------------------------------------------------------
    paradox_company_domain  = 'www . paradox . com'
    paradox_company_pos     = (470, 200)
    paradox_company_posT    = (475, 205)
    paradox_company_money   = 65000
    paradox_company_files   = { 'sysinfo.txt'               : ( 'Owner       : Paradox-Engineering, Inc.\n'+
                                                                'Inc Addr    : German, Munchen.\n'+ 
                                                                'OS          : Ubuntu_14.04_amd64\n'),
                                'users.db'                  : ( '-----------------------------------------------------------\n'+
                                                                '| Index     | User Name             | Sign-Up Date        |\n'+
                                                                '-----------------------------------------------------------\n'+
                                                                '| 001       | Stanislaus Estele     | 2014-04-23 04:51:40 |\n'+
                                                                '| 002       | Morly Simona          | 2015-06-02 07:11:03 |\n'+
                                                                '| 003       | Wsan Annamaria        | 2015-06-15 16:34:41 |\n'+
                                                                '| 004       | Fulbright Alexis      | 2015-06-22 12:32:41 |\n'+
                                                                '| 005       | Kelleher Korella      | 2015-09-29 10:29:05 |\n'+
                                                                '| 006       | Loraine Zorina        | 2015-11-09 14:13:24 |\n'+
                                                                '| 007       | Jabez Codi            | 2015-12-30 15:29:23 |\n'+
                                                                '| 008       | Caresse Crissie       | 2016-01-31 11:04:17 |\n'+
                                                                '| 009       | Danuloff Robbi        | 2016-09-16 08:06:34 |\n'+
                                                                '| 010       | Burg Sari             | 2016-11-29 01:01:44 |\n'+
                                                                '| 011       | Hartnett La           | 2017-03-23 11:40:48 |\n'+
                                                                '| 012       | Waverly Miranda       | 2017-11-12 14:06:35 |\n'+
                                                                '| 013       | Drislane Tiertza      | 2017-12-15 07:22:42 |\n'+
                                                                '| 014       | Odrick Gertrude       | 2017-12-25 17:20:59 |\n'+
                                                                '| 015       | Wye Lorita            | 2018-01-08 22:01:43 |\n'+
                                                                '| 016       | Stempien Hazel        | 2018-04-07 11:28:24 |\n'+
                                                                '| 017       | Durstin Wilow         | 2018-05-25 05:27:34 |\n'+
                                                                '-----------------------------------------------------------'),
                                'cooperative_firm.docx'     : ( 'Brand          - Design firm, Inc.\n'+
                                                                'URL(Domain)    - www.design.com\n'+
                                                                'Brand Value    - 76 million $\n'+
                                                                'Brand Location - United States(America), Los Angeles\n'
                                                                ),    
                                'capital.docx'              : ( 'Classification - Capital No.01\n'+
                                                                'URL(Domain)    - atm.paradox.net\n'+
                                                                'Location       - \n'
                                                                ),
                                'contract.docx'             : ( '\n'+
                                                                '< TECHNOLOGY COOPERATION AGREEMENT >\n'+
                                                                '----------------------------------------------------\n'+
                                                                '\n'+
                                                                '(Build Enigma(Turing Machine) plan program.)\n'+
                                                                '----------------------------------------------------\n'+
                                                                '\n'+
                                                                'This \'Technology Cooperation Agreement\' made and enti\n'+
                                                                'red into as of the 20th day of December, 2011.\n'+
                                                                '\n'+
                                                                'Company        : Enigma-Turing, Inc.\n'+
                                                                'Company Addr   : United Kingdom(England), London\n'+
                                                                '\n'+
                                                                'A Turing machine is a mathematical model of computation\n'+
                                                                'that defines an abstract machine, which manipulates sym\n'+
                                                                'bols on a strip of tape according to a table of rules. \n'+
                                                                'Despite the model\'s simplicity, given any computer algo\n'+
                                                                'rithm, a Turing machine capable of simulating that algo\n'+
                                                                'rithm\'s logic can be constructed.\n'
                                                                )
                            }
    paradox_company_dates   = [ '2013-08-29 06:22:43',
                                '2014-01-09 11:47:32',
                                '2014-02-03 23:34:45',
                                '2016-10-12 13:37:54',
                                '2017-02-28 03:52:55' ]
    paradox_company_sizes   = [ '100',
                                '1700',
                                '9000',
                                '6000',
                                '7800' ]


    # << tutorial company >> ---------------------------------------------------------------------------------------------------
    tutorial_company_domain = 'www . tutorial . com'
    tutorial_company_pos    = (670, 250)
    tutorial_company_posT   = (675, 255)
    tutorial_company_money  = 10000
    tutorial_company_files  = { 'tutorial.txt'              : ( 'Owner       : kkamikoon.\n'+
                                                                'Addr        : Korea, Mokpo University MOAT.\n'),
                                'Hompage.list'              : ( '-----------------------------------------------------------\n'+
                                                                '| Index     | URL                   | Sign-Up Date        |\n'+
                                                                '-----------------------------------------------------------\n'+
                                                                '| 001       | kkamikoon.tistory.com | 2015-07-20 23:51:40 |\n'+
                                                                '-----------------------------------------------------------'),
                                'URL_Information'           : ( 'This Mission\'s URL List.\n'+
                                                                'localhost      - localhost          - [can scan]\n'+
                                                                'Paradox Inc.   - www.paradox.com    - [cannot scan]\n'+
                                                                'Design Inc.    - www.design.com     - [cannot scan]\n'+
                                                                'ATM(Design)    - atm.design.net     - [cannot scan]\n'+
                                                                'ATM(Secumaster)- atm.secumaster.net - [can scan]\n'
                                                                )
                            }
    tutorial_company_dates  = [ '2015-01-12 08:56:13',
                                '2016-07-22 13:41:52',
                                '2016-09-05 02:12:33']
    tutorial_company_sizes  = [ '100',
                                '900',
                                '3200']


    #int.from_bytes(bmoney, byteorder='big', signed=True)

    # domainInfo(domain, postion, money, files, dates, sizes):

    COMPANY = [ [design_company_domain,     design_company_pos,     design_company_posT,    design_company_money,   design_company_files,   design_company_dates,   design_company_sizes],
                [paradox_company_domain,    paradox_company_pos,    paradox_company_posT,   paradox_company_money,  paradox_company_files,  paradox_company_dates,  paradox_company_sizes],
                [tutorial_company_domain,   tutorial_company_pos,   tutorial_company_posT,  tutorial_company_money, tutorial_company_files, tutorial_company_dates, tutorial_company_sizes]
                ]



    # Build Function Start =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    domainInfo(localhost_domain, localhost_pos, localhost_posT, localhost_money, localhost_files, localhost_dates, localhost_sizes)

    for i in range(len(ATM)):
        domainInfo(ATM[i][0], ATM[i][1], ATM[i][2], ATM[i][3], ATM[i][4], ATM[i][5], ATM[i][6])

    for i in range(len(COMPANY)):
        domainInfo(COMPANY[i][0], COMPANY[i][1], COMPANY[i][2], COMPANY[i][3], COMPANY[i][4], COMPANY[i][5], COMPANY[i][6])



metaData()
