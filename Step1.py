import mysql.connector
import operator
import collections
import timeit
import copy


class Step1:
    __q0 = 0
    __gl = None
    __other = 0
    __window_size = 0
    __cog_functions_dictionary = None
    __function_cogs_dictionary = None
    __cogs_frequency = None
    __functions_frequency = None
    __grid = None

    def __init__(self, gl, other, q0, window):
        self.__gl = gl
        self.__other = other
        self.__q0 = q0
        self.__window_size = window
        two_dictionaries = Step1.gen_dictionary(gl)
        self.__cog_functions_dictionary = two_dictionaries[0]
        self.__function_cogs_dictionary = two_dictionaries[1]
        self.__cogs_frequency = Step1.gen_cogs_frequency(self.__cog_functions_dictionary)
        self.__functions_frequency = \
            Step1.gen_functions_frequency(self.__function_cogs_dictionary, self.__cogs_frequency)
        self.__grid = \
            Step1.get_bacteria_cog_map_to_glrcgs(self.__functions_frequency, self.__function_cogs_dictionary,
                                                 self.__window_size, self.__gl, self.__other, self.__cog_functions_dictionary)

    def get_q0(self):
        return self.__q0

    def set_q0(self, q0):
        self.__q0 = q0

    def get_gl(self):
        return self.__gl

    def set_gl(self, gl):
        self.__gl = gl

    def get_other(self):
        return self.__other

    def set_other(self, other):
        self.__other = other

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
    @staticmethod
    def get_bacteria_cog_map_to_glrcgs(functions_frequency_dictionary, function_cogs_dictionary, window, gl, other, cog_f_dict):
        glrcgs = dict()
        # generate grid of radius complied groups

        '''
        REAL GENERATION OF DWGS. UNCOMMENT AT THE END
        regular generation (no preprocess)
        '''
        dwgs = Step1.grid_of_double_window_groups(functions_frequency_dictionary, function_cogs_dictionary, window)


        '''
        JUST FOR CLARIFICATION - CAN BE REMOVED
        One time function to dump the dwgs to db
        # Step1.mysql_insert_values_double_window_groups(dwgs)
        '''

        '''
        TO BE USED JUST WHILE DEVELOPING. COMMENT IN/REMOVE WHEN FINISHED
        generation using preprocess (FASTER but fits only one case)
        
        dwgs = Step1.mysql_get_double_window_groups()
        '''

        glrcgs = Step1.grid_of_glrcgs(dwgs, window, gl, other, cog_f_dict)
        return glrcgs

    @staticmethod
    def grid_of_glrcgs(double_window_groups, window, gl, other, cog_f_dict):

        #initialize grid of glrcgs
        grid_of_glrcgs = dict()

        # for every centroid's double window group
        for bacteria, centroid_cogs in double_window_groups.items():

            # for every centroid
            for centroid_cog, cog_instances_in_bacteria in centroid_cogs.items():

                # for every instance of centroid_cog in the bacteria
                for surrounding_cogs_list in cog_instances_in_bacteria:

                    # check all its window size groups
                    centroid_glrcgs = Step1.centroid_glrcgs(centroid_cog, surrounding_cogs_list, window, gl, other, cog_f_dict)
                    grid_of_glrcgs_bac = grid_of_glrcgs.get(bacteria, False)
                    if not grid_of_glrcgs_bac:

                        grid_of_glrcgs[bacteria] = dict()

                    if bool(centroid_glrcgs):
                        if not grid_of_glrcgs[bacteria].get(centroid_cog, False):
                            grid_of_glrcgs[bacteria][centroid_cog] = [centroid_glrcgs]
                        else:
                            grid_of_glrcgs[bacteria][centroid_cog].append(centroid_glrcgs)

                # filter bacteria with no cogs
                Step1.filter_bacteria_with_no_cogs_from_grid(grid_of_glrcgs)

                # sort grid by bacteria
                grid_of_glrcgs = collections.OrderedDict(sorted(grid_of_glrcgs.items(), key=operator.itemgetter(0)))

        return grid_of_glrcgs

    @staticmethod
    def centroid_glrcgs(centroid_cog, surrounding_cogs_list, window, gl, other, cog_f_dict):

        tup_index_cog = 1
        tup_index_start = 2

        # initialize glrcgs list
        glrcgs = []

        # look for centroid cog tuple
        cog_tuple = [item for item in surrounding_cogs_list if item[tup_index_cog] == centroid_cog][0]

        # get global end position
        global_end = cog_tuple[tup_index_start] + window

        # go through surrounding cogs ordered by loc_start. for each such cog:
        for i in range(len(surrounding_cogs_list)):

            # clone GL
            temp_gl = dict(gl)
            temp_other = other

            # ignore cogs which bound double window boundaries
            if surrounding_cogs_list[i][tup_index_start] + window > global_end:
                continue

            #initialize glrcg i list
            glrcg_i = []

            # go through all cogs in the window that starts at i
            for j in range(i, len(surrounding_cogs_list)):

                # break when first cog bounds current window boundary
                if surrounding_cogs_list[j][tup_index_start] + window > global_end:
                    break

                # cog is in the boundaries
                glrcg_i.append(surrounding_cogs_list[j])

                # get cog functionalities
                functionalities = cog_f_dict.get(surrounding_cogs_list[j][tup_index_cog], False)

                # if surrounding cog doesn't have functionality from the GL
                if not functionalities:
                    # reduce from "other"
                    temp_other -= 1
                else:
                    # reduce every functionality from the grocery list
                    for f in functionalities:
                        temp_gl[f] -= 1

            # if GL is empty
            if Step1.check_empty_gl_and_other(temp_gl, temp_other):
                glrcgs.append(glrcg_i)


        return glrcgs

    @staticmethod
    def is_empty_gl(gl):
        is_empty_gl = True
        for f, q in gl.items():
            if gl[f] > 0:
                is_empty_gl = False
                break
        return is_empty_gl

    @staticmethod
    def is_empty_other(other):
        is_empty_other = other <= 0
        return is_empty_other

    @staticmethod
    def check_empty_gl_and_other(gl, other):
        is_empty_gl = Step1.is_empty_gl(gl)
        is_empty_other = Step1.is_empty_other(other)
        return is_empty_gl and is_empty_other


    @staticmethod
    def grid_of_double_window_groups(functions_frequency_dictionary, function_cogs_dictionary, window):

        # set timer
        start_function_time = timeit.default_timer()

        print('functionality frequency ' + str(functions_frequency_dictionary))

        # get lff
        least_frequent_functionality = list(functions_frequency_dictionary.items())[0][0]
        print('least_frequent_functionality: ' + least_frequent_functionality)

        # get lff's cogs
        list_of_seed_cogs = function_cogs_dictionary[least_frequent_functionality]
        print ('least of cogs with lowest frequency ' + str(list_of_seed_cogs))

        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()

        # build where clause
        where = "where cog IN"
        i = 1
        for cog in list_of_seed_cogs:
            if i == 1:
                where += "('{}',".format(cog)
            if i > 1:
                where += "'{}', ".format(cog)
            i += 1
        where = where[:-2] + ')'

        # build query
        query = "select `#bacteria`,`cog`,`loc_start`,`loc_end` from data5 " + where + \
                "ORDER BY `#bacteria`,`loc_start` ASC"

        # execute query
        cursor.execute(query)

        # initialize list of cogs
        list_of_tuples_represents_seed_cogs = []

        # add each result to dictionary
        for (bacteria, cog, loc_start, loc_end) in cursor:
            list_of_tuples_represents_seed_cogs.append((bacteria, cog, loc_start, loc_end))

        # stop timer to see how long it took to create seed cogs
        stop_time = timeit.default_timer()
        print("Took " + str(
            stop_time - start_function_time) + " seconds to create list_of_tuples_represents_seed_cogs with " + str(
            len(list_of_tuples_represents_seed_cogs)) + " records")

        # create double window groups
        print("Creating double window groups using list_of_tuples_represents_seed_cogs:")

        # f = open('workfile.txt', 'w+')
        bacteria_cog_hashmap_dic = {}

        # start timer for GLRCG
        start_time = timeit.default_timer()
        for seed in list_of_tuples_represents_seed_cogs:
            print('seed:' + str(seed))
            bacteria_name = seed[0]
            start_value = seed[2]
            end_value = seed[3]

            # prepare where clause
            where2 = " where data5.`#bacteria`='{}' AND data5.`loc_start`>={}-{} AND data5.`loc_end`<={}+{}". \
                format(bacteria_name, end_value, window, start_value, window)

            # build query
            query = "select `#bacteria`,`cog`,`loc_start`,`loc_end` from data5" + where2 + " ORDER BY `#bacteria`,`loc_start` ASC"

            # start timer for bacteria_cog_hashmap_dic creation
            start_time = timeit.default_timer()

            # execute query
            cursor.execute(query)

            # initialize cog GLRCG list
            cog_GLRCGs = []

            for (bacteria, cog, loc_start, loc_end) in cursor:
                cog_GLRCGs.append((bacteria, cog, loc_start, loc_end))

            # if there are'nt any COGs/X's around seed return only itself.
            b1 = bacteria_cog_hashmap_dic.get(seed[0], False)
            if not b1:
                bacteria_cog_hashmap_dic[seed[0]] = dict()

            c1 = bacteria_cog_hashmap_dic[seed[0]].get(seed[1], False)
            if not c1:
                bacteria_cog_hashmap_dic[seed[0]][seed[1]] = dict()
                bacteria_cog_hashmap_dic[seed[0]][seed[1]] = [cog_GLRCGs]
            else:
                bacteria_cog_hashmap_dic[seed[0]][seed[1]].append(cog_GLRCGs)

            stop_time = timeit.default_timer()
            # f.write("**************************************************************************\n")
            print("Took " + str(stop_time - start_time) + " seconds to create " + seed[1] + '_' + str(
                seed[0]) + " seed group \n")
            # f.write("Took " + str(stop_time - start_time) + " seconds to create " + seed[1] + '_' +str(seed[0]) +  " seed group \n")
            # f.write("Entries around seed within "+ str(window) + " radius: " + str(cog_GLRCGs) +"\n")
        # close mysql objects
        cursor.close()
        cnx.close()
        # f.close()
        stop_function_time = timeit.default_timer()
        print("Took " + str(stop_function_time - start_function_time) + " seconds to create bacteria_cog_hashmap_dic")

        # sort bacteria_cog_hashmap_dic by bacteria
        bacteria_cog_hashmap_dic = collections.OrderedDict(sorted(bacteria_cog_hashmap_dic.items(), key=operator.itemgetter(0)))

        return bacteria_cog_hashmap_dic

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
            '''
                "FROM temp_cogs_classification as t " \
                "Inner JOIN cogs_frequency as c ON t.cog = c.cog " \
            '''

                # build query
            query = "select * from `cogs_classification3` where `classification` like '%{}%' ".format(c)

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

        # build query
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

        # delete classification-cogs temp table
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
    def mysql_insert_values_double_window_groups(dwgs):

        '''
        inserts double window groups values to mysql table for future use
        :param dwgs: hashmap of (DICT bacteria => (DICT centroid_cog => LIST [surrounding_cog_id => TUPLE (bacteria, surrounding_cog, loc_start, loc_end))]
        :return: void. 
        '''

        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()

        i = 1

        # for every centroid's double window group
        for bacteria, centroid_cogs in dwgs.items():

            # for every centroid
            for centroid_cog, surrounding_cogs_list in centroid_cogs.items():

                for s_cog_tuple in surrounding_cogs_list:

                    # tuple as list
                    l = list(s_cog_tuple)
                    l.insert(1, centroid_cog)

                    # build query
                    query = "INSERT INTO %s (%s) VALUES (%s)" % (
                        'double_window_groups', 'bacteria, centroid, s_cog, s_cog_start, s_cog_end',  ",".join("'" + str(v) + "'" for v in l))

                    # execute query
                    cursor.execute(query)

                    print("executed " + str(i))
                    i += 1

        # close mysql objects
        cursor.close()
        cnx.close()



    @staticmethod
    def mysql_get_double_window_groups():
        # initialize mysql objects
        cnx = mysql.connector.connect(user='root', database='fullptt_prophageannotation')
        cursor = cnx.cursor()

        # build query
        query = "SELECT * FROM double_window_groups ORDER BY bacteria, s_cog_start"

        # execute query
        cursor.execute(query)

        # initialize dictionary
        d = dict()

        # add each result to dictionary
        for (bacteria, centroid, s_cog, s_cog_start, s_cog_end) in cursor:

            # build tuple
            tuple = (bacteria, s_cog, s_cog_start, s_cog_end)

            # build centroid => surrounding cogs dictionary (centroid already exists)


            if bacteria in d:
                if centroid in d[bacteria]:
                    d[bacteria][centroid].append(tuple)
                else:
                    d[bacteria][centroid] = [tuple]
            else:
                d[bacteria] = dict()
                d[bacteria][centroid] = [tuple]

        # close mysql objects
        cursor.close()
        cnx.close()

        d = collections.OrderedDict(sorted(d.items(), key=operator.itemgetter(0)))
        return d

    @staticmethod
    def filter_bacteria_with_no_cogs_from_grid(grid):
        d = copy.deepcopy(grid)
        for bacteria, cogs in d.items():
            if len(cogs) == 0:
                del grid[bacteria]






