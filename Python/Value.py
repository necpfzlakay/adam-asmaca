class Value:
    def __init__(self,value,category,diffLevel) -> None:
        self.__value = value
        self.__category = category
        self.__diffLevel = diffLevel
    def getValue(self):
        return self.__value
    def getCategory(self):
        return self.__category
    def getDiffLevel(self):
        return self.__diffLevel