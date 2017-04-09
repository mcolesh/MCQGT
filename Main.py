from ast import literal_eval
from Step1 import Step1


# input
gl = literal_eval(input("Please enter the data: "))
radius = input("Enter the radius: ")
q0 = input("Enter the genomes quorum: ")

# create step 1 object
step1 = Step1(q0, gl, radius)

print(step1.get_cogs_frequency())

# initialize DICTIONARY









# create COGs classification dictionary

# generate the cogClassification dictionary to a file.



