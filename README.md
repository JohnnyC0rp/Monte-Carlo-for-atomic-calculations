# Monte Carlo for searching an optimal system state

This script allows you to calculate atomic models in 2 and 3 dimensional space and visualizes it using plotly.
Monte Carlo Simulation, also known as the Monte Carlo Method or a multiple probability simulation, is  a mathematical technique, which is used to estimate the possible outcomes of an uncertain event . I am using the following algorithm:

1) Initial condition: arbitrarily distribution of the atoms in a given region of space.
2) Calculate the total energy of the system (using Lennard-Jones potential for two atoms and considering each pair)
3) Move the arbitrary atom in an arbitrary direction (select reasonable discrete steps, depending on the parameters of Lennard-Jones potential)
4) Calculate the change in the total energy of the system.
5) If the energy is reduced, then use this shift, and repeat the cycle from step (3).
6) If the energy is increased by ΔE, then calculate value A = exp (-ΔE/kT) and generate a random number in the range [0 ... 1]. If this number is greater than A, then cancel shift of atom in step (3) and redo step (3)(Monte Carlo itself). If this number is less than A, then apply this shift and repeat the cycle from step (3).

Using this algorithm is a good practice because it prevents us from finding the local minimum of system and gives an ability to find the global minimum.

## How to use

This repo contains file run.py, it is used to run program from console, but you can write your own frontend interface.

### Using run.py

```
$ python3 run.py
Enter num iterations:
(in second case it will considered as num of useless iterations)
20000
Enter KT:
0.0001
Enter num of frames in animation:
(This will considered for all animations including rdf animation)
15
Enter file from which read atoms:
(skip, if u want to generate them randomly; this feature is recommended for calculating melting)
Enter num of atoms:
(they wil be generated randomly; skip to continue)
10
Enter space borders in which atoms will be generated separated by space:
(example: '-1 1')
-1 1
Enter A and B for atoms:
(for example: '0.5 0.5')
0.5 0.5
Enter num of atoms:
(they wil be generated randomly; skip to continue)

Enter affecting radius:
(this is just an optimization feature, skip for disable; attention: it may seriously affect on synthesis calculations)

Enter 2 or 3 for specifying dimensions:
2
Do u want to see all received data immediately after finishing:
(0 or 1; not recommended when running on remote server)
0
Enter calculation group:
(it will be saved in separate folder)
showcase
Enter name of this calculation so u can find it easily in future:
1
Please wait...
Atoms [[10, (-1.0, 1.0), [0.5, 0.5]]]
Iterations: 20000
[Pos]
 [-0.00264536  1.13606533]
[Pos]
 [0.97544928 1.66013262]
[Pos]
 [-1.08116242 -0.92986835]
[Pos]
 [-0.61970951  0.09475674]
[Pos]
 [-0.01076066  2.24879777]
[Pos]
 [-0.42781682 -1.87448181]
[Pos]
 [-1.09921115  1.1137749 ]
[Pos]
 [0.51837975 0.15211179]
[Pos]
 [ 0.03745409 -0.84931487]
[Pos]
 [1.46899405 0.66580568]

Total system energy:-4.304956854578128
---------------------------------------------
Done.
```

Results for above example:

ATTENTION: For atoms positions and RDF function animations are provided, so you can see how it was changed step by step

![image](https://user-images.githubusercontent.com/79414726/198291488-d395248b-4974-4b78-92bb-f63cd4a39609.png)
Start state
![image](https://user-images.githubusercontent.com/79414726/198293153-40324682-e607-4114-85d5-d456405d5b6d.png)
End state

As you can see, atoms now are forming eye-catching structure, it is not perfect, but it is because we used only 20000 iterations, for precise result use at least 100000 iterations

You can also monitor how total energy was changing with iterations.

![image](https://user-images.githubusercontent.com/79414726/198294790-49c531af-342e-4643-bff4-357018aa50a0.png)

And check out RDF function

![rdf](https://user-images.githubusercontent.com/79414726/198296189-cef97c3b-2dc8-4324-bf50-9100922cd4cb.png)

It system.py will create 'output' folder, there group folder with name you have gave and there calculation folder with name you have gave and there it will put all results

```
Working directory
└───output
    └───test
        └───test1_KT=0.0001
            ├───html
            ├───png
            └───xyz
```

## Use cases

Using my program for example you can do these things:

1. Calculate crystal structure for atoms with different parameters
2. Simulate nanoparticle melting process and see how it will slowly destroy
3. Simulate nanoparticle synthesis and see how from separate atoms whole structures will be forming

For melting you can take already calculated structures from 'Ready structures for calculating melting' folder

### For example synthesis:

![image](https://user-images.githubusercontent.com/79414726/198309477-f87d81e4-cc94-4f76-818a-f1ad20ef59e7.png)
start
![image](https://user-images.githubusercontent.com/79414726/198309491-564e9385-96f5-4388-b473-1db7fda9aa6a.png)
end
Here, atoms hasn't formed one completed crystal but 5 separate
![Untitled](https://user-images.githubusercontent.com/79414726/198312125-39e255f8-3c82-4f26-aaa4-7d181d5f19e9.png)

### Melting:

Lets try set high temperatute and see what will happen

![image](https://user-images.githubusercontent.com/79414726/198829297-0a049fc4-6a18-4189-94e6-d100339a7098.png)

At the start atoms have straight structure

![image](https://user-images.githubusercontent.com/79414726/198829376-4719ed2e-515f-43b1-968e-39a7b00f86a7.png)

Then, structure began to destroy

![image](https://user-images.githubusercontent.com/79414726/198829422-0d006569-72af-47f9-aff3-ac7d06bbd5fa.png)

And finally there is completely no structure 

Lets take a look at energy and RDF
![image](https://user-images.githubusercontent.com/79414726/198829474-8a137603-21e6-492b-b591-6b4cea45fd36.png) 
![image](https://user-images.githubusercontent.com/79414726/198829501-47c00aa5-0215-4a6b-8c6f-516d98990b4d.png)

As we can see energy was increasing with iterations, moreover we have about more than 16000 accepted steps from 30000  