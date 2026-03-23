# How to start

## Log in and register to this Challenge. 
First sign up or sign in Codabench.
Then register to the challenge in the submissions tab. 

## Download the starting_kit

Under the tab "files", download the archive file "starting_kit.zip"

When extracted it should contain :
* ```starting_kit/submission_script.py``` 
* ```starting_kit/data/```  

```starting_kit/data/``` is a folder containing **examples** csv files that should be treated.


## Execute the baseline and submit on Codabench. 
```submission_script.py``` is a python script that you can execute with ```python submission_script.py```.
The execution of this script should create a folder : `starting_kit/submissions/` which contains a `program.zip` and `resultS.zip` that are ready to be submited to Codabench under the tab `My Submission`.
NOTE that since csv files of the challenge are different than the one in ```starting_kit/data/``` it is **mandatory** to submit the `program.zip` into Codabench. 


## Improve ! 

Now it is time to code and make improvement to the CSV parser : 

you should edit the code between the comment : 

```{python}
def program(list_rows_one_file):
  ##
  ## YOUR CODE BEGINS HERE
  ##


  ##
  ## YOUR CODE ENDS HERE
  ##
```

The rest of the script is only there to localy test your script on the provided test datas and gather the program function into a zip archive. 
Note that only the program function `def program(list_rows_one_file)` is usefull in Codabench, however the code ingestion step in Codabench mimics the code in the starting_kit. 