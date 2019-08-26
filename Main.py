from ast import literal_eval
from Step1 import Step1
from collections import OrderedDict
import operator
import Step1
from Step2 import Step2
import winsound

'''
gl = literal_eval(input("Please enter the data: "))
window = input("Enter the radius: ")
q0 = input("Enter the genomes quorum: ")
'''

# create step 1 object
#gl = [("flagellar", 1), ("methylase", 2), ("GTP", 1), ("kinase", 1), ("tf", 1)] LEFTOVERS FROM DAVID


#gl = [("H;METABOLISM", 1)]
gl = [("kinase", 1), ("tf", 1)]
other = 1

q0 = 10
window = 10000
step2 = Step2(gl, other, q0, window)
step2.print_gene_teams()

#playing an audio file screams I'm done.
winsound.PlaySound('Done.wav', winsound.SND_FILENAME)

#print(step1.get_grid())
#print(sorted(step1.get_functions_frequency().items(), key=operator.itemgetter(1)))
#print(sorted(step1.get_cogs_frequency().items(), key=operator.itemgetter(1)))
#print(step1.get_functions_frequency())
#print(step1.get_cogs_frequency())









# create COGs classification dictionary

# generate the cogClassification dictionary to a file.



