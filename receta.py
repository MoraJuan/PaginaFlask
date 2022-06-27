class ClaseUsuario:
    __receta = None

    def __init__(self):
        self.__receta = None

    def __del__(self):
        self.__receta = None

    def addReceta(self, receta):
        self.__receta = receta

    def getReceta(self):
        return self.__receta