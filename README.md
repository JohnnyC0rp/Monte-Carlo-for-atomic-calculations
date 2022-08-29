# Monte-Carlo-for-calculating-atom-crystal-model

This script calculates atomic crystal model in 2 and 3 dimensional space and visualizes it using plotly. 
The Monte Carlo method is as follows: 
1) initial condition: arbitrarily distribution of the atoms in a given region of space.
2) Calculate the total energy of the system
3) move the arbitrary atom in an arbitrary direction (select reasonable discrete steps, depending on the parameters of Lennard-Jones potential)
4) Calculate the change in the total energy of the system. If the energy is reduced, then use this shift, and repeat the cycle from step (3). If the energy is increased by ΔE, then calculate value A = exp (-ΔE/kT) and generate a random number in the range [0 ... 1]. If this number is greater than A, then cancel shift of atom in step (3) and redo step (3). If this number is less than A, then apply this shift and repeat the cycle from step (3).
 
![newplot](https://user-images.githubusercontent.com/79414726/187230008-96a748fd-83ad-4ecb-9916-f6599b28f7de.png)

It also allows you to build distances bar plot to estimate crystal structure, if there are a lot of same distances, it's probably a right crystal.

![newplot](https://user-images.githubusercontent.com/79414726/187230158-f1acdedf-e147-47b5-85f3-74e663d97fe4.png)



3-dimensional space:



![newplot](https://user-images.githubusercontent.com/79414726/187231047-31712a3e-2886-464e-bca5-0ec4c8475e27.png)
![newplot](https://user-images.githubusercontent.com/79414726/187231139-0efab6ac-6eb1-4c05-bb82-20a65fa61cac.png)
