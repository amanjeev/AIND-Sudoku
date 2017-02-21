# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation: the process of finding a solution to a set of constraints that impose conditions that the variables must satisfy. ~ Wikipedia

So in this case, we have to find the constraints and then get the values that satisfy those constraints.

Constaints: 1 unit at a time, naked twins (2 pair), elements with length > 1 which are not the twins

Propagation: This is about finding a twin pair of numbers in a unit, from all the unitlists. Once you have the twins and you have the elements of the unit which are greater than 1 in length, you can eliminate the numbers that are in the twins but exist in other boxes as well. Continue on to the other unit in the unitlist.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Add two diagonal units to the existing list of units. Just like a row or column constraint, the constraint here becomes the diagonal element list.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.