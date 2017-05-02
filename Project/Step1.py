import mysql.connector
import operator
import collections
import timeit

class Step1:
    __q0 = 0
    __gl = None
    __window_size = 0
    __cog_functions_dictionary = None
    __function_cogs_dictionary = None
    __cogs_frequency = None
    __functions_frequency = None
    __grid = None

    # g1 example [("kinase",3),("tf",2),("a",1)]
    def __init__(self,gl,q0,window):
        self.__gl = gl
        self.__q0 = q0
        self.__window_size = window
        two_dictionaries = Step1.gen_dictionary(gl)
        self.__cog_functions_dictionary = two_dictionaries[0]
        self.__function_cogs_dictionary = two_dictionaries[1]
        self.__cogs_frequency = Step1.gen_cogs_frequency(self.__cog_functions_dictionary)
        self.__functions_frequency = \
            Step1.gen_functions_frequency(self.__function_cogs_dictionary, self.__cogs_frequency)
        self.__grid = Step1.get_bacteria_cog_map_to_GLRCGs(self.__functions_frequency, self.__function_cogs_dictionary,window)

    def get_q0(self):
        return self.__q0

    def set_q0(self, q0):
        self.__q0 = q0

    def get_gl(self):
        return self.__gl

    def set_gl(self, gl):
        self.__gl = gl

    def get_window_size(self):
        return self.__window_size

    def set_window_size(self, window_size):
        self.__window_size = window_size

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

    def get_functions_frequency(self):
        return self.__functions_frequency

    def set_functions_frequency(self, functions_frequency):
        self.__functions_frequency = functions_frequency

    def get_grid(self):
        return self.__grid

    def set_grid(self, grid):
        self.__grid = grid

    #This function generate <bacteria_x : COG_y hashmap> hashmap
    #COG_y hashmap - <COG_y : List of GLRCGs around COG_y in bacteria_x>
    #Note:(Grocery List and Radius Complied Groups) hashmap
    def get_bacteria_cog_map_to_GLRCGs(functions_frequency_dictionary,function_cogs_dictionary,window):
        start_function_time = timeit.default_timer()
        print('functionality frequency '+ str(functions_frequency_dictionary))
        least_frequent_functionality =(functions_frequency_dictionary.popitem(last=False))[0]
        print('least_frequent_functionality: '+least_frequent_functionality)
        list_of_seed_cogs = function_cogs_dictionary[least_frequent_functionality]
        print('least of cogs with lowest frequency ' + str(list_of_seed_cogs))
        #print("total number of COGs in list: " + str(len(list_of_seed_cogs)))
        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()
        where = "where cog IN"
        i = 1
        for cog in list_of_seed_cogs:
                if i == 1:
                    where += "('{}',".format(cog)
                if i > 1:
                    where += "'{}', ".format(cog)
                i+=1
        where=where[:-2]+')'
        # build query
        query = "select `#bacteria`,`cog`,`loc_start`,`loc_end` from data5 " + where + "ORDER BY `#bacteria`,`loc_start` ASC"
        # execute query
        cursor.execute(query)
        list_of_touples_represents_sead_cogs=[]
        # add each result to dictionary
        for (bacteria,cog,loc_start,loc_end) in cursor:
            list_of_touples_represents_sead_cogs.append((bacteria,cog,loc_start,loc_end))
        stop_time = timeit.default_timer()
        print("Took " + str(stop_time - start_function_time) + " seconds to create list_of_touples_represents_sead_cogs with " + str(len(list_of_touples_represents_sead_cogs)) + " records")
        #print("the seads list: " + str(list_of_touples_represents_sead_cogs))
        print("Creating GLRCGs using list_of_touples_represents_sead_cogs:")
        f = open('workfile.txt', 'w+')
        bacteria_cog_hashMap_dic = {}
        #sead (bacteria,cog,loc_start,loc_end) of relevant COGs we should search around
        start_time = timeit.default_timer()
        for sead in list_of_touples_represents_sead_cogs:
            print('sead:'+ str(sead))
            bacteria_name = sead[0]
            start_value = sead[2]
            end_value = sead[3]
            '''
                       This WHERE returns all records satisfing condition: (record.start=>start_value-r and record.end<=start_value) or (record.start=>end_value and record.start<=end_value+r)
            #-----<----r---x-(cog)----r--x-->-----
            WHERE1=" where data5.`#bacteria`='{}' AND ( ( (data5.`loc_start`>={}-{}) AND (data5.`loc_end`<={}) ) OR ( (data5.`loc_start` >={}) AND (data5.`loc_end`<={}+{}) ) )"
            .format(bacteria_name,start_value,window,start_value,end_value,end_value,window)
            
            WHERE2=" where data5.`#bacteria`='{}' AND data5.`loc_start`>={}-{} AND data5.`loc_end`<={}+{}".format( bacteria_name, end_value, window,start_value,window)
            WHERE3 = " where data5.`#bacteria`='{}' AND data5.`loc_start` BETWEEN  {}-{} AND {}+{}".format(
                bacteria_name, end_value, window, start_value, window)
            '''
            WHERE2=" where data5.`#bacteria`='{}' AND data5.`loc_start`>={}-{} AND data5.`loc_end`<={}+{}".format( bacteria_name, end_value, window,start_value,window)
            query = "select `#bacteria`,`cog`,`loc_start`,`loc_end` from data5" + WHERE2 + " ORDER BY `#bacteria`,`loc_start` ASC"
            start_time = timeit.default_timer()
            # execute query
            cursor.execute(query)
            cog_GLRCGs = []
            boolean = 1
            for (bacteria, cog, loc_start, loc_end) in cursor:
                '''
                if (loc_start>sead[3] and boolean==1):
                    cog_GLRCGs.append(sead)
                    boolean=0
                '''
                cog_GLRCGs.append((bacteria, cog, loc_start,loc_end))
            #if there are'nt any COGs/X's around sead return only itself.
            '''
            if not cog_GLRCGs:
                cog_GLRCGs.append(sead)
            '''
            if sead[0] not in bacteria_cog_hashMap_dic:
                bacteria_cog_hashMap_dic[sead[0]] = {}
                bacteria_cog_hashMap_dic[sead[0]][sead[1]]=cog_GLRCGs
            else:
                bacteria_cog_hashMap_dic[sead[0]][sead[1]]=cog_GLRCGs

            stop_time = timeit.default_timer()
            f.write("**************************************************************************\n")
            print("Took " + str(stop_time - start_time) + " seconds to create " + sead[1] + '_' +str(sead[0]) +  " sead group \n")
            f.write("Took " + str(stop_time - start_time) + " seconds to create " + sead[1] + '_' +str(sead[0]) +  " sead group \n")
            f.write("Entries around sead within "+ str(window) + " radius: " + str(cog_GLRCGs) +"\n")
        # close mysql objects
        cursor.close()
        cnx.close()
        f.close()
        stop_function_time = timeit.default_timer()
        print("Took " + str( stop_function_time - start_function_time) + " seconds to create bacteria_cog_hashMap_dic")
        return 1

    @staticmethod
    def gen_dictionary(gl):
        print("generating cog-functions dictionary and function-cogs dictionary")
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

        # create temporary classification-cogs table in the DB
        Step1.create_classification_cogs_table_in_db(cog_functions_dictionary)

        print("generating cogs frequency dictionary")
        start_time = timeit.default_timer()

        # initialize dictionary
        d = dict()

        cogs = cog_functions_dictionary.keys()

        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()

        #build query
        query = "SELECT DISTINCT t.cog, c.frequency " \
                "FROM temp_cogs_classification as t " \
                "Inner JOIN cogs_frequency as c ON t.cog = c.cog " \
                "ORDER BY `frequency`"
        # execute query
        cursor.execute(query)
        # add each result to dictionary
        for (cog, frequency) in cursor:
            d[cog] = frequency
        # close mysql objects
        cursor.close()
        cnx.close()

        d = collections.OrderedDict(sorted(d.items(), key=operator.itemgetter(1)))

        stop_time = timeit.default_timer()

        print("Took " + str(stop_time - start_time) + " seconds")

        #delete classification-cogs temp table
        Step1.mysql_delete_classification_cogs_table()
        return d


    @staticmethod
    def create_classification_cogs_table_in_db(cog_functions_dictionary):

        value_pairs = Step1.dict_to_mysql_value_pairs(cog_functions_dictionary)

        cols = ["`cog`", "`classification`"]

        Step1.mysql_create_classification_cogs_table()
        Step1.mysql_insert_values_classification_cogs_table(cols, value_pairs)

    @staticmethod
    def mysql_create_classification_cogs_table():

        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()

        # build query
        query = "CREATE TABLE temp_cogs_classification (cog VARCHAR(7), classification VARCHAR(94))"

        # execute query
        cursor.execute(query)

        # close mysql objects
        cursor.close()
        cnx.close()

    @staticmethod
    def mysql_insert_values_classification_cogs_table(col_names, value_pairs):

        #
        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()

        # build query
        query = "INSERT INTO %s (%s) VALUES %s" % (
            'temp_cogs_classification', ",".join(col_names), ",".join(value_pairs))

        # execute query
        cursor.execute(query)

        # close mysql objects
        cursor.close()
        cnx.close()

    @staticmethod
    def mysql_delete_classification_cogs_table():

        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()

        # build query
        query = "DROP TABLE temp_cogs_classification"

        # execute query
        cursor.execute(query)

        # close mysql objects
        cursor.close()
        cnx.close()


    @staticmethod
    def dict_to_mysql_value_pairs(d):
        records = []
        # build records of table
        for key, values in d.items():
            for value in values:
                records.append("('{}','{}')".format(key, value))
        return records


    @staticmethod
    def generate_orwhere_of_cogs(cogs):
        where = "where"
        i = 1
        for cog in cogs:
            if i == 1:
                where += " `cog`='{}' ".format(cog)
            if i > 1:
                where += " OR `cog`='{}' ".format(cog)
            i += 1
        return where

    @staticmethod
    def gen_functions_frequency(functions_cog_dictionary,cogs_frequency_dictionary):
        print("generating functions frequency dictionary")

        # initialize dictionary
        d = dict()

        # for every function in functions_cog_dictionary
        for func in functions_cog_dictionary:
            # get cogs list
            cog_list = functions_cog_dictionary[func]
            # sum cogs frequency
            func_frequency = 0
            for cog in cog_list:
                func_frequency += cogs_frequency_dictionary[cog]
            # update function frequency
            d[func] = func_frequency
        d = collections.OrderedDict(sorted(d.items(),key=operator.itemgetter(1)))
        return d



    @staticmethod
    def gen_grid(cog_list, window_size):

        # create temp table to store records (#bateria, loc_start, loc_end, cog) of cogs from GL (denote as t)

        # create nested query in this fashion:
            # select all records from `data_sorted_by_bac_and_locstart` (denote as s) s.t.:
                # select all records from t
            # where s.#bacteria=t.#bacteria AND
        #       ( s.loc_start >= t.loc_start + window_size - 1 OR s.loc_end <= t.loc_end - window_size + 1)

        # save results as a dictionary with 2 keys (bacteria + loc_start) if such thing is possible in python

        # delete the temp table

        '''    
                print("generating pre-grid")
        # initialize pregrid (contains just LFF (Lowest Frequency Functionality) COGS)
        pre_grid = dict()

        # generate orwhere of cogs
        where = Step1.generate_orwhere_of_cogs(cog_list)

        #build query
        query = "select `from data5 " + where + \
                "ORDER BY `#bacteria`,`loc_start` ASC"

        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()

        # execute query
        cursor.execute(query)

        # add each result to pregrid
        for (bac, cog, start, end) in cursor:
            if bac in pre_grid:
                pre_grid[bac].append([cog, start, end])
            else:
                pre_grid[bac] = [[cog, start, end]]

        # close mysql objects

        cursor.close()
        cnx.close()

        # generate grid from pre grid
        grid = Step1.gen_grid_from_pregrid(pre_grid, window_size)

        return grid
        
        '''


    @staticmethod
    def gen_grid_from_pregrid(pre_grid, window_size):
        print("generating grid")
        # initialize grid
        grid = dict()

        # generate orwhere of cogs
        where = Step1.generate_where_of_cogs_surrounding_lff_cogs(pre_grid, window_size)

        #build query
        query = "select `#bacteria`,`cog`,`loc_start`,`loc_end` from data5 " + where + \
                "ORDER BY `#bacteria`,`loc_start` ASC"

        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()

        # execute query
        cursor.execute(query)

        # add each result to dictionary
        for (bac, cog, start, end) in cursor:
            if bac in d:
                grid[bac].append([cog, start, end])
            else:
                grid[bac] = [[cog, start, end]]

        # close mysql objects
        cursor.close()
        cnx.close()

        return grid

    @staticmethod
    def generate_where_of_cogs_surrounding_lff_cogs(pre_grid, window_size):
        where = "where"
        i = 1
        for bac, cogs in pre_grid.items():
            for cog_record in cogs:
                if i == 1:
                    where += " (`#bacteria`='{}' AND (`loc_start`>='{}' OR `loc_end`<='{}')) ".\
                        format(bac, cog_record[1] - window_size + 1, cog_record[2] + window_size - 1)
                if i > 1:
                    where += " OR (`#bacteria`='{}' AND (`loc_start`>='{}' OR `loc_end`<='{}')) ". \
                        format(bac, cog_record[1] - window_size + 1, cog_record[2] + window_size - 1)
                i += 1
        return where








