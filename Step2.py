from Step1 import Step1
from LocalGLRCG import LocalGLRCG
import copy
import operator
import collections


class Step2(Step1):
    __sorted_gl = None
    __bac_glrcgs_map = None
    __func_lfflevel_map = None
    __lfflevel_func_map = None
    __ce = None
    __enum_structure = None
    __ge = None
    __gene_teams = []

    def __init__(self, gl, other, q0, window):
        super(Step2, self).__init__(gl, other, q0, window)

        # sort GL
        self.__sorted_gl = Step2.make_ordered_dict_by_lff_from_gl(Step2.get_gl(self),
                                                                  Step2.get_functions_frequency(self))
        # func_lfflevel_map + lfflevel_func_map
        func_lfflevel_maps = Step2.gen_func_lff_level_maps(self.get_functions_frequency())
        self.__func_lfflevel_map = func_lfflevel_maps[0]
        self.__lfflevel_func_map = func_lfflevel_maps[1]

        parent_index = -1

        # generate the cogs dictionary and enum_structure
        structures = \
            Step2.gen_structures(self.get_grid(),
                                 self.get_cog_functions_dictionary(),
                                 self.get_functions_frequency(),
                                 self.get_func_lfflevel_map(),
                                 self.get_lfflevel_func_map())
        self.__ce = structures[0]
        self.__enum_structure = structures[1]
        self.__ge = structures[2]
        self.__bac_glrcgs_map = structures[3]

        # set left_bacteria
        left_bacteria = [len(self.get_bac_glrcgs_map())]

        # set path
        path = []

        # set others array
        others_array = Step2.gen_others_array(self.get_ge())

        # set gene_teams
        self.__gene_teams = []

        # get other requirement
        other_requirement = self.get_other()

        Step2.gen_gene_teams(parent_index,
                             self.get_bac_glrcgs_map(),
                             left_bacteria,
                             q0,
                             self.get_enum_structure(),
                             self.get_sorted_gl(),
                             path,
                             others_array,
                             self.get_gene_teams(),
                             other_requirement,
                             self.get_func_lfflevel_map(),
                             self.get_ce())

    def print_gene_teams(self):

        # open file
        f = open('results.txt', 'w+')

        # get the glrcg enumeration dictionary
        ge = self.get_ge()

        # set indices in the glrcg
        bac_index = 0
        cog_number_index = 1
        cog_start_index = 2
        cog_end_index = 3

        # initialize result counter
        i = 1
        for item in self.get_gene_teams():
            path = item[0]
            glrcgs = item[1]

            f.write("**************************************************************************\n")
            f.write("result number " + str(i) +"\n")
            f.write("cogs: " + str(path) + "\n")
            f.write("groups: " + "\n")
            for glrcg_id in glrcgs:
                glrcg_data = ge[glrcg_id]

                # take bacteria info from 1st element of glrcg
                first_glrcg_index = 0
                bacteria = glrcg_data[first_glrcg_index][bac_index]

                f.write(bacteria + ": ")

                for cog in glrcg_data:
                    cog_number = cog[cog_number_index]
                    f.write(str(cog_number) + "  ")

                f.write("\n")
            f.write("\n\n")
            i += 1
        f.close()

    def get_sorted_gl(self):
        return self.__sorted_gl

    def get_func_lfflevel_map(self):
        return self.__func_lfflevel_map

    def get_lfflevel_func_map(self):
        return self.__lfflevel_func_map

    def get_bac_glrcgs_map(self):
        return self.__bac_glrcgs_map

    def get_ce(self):
        return self.__ce

    def get_ge(self):
        return self.__ge

    def get_enum_structure(self):
        return self.__enum_structure

    def get_gene_teams(self):
        return self.__gene_teams

    @staticmethod
    def gen_gene_teams(parent_index, bac_glrcg_map, left_bacteria, q0, enum_structure, gl, path, others_array,
                       gene_teams, other_requirement, func_lfflevel_map, ce):
        print(parent_index)
        # not enough bacteria to complete requirements
        if not Step2.enough_bacteria_left(left_bacteria, q0):
            return

        # gl requirement is ok. check others requirement
        if Step2.is_empty_gl(gl):
            return Step2.check_others_requirement(
                bac_glrcg_map, left_bacteria, q0, path, others_array, gene_teams, other_requirement)

        gl_copy = copy.deepcopy(gl)
        lff = Step2.get_next_gl_component(gl_copy)

        i_start = Step2.calc_i_start(parent_index, lff, enum_structure, func_lfflevel_map)
        i_end = Step2.calc_i_end(lff, enum_structure, func_lfflevel_map)

        for cog_id in range(i_start, i_end+1):
            cog_number_index = 1
            cog_number = ce[cog_id][cog_number_index]

            # copy modified elements for next iteration
            bac_glrcg_map_copy = copy.deepcopy(bac_glrcg_map)
            path_copy = copy.deepcopy(path)
            others_array_copy = copy.deepcopy(others_array)
            left_bacteria_copy = copy.deepcopy(left_bacteria)

            path_copy.append(cog_number)

            Step2.remove_cog_instance_from_bac_glrcgs_map(bac_glrcg_map_copy, lff, cog_number, others_array_copy,
                                                          left_bacteria_copy)

            Step2.gen_gene_teams(
                cog_id, bac_glrcg_map_copy, left_bacteria_copy, q0, enum_structure, gl_copy, path_copy,
                others_array_copy, gene_teams, other_requirement, func_lfflevel_map, ce)

    @staticmethod
    def check_others_requirement(bac_glrcg_map, left_bacteria, q0, path, others_array, gene_teams, other_requirement):

        # not enough bacteria to complete requirements
        if not Step2.enough_bacteria_left(left_bacteria, q0):
            return
        if other_requirement is 0:
            survivors = Step2.survivor_glrcgs(bac_glrcg_map)
            gene_teams.append([path, survivors])
            return

        other_requirement -= 1
        for cog_number, count in others_array.items():
            if cog_number != "-" and count >= q0:
                bac_glrcg_map_copy = copy.deepcopy(bac_glrcg_map)
                others_array_copy = copy.deepcopy(others_array)
                left_bacteria_copy = copy.deepcopy(left_bacteria)
                path_copy = copy.deepcopy(path)
                path_copy.append(cog_number)

                Step2.remove_cog_instance_from_bac_glrcgs_map(bac_glrcg_map_copy, "other", cog_number,
                                                              others_array_copy, left_bacteria_copy)

                Step2.check_others_requirement(bac_glrcg_map_copy, left_bacteria_copy, q0, path_copy, others_array_copy
                                         , gene_teams, other_requirement)

        '''
        
    others_array = others_array -1
    for cog_number in others_array:
        if cog_number > = q0:
              update_bac_glrcg_map(bac_glrcg_map, cog_number, "other" , others_array)
              continue_to_others(bac_glrcg_map, left_bacteria,q0,Path,others_array,gene_teams, other)

    '''
    @staticmethod
    def remove_cog_instance_from_bac_glrcgs_map(bac_glrcg_map, lff, cog_number, others_array, left_bacteria):
        bac_glrcg_map_copy = copy.deepcopy(bac_glrcg_map)

        for bac_copy, local_glrcg_dict_copy in bac_glrcg_map_copy.items():
            bac = bac_copy
            local_glrcg_dict = bac_glrcg_map[bac]
            local_glrcg_dict_copy = copy.deepcopy(local_glrcg_dict)
            for glrcg_id_copy, local_glrcg_copy in local_glrcg_dict_copy.items():
                glrcg_id = glrcg_id_copy
                local_glrcg = local_glrcg_dict[glrcg_id]
                Step2.remove_elements(bac_glrcg_map, bac, local_glrcg, glrcg_id, lff, cog_number, others_array,
                                      left_bacteria)

    @staticmethod
    def enough_bacteria_left(left_bacteria, q0):
        return left_bacteria[0] >= q0

    @staticmethod
    def gen_structures(grid, cog_functions_dictionary, functions_frequency_dictionary, f2n, n2f):

        # get functionalities
        functionalities = list(functions_frequency_dictionary.keys())

        # bac_glrcgs_dict
        bac_glrcgs_dict = dict()

        # initialize glrcg enumeration dictionary
        ge_dict = dict()
        ge_index = 0

        cogid_index_in_tuple = 1
        # if beneficial - take into consideration cogs frequency order. That will require some DB work

        d_n = dict()
        d_n_with_all_cog_info = dict()
        i = 0
        for f, freq in functions_frequency_dictionary.items():
            d_n[i] = []
            d_n_with_all_cog_info[i] = []
            i += 1
        d_n[i] = []
        d_n_with_all_cog_info[i] = []

        # go over the grid add all cogs
        for bac, cogs in grid.items():

            bac_glrcgs_dict[bac] = dict()

            for centroid, centroid_appearances in cogs.items():

                for centroid_appearance in centroid_appearances:

                    for glrcg in centroid_appearance:

                        # glrcg enumeration
                        ge_dict[ge_index] = glrcg

                        # initiazize glrcg entry in bac_glrcgs_dict
                        local_glrcg = LocalGLRCG(ge_index, functionalities, cog_functions_dictionary)

                        for cog in glrcg:
                            cog_id = cog[cogid_index_in_tuple]

                            # add cog instance to the local glrcg structure
                            if cog_id != "-":
                                local_glrcg.add_cog_instance(cog_id, n2f)


                            # TODO decide what to do with unknown ("-") cogs
                            if cog_id == "-":
                                continue
                            elif cog_functions_dictionary.get(cog_id, False):
                                for f in cog_functions_dictionary[cog_id]:
                                    if cog_id not in d_n[f2n[f]]:
                                        d_n[f2n[f]].append(cog_id)
                                        d_n_with_all_cog_info[f2n[f]].append(cog)

                            else:
                                if cog_id not in d_n[f2n["other"]]:
                                    d_n[f2n["other"]].append(cog_id)
                                    d_n_with_all_cog_info[f2n["other"]].append(cog)

                        bac_glrcgs_dict[bac][ge_index] = local_glrcg
                        ge_index += 1

        # we need to sort d_n_with_all_cog_info in lff order
        d_n = collections.OrderedDict(sorted(d_n.items(), key=operator.itemgetter(0)))
        d_n_with_all_cog_info = collections.OrderedDict(
            sorted(d_n_with_all_cog_info.items(), key=operator.itemgetter(0)))

        # every functional cog is also classified as "other"
        func_as_other_list_cogids = []
        func_as_other_list_cogs = []
        for func_order, cog_list in d_n_with_all_cog_info.items():
            if func_order < len(d_n_with_all_cog_info) - 1:
                for cog in cog_list:
                    cog_id = cog[cogid_index_in_tuple]
                    func_as_other_list_cogids.append(cog_id)
                    func_as_other_list_cogs.append(cog)
        d_n[f2n["other"]] = func_as_other_list_cogids + d_n[f2n["other"]]
        d_n_with_all_cog_info[f2n["other"]] = func_as_other_list_cogids + d_n_with_all_cog_info[f2n["other"]]

        # generate the cog enumeration structure
        ce = dict()
        ce_reverse = dict()

        # first give ids to all different cogs
        all_cogs_in_list = []
        i = 0
        for func_order, cog_list in d_n_with_all_cog_info.items():
            for cog in cog_list:
                if cog[cogid_index_in_tuple] not in all_cogs_in_list:
                    all_cogs_in_list.append(cog[cogid_index_in_tuple])
                    ce[i] = cog
                    ce_reverse[cog[cogid_index_in_tuple]] = i
                    i += 1

        # second, convert d_n to list of ids instead of cog_ids
        for func_order, cog_list in d_n.items():
            enum_list = []
            for cog in cog_list:
                enum_list.append(ce_reverse[cog])
            d_n[func_order] = enum_list

        ce = collections.OrderedDict(sorted(ce.items(), key=operator.itemgetter(0)))
        d_n = collections.OrderedDict(sorted(d_n.items(), key=operator.itemgetter(0)))

        return [ce, d_n, ge_dict, bac_glrcgs_dict]

    @staticmethod
    def make_ordered_dict_by_lff_from_gl(gl, functions_frequency_dict):
        # go through the ordered functions frequency dictionary.
        # find the equivalent functionality from GL and put it in a list.
        # eventually create an ordered dict from that list
        dict_gl = dict(gl)
        l = []
        for func, freq in functions_frequency_dict.items():
            for grocery, amount in dict_gl.items():
                if grocery == func:
                    l.append((grocery, amount))

        returned_dict = collections.OrderedDict(l)
        return returned_dict

    @staticmethod
    def gen_func_lff_level_maps(functions_frequency_dictionary):
        f2n = dict()
        n2f = dict()
        i = 0
        for f, freq in functions_frequency_dictionary.items():
            f2n[f] = i
            n2f[i] = f
            i += 1
        f2n["other"] = i
        n2f[i] = "other"

        return [f2n, n2f]

    @staticmethod
    def gen_others_array(ge):
        d = dict()
        cog_number_index = 1
        for glrcg_id, cog_list in ge.items():
            for cog in cog_list:
                cog_number = cog[cog_number_index]
                current_count = d.get(cog_number, False)
                if not current_count:
                    d[cog_number] = 1
                else:
                    d[cog_number] += 1

        return d

    @staticmethod
    def get_next_gl_component(gl):
        groceries = list(gl.items())
        first_grocery = groceries[0]
        functionality = first_grocery[0]
        amount = first_grocery[1]
        if amount == 1:
            del gl[functionality]
        return functionality

    @staticmethod
    def calc_i_start(parent_index, lff, enum_structure, func_lfflevel_map):

        # get first id of lff
        lff_cog_list = enum_structure[func_lfflevel_map[lff]]
        # TODO check if there exists a case where there's no first_id (None value)
        first_id = next(iter(lff_cog_list), None)

        # different functionality from parent
        if first_id >= parent_index + 1:
            return first_id

        # same functionality as parent
        else:
            return parent_index + 1

    @staticmethod
    def calc_i_end(lff, enum_structure, func_lfflevel_map):
        # get last element of the lff id
        lff_cog_list = enum_structure[func_lfflevel_map[lff]]
        last_id = lff_cog_list[-1]
        return last_id

    @staticmethod
    def remove_elements(bac_glrcg_map, bac, local_glrcg, glrcg_id, lff, cog_number, others_array, left_bacteria):
        is_found = False
        f2lmap = local_glrcg.get_func_to_localglrcgelements()
        list_of_glrcg_elements = f2lmap[lff]

        for element in list_of_glrcg_elements:
            if element is not None:
                element_cog_number = element.get_cog_number()

                # cog instance was found
                if cog_number == element_cog_number:
                    is_found = True
                    # get pointers of element
                    pointers = element.get_pointers()

                    # go through instance pointers
                    for f, p in pointers.items():
                        if p is not -1:
                        # modify the p item in f list None
                            f2lmap[f][p] = None
            if is_found:
                break

        if is_found:
            Step2.update_others_array(others_array, cog_number)
            if Step2.all_glrcg_elements_are_none(local_glrcg):
                Step2.remove_local_glrcg_from_structure(bac_glrcg_map, bac, glrcg_id, left_bacteria)
        else:
            Step2.remove_glrcg_from_bac(bac_glrcg_map, bac, glrcg_id, others_array, local_glrcg, left_bacteria)

        '''
            search in  localGLRCG.map[lff] list for cog_number
            if cog_number found:
                remove cog_number from localGLRCG element (should read more about pythons pointers)
                update_others_array(others_array,cog_number)
            else:
            update the others_array such that all intances of localGLRCG  are discarded
                bac.remove[localGLRCG]
            if bac.isEmpty:
                left_bacteria =   left_bacteria - 1
        '''

    @staticmethod
    def update_others_array(others_array, cog_number):
        others_array[cog_number] -= 1



    @staticmethod
    def remove_glrcg_from_bac(bac_glrcg_map, bac, glrcg_index, others_array, local_glrcg, left_bacteria):
        # update others array - every cog in other is reduced by 1 in others array
        f2l = local_glrcg.get_func_to_localglrcgelements()
        list_of_other_elements = f2l["other"]
        for other_element in list_of_other_elements:
            if other_element is not None:
                cog_number = other_element.get_cog_number()
                Step2.update_others_array(others_array, cog_number)

        # remove local_glrcg_from_structure
        Step2.remove_local_glrcg_from_structure(bac_glrcg_map, bac, glrcg_index, left_bacteria)

    @staticmethod
    def all_glrcg_elements_are_none(local_glrcg):
        f2l = local_glrcg.get_func_to_localglrcgelements()
        list_of_other_elements = f2l["other"]
        for other_element in list_of_other_elements:
            if other_element is not None:
                return False
        return True

    @staticmethod
    def remove_local_glrcg_from_structure(bac_glrcg_map, bac, glrcg_index, left_bacteria):
        # remove the local glrcg structure from bac
        list_to_delete = bac_glrcg_map[bac]
        del list_to_delete[glrcg_index]

        # if bac has no glrcgs - remove bac
        if not bac_glrcg_map[bac]:
            del bac_glrcg_map[bac]
            left_bacteria[0] -= 1

    @staticmethod
    def survivor_glrcgs(bac_glrcg_map):
        r = []
        for bac, glrcg_dict in bac_glrcg_map.items():
            for glrcg_id, local_glrcg in glrcg_dict.items():
                r.append(glrcg_id)
        return r




