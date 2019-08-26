class LocalGLRCGElement:
    __cog_number = -1
    __pointers = None

    def __init__(self, cog_number, pointers):
        self.__cog_number = cog_number
        self.__pointers = pointers

    def get_cog_number(self):
        return self.__cog_number

    def set_cog_number(self, cog_number):
        self.__cog_number = cog_number

    def get_pointers(self):
        return self.__pointers

    def set_pointers(self, pointers):
        self.__pointers = pointers


