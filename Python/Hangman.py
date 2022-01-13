from random import randint
from os import getcwd, path, system
import sys
import msvcrt
import pyfiglet

from Python.Value import Value
import pandas as pd

GAMESCREEN = f"""
"""
class Hangman:

    databaseLoc = getcwd() +  fr'\Database\database.csv'
    __score = 0
    __winStat = False
    __numberOfLives = 10
    __values = [] 
    __chosenWord = "None"
    __chosenWordList = []
    __lenChosenWord = 0
    __isLoadDatabase = False
    __selectedWords = []
    __chosenWordLetters = dict()
    __enteredLetters = []
    __knownLetters = []
    __remLetterCount = 0 # kalan harf sayisi
    __detailTextList = []
    def __init__(self,pcName,diff = 1):
        self.__pcName = pcName
        self.__diff = diff
        self.__loadDatabase()

    def changeDatabaseLocation(self,databaseLoc):
        if path.exists(databaseLoc):
            self.databaseLoc = databaseLoc
            self.__loadDatabase()
        else:
            print('File not exists')

    def changeDiff(self,diff):
        self.__diff = diff

    def getDiff(self):
        return self.__diff

    def __loadDatabase(self):
        if path.exists(self.databaseLoc):
            csv_reader = pd.read_csv(self.databaseLoc, delimiter=',')
            for value,category,diffLevel in csv_reader.values:
                myObj = Value(value,category,diffLevel)
                self.__values.append(myObj)
            self.__isLoadDatabase = True
        else:
            print('File not exists')
    
    def __chooseWord(self):
        control = True
        while control:
            if len(self.__selectedWords) == len(self.__values):
                self.__selectedWords.clear()
            

            zorlukSeviyesiOyunSeviyesiIleAynıOlanlarinSayisi = 0 # Değişken ismi için kusura bakmayın bulamadım :)
            for value in self.__values:
                diffLevel = value.getDiffLevel()
                if diffLevel == self.__diff:
                    zorlukSeviyesiOyunSeviyesiIleAynıOlanlarinSayisi += 1
            if len(self.__selectedWords) == zorlukSeviyesiOyunSeviyesiIleAynıOlanlarinSayisi:
                self.__selectedWords.clear()


            randomValue = self.__getRandomValue()
            selectedObj = self.__values[randomValue]
            selectedValue = selectedObj.getValue()
            if selectedValue in self.__selectedWords:
                control = True
            else:

                if selectedObj.getDiffLevel() == self.__diff:
                    control = False
                    self.__chosenWord = selectedValue
                    for i in self.__chosenWord:
                        if not i in self.__chosenWordList:
                            self.__chosenWordList.append(i)
                        iValue = self.__chosenWordLetters.get(i,-1)
                        if iValue == -1:
                            self.__chosenWordLetters[i] = 1
                        else:
                            self.__chosenWordLetters[i] += 1
                    
                    self.__addDetailText(f"Kategori: {selectedObj.getCategory()}")
                    self.__printDetailText()
                    self.__lenChosenWord = len(selectedValue)
                    self.__remLetterCount = self.__lenChosenWord
                    self.__selectedWords.append(self.__chosenWord)
                else:
                    control = True




    def __getRandomValue(self)->int:
        return randint(0,len(self.__values)-1)

    def __printGameScreen(self):
        print(f"\n\n\n\n\n\n")
        print("\t\t\t",end=" ")
        for i in self.__chosenWord:
            if i in self.__knownLetters:
                print(i,end=" ")
            else:
                print("_",end=" ")

        print(f"\nEntered Letters: {','.join(self.__enteredLetters)}\n")

    def __printWinScreen(self):
        self.__calculateScore()
        print(pyfiglet.figlet_format(f'WIN'))
        print(f"SCORE: {self.__score}")
        print("press any key to return to the main menu and  'q' for exit")
        inputText = msvcrt.getwch()
        if inputText == 'q':
            exit()
        else:
            self.__resetGame()

    def __printLoseScreen(self):
        self.__calculateScore()
        print(pyfiglet.figlet_format(f'LOSE'))
        print(f"SCORE: {self.__score}")
        print("press any key to return to the main menu and 'q' for exit")
        inputText = msvcrt.getwch()
        if inputText == 'q':
            exit()
        else:
            self.__resetGame()
    


    def __printDetailText(self):
        system('cls')
        self.__printGameScreen()
        self.__smartDelete()
        for i in self.__detailTextList:
            print(i)

    def __smartDelete(self):
        loseTextList = []
        minLoseInt = 999
        for index,i in enumerate(self.__detailTextList):
            if "Maalesef" in i:
                iInt = int(i.replace('Maalesef yanlış seçim, ',"").replace(' hakkın kaldı.',""))
                if iInt < minLoseInt:
                    minLoseInt = iInt
                loseTextList.append((index,iInt))
        for index, j in loseTextList:
            if j != minLoseInt:
                self.__detailTextList.pop(index)
        
        

    def __addDetailText(self,text):
        self.__detailTextList.append(text)

    def __getLetter(self):

        bannedASCII = [224,46,44,34,60,62,48,49,50,51,52,53,54,55,56,57,45,42,47]
        letter = msvcrt.getwch()
        letter = letter.lower().strip()
        control = False
        for ascii in bannedASCII:
            if ord(letter) == ascii:
                control= True

        if len(letter ) == 1: #CHECK LETTER LENGHT
            if not control:
                if letter in self.__chosenWordList:
                    self.__chosenWordList.remove(letter)
                    lenLetter = self.__chosenWordLetters.get(letter,-1)
                    self.__addDetailText(f"Evet doğru bildin, {letter} harfinden {lenLetter} tane var.")
                    if not letter in self.__enteredLetters:
                        self.__enteredLetters.append(letter)
                    self.__remLetterCount -= lenLetter
                    self.__knownLetters.append(letter)
                else:
                    if not letter in self.__enteredLetters:
                        self.__enteredLetters.append(letter)
                    self.__numberOfLives -=1
                    self.__addDetailText(f"Maalesef yanlış seçim, {self.__numberOfLives} hakkın kaldı.")
            iInt = 0
            for i in self.__detailTextList:
                if "Kalan harf sayısı: " in i:
                    iInt = int(i.replace('Kalan harf sayısı: ',""))
            if iInt != self.__remLetterCount:
                self.__addDetailText(f"Kalan harf sayısı: {self.__remLetterCount}")


    def __checkWinStatus(self):
        if self.__remLetterCount == 0 and self.__numberOfLives >= 0:
            self.__winStat = True
            self.__printWinScreen()
            
        else:
            self.__winStat = False
            self.__printLoseScreen()
            


    def __resetGame(self):
        self.__chosenWordList.clear()
        self.__score = 0
        self.__winStat = False
        self.__numberOfLives = 10
        self.__lenChosenWord = 0
        self.__chosenWordLetters = dict()
        self.__enteredLetters.clear()
        self.__knownLetters.clear()
        self.__remLetterCount = 0 # kalan harf sayisi
        self.__detailTextList.clear()

    def __calculateScore(self):
        winLoseCont = 25 # kaybettiyse 25 puan
        if self.__winStat:
            winLoseCont = 100 # kazandıysa 100 puan

        lifeCont = self.__numberOfLives * 15 # kalan can sayısının 15 katı puan

        # Burada ise bilinen kelimede kaç tane tekrar eden harf var onu kontrol ediyoruz.
        # Örneğin adana kelimesini ele alalım. 
        # Adana da 3 tane a var bundan dolayı ilk A için 10 ikinci ve ücüncü için 5 puan alıyor.
        # Kısaca tahmin edilmesi gereken kelimede bir harf birden fazla varsa fazlalıklar için az puan alıyor.

        letterCont = 0
        for letter in self.__knownLetters:
            letterCount = self.__chosenWordLetters.get(letter,-1)
            if letterCount != -1:
                if letterCount == 1:
                    letterCont += 10
                elif letterCount > 1:
                    letterCont += (letterCont -1 * 5) + 10

        #kelime ne kadar uzunsa 5 katı kadar fazladan puan alıyor
        lenCont = self.__lenChosenWord * 5
        self.__score = winLoseCont + lifeCont + letterCont + lenCont

    def startGame(self):
        if self.__isLoadDatabase:
            system('cls')
            self.__chooseWord()
            # self.__printGameScreen()
            whileControl = True
            while whileControl:
                if self.__numberOfLives == 0:
                    whileControl = False
                    self.__checkWinStatus()
                elif self.__remLetterCount == 0:
                    whileControl = False
                    self.__checkWinStatus()
                else:
                    self.__getLetter()
                self.__printDetailText()

        else:
            print("Error (database error)")
        