'''
initialize all structures:
    parent_index - parent index (int). init: 0
    bac_glrcg_map - bac => list of LocalGLRCGElements
    left_bacteria - int representing number of bacteria
    q0 - min number of bacteria holding corrent GLRCGs
    enum_structure - cogs enumerated and grouped by their functionalities. lff groups come first.
                    each cog enumeration is paired with its cog id. Only GL cogs.
    GL - GL as a dictionary sorted by lff.
    path - all ancestor cogs list ordered top-down. init: []
    others_array - sum of all instances over all survivor GLRCGS so far.
                    Only Step 1 Survivor cogs are counted.
                    init: go over the bac_glrcg_map and count appearances
    gene_teams - list of gene_teams, gene_team items (init : [])
    note : gene_team item - [path,list of left GLRCGs IDs]

Recursive Algorithm
void gen_gene_teams (parent_index, bac_glrcg_map, left_bacteria,q0,enum_structure,GL,Path,others_array,gene_teams, other):
    if(left_bacteria<q0):
        return;

    if gl is empty, meaning it's complied (note others are yet to check):
        continue_to_others(bac_glrcg_map, left_bacteria,q0,Path,others_array,gene_teams, other)

    lff <- get next GL component from GL (also reduces GL relevent component by 1)

    i_start <- calc_i_start (parent_index, GL)
    i_end <- calc_i_end (parent_index, GL)

    for id from i_start to i_end:
        update_bac_glrcg_map(bac_glrcg_map, enum_structure[lff][id], lff, others_array)
        gen_gene_teams(parent_index, bac_glrcg_map, left_bacteria,q0,enum_structure,GL,Path,others_array,gene_teams, other)

update_bac_glrcg_map(bac_glrcg_map, lff, cog_number,others_array):
    for bac in bac_glrcg_map:
        for localGLRCG in bac:
            remove_elements(bac, localGLRCG, lff, cog_number ,others_array)

remove_elements(bac, localGLRCG, lff, cog_number,others_array):
    search in  localGLRCG.map[lff] list for cog_number
    if cog_number found:
        remove cog_number from localGLRCG element (should read more about pythons pointers)
        update_others_array(others_array,cog_number)
    else:
        update the others_array such that all intances of localGLRCG  are discarded
        bac.remove[localGLRCG]
        if bac.isEmpty:
            left_bacteria =   left_bacteria - 1

update_others_array(others_array,elements):
    others_array[elements]= others_array[elements]-1

calc_i_start (parent_index, GL):
    lff <- first component of GL
    if enum_structure[lff].first() >= parent_index + 1
        return enum_structure[lff].first()
    else
        return parent_index + 1

calc_i_end (parent_index, GL):
    lff <- first component of GL
    enum[lff][len(enum[lff])-1[0] (the last element of the lff id. 0 coordinate is id. 1 coordinate is cog id)

continue_to_others(bac_glrcg_map, left_bacteria,q0,Path,others_array,gene_teams, other)

    if(left_bacteria<q0):
        return;

    if others == 0:
        gene_teams.add( gene_team item )
        return

    others_array = others_array -1
    for cog_number in others_array:
        if cog_number > = q0:
              update_bac_glrcg_map(bac_glrcg_map, cog_number, "other" , others_array)
              continue_to_others(bac_glrcg_map, left_bacteria,q0,Path,others_array,gene_teams, other)

'''