from ast import literal_eval
from Step1 import Step1
from collections import OrderedDict
import operator
import winsound
# input
'''
gl = literal_eval(input("Please enter the data: "))
window = input("Enter the radius: ")
q0 = input("Enter the genomes quorum: ")
'''

# create step 1 object
#[("flagellar",1),("methylase ",2),("GTP",1),("kinase",1),("tf",1)]
gl = [("flagellar",1),("methylase",2),("GTP",1),("kinase",1),("tf",1)]
q0 = 1
window = 5000
step1 = Step1(gl, q0, window)
#playing an audio file screams I'm done.
winsound.PlaySound('Done.wav', winsound.SND_FILENAME)

#print(step1.get_grid())
#print(sorted(step1.get_functions_frequency().items(), key=operator.itemgetter(1)))
#print(sorted(step1.get_cogs_frequency().items(), key=operator.itemgetter(1)))
#print(step1.get_functions_frequency())
#print(step1.get_cogs_frequency())









# create COGs classification dictionary

# generate the cogClassification dictionary to a file.



