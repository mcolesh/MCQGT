# The Multi-Colored-Gean-Team problem


## The problem:
Finding sets of nearby genes with some restrictions that are preserved on at least 'n' species of bacteria. 

## A little background and motivation:
It has been found that Groups of nearby genes tend to code for proteins that have a functional interaction.
We believe that a nearby genes that are preserved among many different species indicates for:

1. Genomic evolution correlation.  
2. Functionality correlation.

__By finding all sets of nearby genes that follows a given restriction and the species they are belong to we can learn alot about species relations and biological machines / protein interactions.__

## More formally:
Given:
Set of genomes G
Radius - 𝑟, measured in number of COGs. 
Genome quorum 𝑞_0.
Set of key-words 𝑤_1…𝑤_𝑖 (represented by colors 𝑐_1…𝑐_𝑖).
Set of key-words quantities − 𝑞_1…𝑞_𝑖.
Multi Colored Quorum Gene Team (MCQGT) is  a set of genes 𝑆 that:
Contains 𝑞_𝑗 genes colored by 𝑐_𝑗 , ∀𝑗, 1≤𝑗≤𝑖 .
     (Gene is colored by 𝑐_𝑗 if its description contains the 𝑤_𝑗 word).
Appears in |𝐺’|≥ 𝑞_0   genomes, where 𝐺’∈𝐺.
Within a radius ≤𝑟.

## Solution overview:
Step 1: Counting key-words frequencies and choosing the Least-Frequent-Key-Word (LFK). 
Step 2: Finding all radiuses around all LFKs appearances using sliding windows of size r and eliminate groups that not contains 𝑤_1…𝑤_𝑖 words with count 𝑞_1…𝑞_𝑖 respectivly. 
Step 3: Finding Multi-Colored-Quorum-Gean-Teams (MCQGTs), sets from step 2 that appears at least in 𝑞_0 species: using an admissible branch and bound search over an enumeration tree. the tree nodes are genes and paths spell candidate solutions and are ordered by least least frequent to most frequent key-word.




