from LocalGLRCGElement import LocalGLRCGElement
import collections


class LocalGLRCG:
    __func_to_localglrcgelements = None
    __cog_functions_dictionary = None
    __glrcg_id = None

    def __init__(self, glrcg_id, functionalities, cog_functions_dictionary):
        self.__glrcg_id = glrcg_id
        self.__cog_functions_dictionary = cog_functions_dictionary
        l = []
        for f in functionalities:
            l.append((f, []))
        l.append(("other", []))
        self.__func_to_localglrcgelements = collections.OrderedDict(l)

    def get_func_to_localglrcgelements(self):
        return self.__func_to_localglrcgelements

    def get_cog_functions_dictionary(self):
        return self.__cog_functions_dictionary

    def get_functionality_next_indices(self):
        d = dict()
        structure = self.get_func_to_localglrcgelements().items()
        for f, elements_list in structure:
            d[f] = len(elements_list)
        return d

    def cog_has_functionality(self, cog_number, f):
        cog_functions_dictionary = self.get_cog_functions_dictionary()
        cog_functions = cog_functions_dictionary.get(cog_number, False)

        if (cog_functions) and (f in cog_functions):
            return True
        else:
            return False

    def add_cog_instance(self, cog_number, n2f):
        func_to_localglrcgelements = self.get_func_to_localglrcgelements()
        f_indices = self.get_functionality_next_indices()

        for f1, elements in func_to_localglrcgelements.items():

            if (f1 is not "other") and (not self.cog_has_functionality(cog_number, f1)):
                continue

            pointers = []
            i = 0

            for f2 in func_to_localglrcgelements.keys():
                if self.cog_has_functionality(cog_number, f2) or (f2 is "other"):
                    # connect f1 to f2
                    pointers.append((n2f[i], f_indices[f2]))
                else:
                    pointers.append((n2f[i], -1))
                i += 1
            pointers = collections.OrderedDict(pointers)
            lge = LocalGLRCGElement(cog_number, pointers)

            l = func_to_localglrcgelements.get(f1, False)
            if not l:
                func_to_localglrcgelements[f1] = [lge]
            else:
                func_to_localglrcgelements[f1].append(lge)












