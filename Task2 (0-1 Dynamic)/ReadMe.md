ReadMe for 01Dynamic.py

This program has two modes, testing and defualt. 
The default mode will run one iteration of the knapsack problem with 
predefined items list and can be used to show the validity of the program
as the items list is currently set to the example in the slides. 

The testing mode will run through the knapsack problem on randomly generated input
ranging from capacity of 100 and items list of 100 through capacity of 5000 and items list 
of 5000 and will time the execution of the program and will write the results to a .csv file. 

If the printing variable is set to true, then all results and some information regarding the items list
will be printed to the console during exection. 

If the debug variable is set to true, then large amounts of information regarding item generation, table generation, and
other relevent information will be printed to the console. 

To enable any of these modes, edit the global variable near the top of the program and set the either to 
'True' or 'False' to enable/disable the modes. 

Once the wanted run environment is set up, in a command line navigate to the directory and run the command
'python 01Dynamic.py' and the program will run as desired. 