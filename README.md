# 2020_numerical_optimization_project

This repo is for numerical optimization project. The requirements are in requirements.pdf.



Please install Gurobi 9.1 solver before running,  the license can be accessed from here: https://www.gurobi.com/academia/academic-program-and-licenses/


## file description
split_data: the splited original tasks, in txt format.

metadata: preprocessing of each task, which could be used directly in downstream tasks(MIP solver), can be read via pickle module.

greedy.py: use greedy method to solve the problem, contains 2 version of greedy rules.

model.py: use MIP solver to solve the problem, contains the model description in gurobi language.

rtv.py: contains function for preprocessing each task and running one task a time.

run_task.py: main function for running task. You can change the task number and methods manually. 

MIP_*_result: pickle file containing the result of each task

## how to run tasks
- for running the test:

python run_task.py start end mode

where

start: the start index of file

end: the end index of file 

mode: 0 meas "MIP", 1 meas "MIP+greedy1", 2means "MIP+greedy2"

- ex: running task 2 to 4 in "MIP" mode:

python run_task.py 2 5 0
