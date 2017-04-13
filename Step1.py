import mysql.connector



class Step1:
    __q0 = 0
    __gl = None
    __radius = 0
    __cog_functions_dictionary = None
    __function_cogs_dictionary = None
    __cogs_frequency = None
    __functions_frequency = None
    # g1 example [("kinase",3),("tf",2)]
    def __init__(self,gl,q0, radius):
        self.__gl = gl
        self.__q0 = q0
        self.__radius = radius
        two_dictionaries = Step1.gen_dictionary(gl)
        self.__cog_functions_dictionary = two_dictionaries[0]
        self.__function_cogs_dictionary = two_dictionaries[1]
        self.__cogs_frequency = Step1.gen_cogs_frequency(self.__cog_functions_dictionary)
        #self.__functions_frequency = Step1.gen_function_frequency_dictionary()

    def get_q0(self):
        return self.__q0

    def set_q0(self, q0):
        self.__q0 = q0

    def get_gl(self):
        return self.__gl

    def set_gl(self, gl):
        self.__gl = gl

    def get_radius(self):
        return self.__radius

    def set_radius(self, radius):
        self.__radius = radius

    def get_cog_functions_dictionary(self):
        return self.__cog_functions_dictionary

    def set_cog_functions_dictionary(self, cog_functions_dictionary):
        self.__cog_functions_dictionary = cog_functions_dictionary

    def get_function_cogs_dictionary(self):
        return self.__function_cogs_dictionary

    def set_function_cogs_dictionary(self, function_cogs_dictionary):
        self.__function_cogs_dictionary = function_cogs_dictionary

    def get_cogs_frequency(self):
        return self.__cogs_frequency

    def set_cogs_frequency(self, cogs_frequency):
        self.__cogs_frequency = cogs_frequency

    @staticmethod
    def gen_dictionary(gl):
        # initialize dictionary
        d = dict()
        reverse_d = dict()

        # for every gl component
        for (c, q) in gl:

            # initialize mysql objects
            cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
            cursor = cnx.cursor()

            # build query
            query = "select * from `cogs_classification2` where `classification` like '%{}%' ".format(c)

            # execute query
            cursor.execute(query)

            # add each result to dictionary
            for (ID, classification) in cursor:
                if ID in d:
                    d[ID].append(c)
                else:
                    #This is a bug fix
                    d[ID] = [c]

                if c in reverse_d:
                    reverse_d[c].append(ID)
                else:
                    reverse_d[c] = [ID]

            # close mysql objects
            cursor.close()
            cnx.close()
        return [d, reverse_d]

    @staticmethod
    def gen_cogs_frequency(cog_functions_dictionary):
        # initialize dictionary
        d = dict()

        cogs = cog_functions_dictionary.keys()

        # initialize keys
        for key in cogs:
            d[key] = 0

        # initialize number of data examples - normalizer
        normalizer = 6634238

        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()

        # build query
        where = "where"
        i = 1
        for cog in cogs:
            if i == 1:
                where += " 'cog'='{}' ".format(cog)
            if i > 1:
                where += " OR 'cog'='{}' ".format(cog)
            i += 1
        query = "select `cog`, COUNT(*) as num from data " + where + "GROUP BY `cog` ORDER BY `num` ASC";

        # execute query
        cursor.execute(query)

        # add each result to dictionary
        for (cog, num) in cursor:
            d[cog] = num
            print("%{}%, %{}% ".format(cog, num))

        # close mysql objects
        cursor.close()
        cnx.close()

        return d









