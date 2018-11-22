#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <windows.h>

#define TimePerCase0   20
#define TimePerCase1   20
#define TimePerDefault 20

enum {
  BLACK,     	 /*  0 : 까망 */
  DARK_BLUE,     /*  1 : 어두운 파랑 */
  DARK_GREEN,    /*  2 : 어두운 초록 */
  DARK_SKY_BLUE, /*  3 : 어두운 하늘 */
  DARK_RED,    	 /*  4 : 어두운 빨강 */
  DARK_VOILET,   /*  5 : 어두운 보라 */
  DARK_YELLOW,   /*  6 : 어두운 노랑 */
  GRAY,     	 /*  7 : 회색 */
  DARK_GRAY,     /*  8 : 어두운 회색 */
  BLUE,      	 /*  9 : 파랑 */
  GREEN,      	 /* 10 : 초록 */
  SKY_BLUE,    	 /* 11 : 하늘 */
  RED,           /* 12 : 빨강 */
  VIOLET,      	 /* 13 : 보라 */
  YELLOW,        /* 14 : 노랑 */
  WHITE,         /* 15 : 하양 */ 
};

// Function Defination=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
void textcolor(int);


// Main Function Start=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
int main(int argc, char* argv[])
{
	/*
	argv[0] 	= File name 		==> doesn't need to care and print.
	argv[1] 	= Case number 		==> case of print.
	argv[2]~ 	= Text to print 
	*/
	int i, j;
	char ch = 0x00;
	
	switch(atoi(argv[1]))
	{
		case 0:		// Game Over Message ------------------------------------
			system("mode con: cols=80 lines=7");
			for(i=2; i<argc; i++)
			{
				for(j=0; j<strlen(argv[i]); j++)
				{
					printf("%c", argv[i][j]);
					Sleep(TimePerCase0);
				}
				if(i >= 2)
				{
					textcolor(YELLOW);
					printf("\n--------------------------------------------------------------------------------");
					Sleep(TimePerDefault * 50);
				}
				printf("\n");
			}
			break;
			
			
		case 1:		// Help of game(like F1) --------------------------------
			system("mode con: cols=70 lines=40");
			for(i=2; i<argc; i++)
			{
				printf("%s", argv[i]);
				Sleep(TimePerCase1);
				
				// Set Text Color Yellow for explanation
				textcolor(YELLOW);
				
				printf("\n");
			}
			break;			
		
		
		default: 	// Mission Status printing -----------------------------
			system("mode con: cols=70 lines=15");
			for(i=2; i<argc; i++)
			{
				printf("%s", argv[i]);
				Sleep(TimePerDefault);
				
				if ( i == 2 || i == argc-1 ) // Target Abstract Printing
				{
					textcolor(YELLOW);
					printf("\n----------------------------------------------------------------------");
				}
				else if( i >= 4 && i < argc-1 ) // Target of Mission Data Printing
				{
					textcolor(DARK_YELLOW);
				}
				
				
				
				printf("\n");
			}
			break;			
	}
	
	textcolor(WHITE);
	printf("\nAre you exit this command prompt?(Y only)");
	while(ch != 0x79 && ch != 0x59)
	{
		ch = getch();	
	}
	
	return 0;
}

void textcolor(int color_number)
{
 SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),color_number);
};

