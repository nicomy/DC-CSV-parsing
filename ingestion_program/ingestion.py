import argparse
import os
import subprocess




parser = argparse.ArgumentParser("Programme ingestion")
parser.add_argument("ingestion_program", help="Directory where the ingestion program is located ", type=str)
parser.add_argument("input", help="Input data directory ", type=str)
parser.add_argument("output", help="Output directory (where predictions are written)", type=str)
parser.add_argument("submission_program", help="Directory of the code submitted by the participants", type=str)
args = parser.parse_args()



print("Ingestion Program :")
print(list(os.walk(args.ingestion_program)))
print("")
print("Input :")
print(list(os.walk(args.input)))
print("")
print("Output :")
print(list(os.walk(args.output)))
print("")
print("Submission Program :")
print(list(os.walk(args.submission_program)))
print("")

## output files
output_profiling = args.output+os.sep + "Rprof.txt"


#Check it is a result submission or a program submission
program_py = args.submission_program+ os.sep + "program.py"
output_results  = args.output+ os.sep + "output.json"

if (os.path.isfile(program_py)) :
  print("Executing a python program")
  cmd = ["python", args.ingestion_program +os.sep+  "sub_ingestion.py", args.input , args.output, args.submission_program,output_profiling]
  print(" ".join(cmd))
  subprocess.call(cmd)
if (os.path.isfile(output_results)) :
    print("no program to execute ! Go straight to scoring")   
else :
    raise("no program or prediction to execute !") 



print("Output :")
print(os.listdir( args.output))
print("")
