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
  # system(command = paste("python", paste0(ingestion_program, .Platform$file.sep, "sub_ingestion.py"), input, output, submission_program,output_profiling, sep = " ") )
  subprocess.call(cmd)
else :
    print("no program to execute, go straight to scoring step") 
    print(" output_profiling file:" + output_profiling)
    # l_time = list()

    # dir_name = args.input + os.sep
    # dataset_list = list.files(dir_name,pattern="mixes*")
    # total_time = 86400 #24 h in seconds! 

    # for (dataset_name in dataset_list){

    #   cleaned_dataset_name <- sub("\\.h5$", "", unlist(strsplit(dataset_name, "_"))[2])

    #   l_time[[cleaned_dataset_name]] = total_time
    # }

    # write_hdf5(output_profiling,l_time)



print("Output :")
print(os.listdir( args.output))
print("")
