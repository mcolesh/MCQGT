from ast import literal_eval
from Step1 import Step1
from collections import OrderedDict
import operator

# input
'''gl = literal_eval(input("Please enter the data: "))
d = input("Enter the radius: ")
q0 = input("Enter the genomes quorum: ")'''

# create step 1 object
gl = [("kinase",3),("tf",2)]
q0 = 1
d = 1500
step1 = Step1(gl, q0, d)
print(step1.get_cogs_frequency())
print(step1.get_functions_frequency())
#print(step1.get_grid())
#print(sorted(step1.get_functions_frequency().items(), key=operator.itemgetter(1)))
#print(sorted(step1.get_cogs_frequency().items(), key=operator.itemgetter(1)))

#print(step1.get_functions_frequency())
#print(step1.get_cogs_frequency())









# create COGs classification dictionary

# generate the cogClassification dictionary to a file.



