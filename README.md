# The Multi-Colored-Gean-Team problem

The problem:
Finding sets of nearby genes with some restrictions in at least 'n' species of bacteria. 
More formally:
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

A little background and motivation:
It has been found that Groups of nearby genes tend to code for proteins that have a functional interaction.
We believe that a nearby genes that are preserved among many different species indicates for:
    +Genomic evolution correlation.  
    +Functionality correlation.

By finding all sets of nearby genes that follows a given restriction and the species they are belong to we can learn alot about species relations 


