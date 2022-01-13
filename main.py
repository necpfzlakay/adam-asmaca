from re import T
import pyfiglet
import msvcrt
from keyboard import is_pressed
from os import system,environ

from colorama import Fore



from Python.Hangman import Hangman

menuSecenekler = ["Start Game","Change Difficulty","About Us","Exit"]
categories = ["Countries","Cities","Animals","Plants","Random"]
diffLevelList = ['Easy','Medium','Hard']
aboutUsText = """grubumuz hakkındaki mesaj"""
okBaslangic = 0
printOneTimeMenu = True
whileControl = True
pcName = environ['COMPUTERNAME']



if __name__ == "__main__":
    hangman = Hangman(pcName)
    while whileControl:
        if printOneTimeMenu:
            system('cls')
            print(Fore.BLUE + " ")
            print(pyfiglet.figlet_format('Bluecoder'))
            for index,i in enumerate(menuSecenekler):
                if index == okBaslangic:
                    print(f"\t\t> {i}")
                else:
                    print(f"\t\t{i}")
        printOneTimeMenu = False
        secim = msvcrt.getch()
        if secim == b"H": # PRESS UP
            if okBaslangic == 0:
                okBaslangic == len(menuSecenekler)-1
            else:
                okBaslangic-=1
            printOneTimeMenu = True
        elif secim == b"P": # PRESS DOWN
            if okBaslangic == len(menuSecenekler)-1:
                okBaslangic == 0
            else:
                okBaslangic+=1
            printOneTimeMenu = True
        elif secim == b'\x03': # PRESS CTRL C
            exit()
        elif secim == b'\r': # PRESS ENTER
            if okBaslangic ==0: # START GAME
                hangman.startGame()
                printOneTimeMenu=True
            elif okBaslangic ==1: # CHANGE DİFF
                printOneTimeMenu=False
                currentDiffLevel = hangman.getDiff()
                print(f"Current Difficulty: {diffLevelList[currentDiffLevel]}")
                for index,i in enumerate(diffLevelList,start=1):
                    print(f"{index}) {i} ",end="")
                try:
                    diffLevel = int(input('\nDiff Level: '))-1
                    print(f"New Difficulty: {diffLevelList[diffLevel]}")
                    hangman.changeDiff(diffLevel)
                    print("Press any key to continue.")
                    msvcrt.getch()
                    printOneTimeMenu=True
                except ValueError:
                    print('Check value')
                finally:
                    inputDiff = 1 
            elif okBaslangic ==2: # PRİNT ABOUT US TEXT
                print(aboutUsText)
                printOneTimeMenu=False
            elif okBaslangic ==3: #EXIT
                whileControl = False