from ast import literal_eval
from Step1 import Step1

#[("kinase",3),("tf",2)], [("a",3),("kinase",2)]
# input
gl = literal_eval(input("Please enter the data: "))
q0 = input("Enter the genomes quorum: ")
radius = input("Enter the radius: ")

# create step 1 object
step1 = Step1(gl,q0, radius)
dica = (step1.gen_dictionary(gl)[0])
for keys,values in dica.items():
    print(keys)
    print(values)
print(step1.get_cogs_frequency())

# initialize DICTIONARY









# create COGs classification dictionary

# generate the cogClassification dictionary to a file.



