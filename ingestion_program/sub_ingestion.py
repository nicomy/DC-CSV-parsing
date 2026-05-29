import argparse
import os
import json
import importlib
import subprocess
import sys
from timeit import default_timer as timer



# Parsing command-line arguments
parser = argparse.ArgumentParser(description='Process some paths.')
parser.add_argument('input', type=str, help='input data directory')
parser.add_argument('output_results', type=str, help='output file')
parser.add_argument('submission_program', type=str, help='directory of the code submitted by the participants')
parser.add_argument('output_profiling', type=str, help='output_profiling')


args = parser.parse_args()

# Assigning the arguments to variables
input_dir = args.input.strip()
print(f"input data directory: {input_dir}")

output_results = args.output_results.strip()
print(f"output file: {output_results}")

submission_program = args.submission_program.strip()
print(f"directory of the code submitted by the participants: {submission_program}")

output_profiling = args.output_profiling.strip()
print(f"output_profiling file: {output_profiling}")




# Install and import each package
def install_and_import_packages(required_packages):
  for package in required_packages:
      try:
          globals()[package] = importlib.import_module(package)
      except ImportError:
          print('impossible to import, installing packages',package)
          package_to_install = 'scikit-learn' if package == 'sklearn' else package
          subprocess.check_call([sys.executable, "-m", "pip", "install", package_to_install])
          globals()[package] = importlib.import_module(package)

        

def write_in_json(dic_res,file):
    json_pers = json.dumps(dic_res, indent=2, sort_keys=True,  ensure_ascii=False)
    with open(file,"w") as f :
        f.write(json_pers)



def generate_prop_dic(prefix_file="file_easy", prediction_name="output_easy.json" ):
    nb_file_ignored = 0 
    dir_name = input_dir
    datasets_list = [filename for filename in os.listdir(dir_name) if filename.startswith(prefix_file)]
    pred_dic = {}
    total_time = 0
    for dataset_name in datasets_list :

        file= os.path.join(dir_name,dataset_name)
        
        with open(file,'r') as f : 
            list_csv_data = f.readlines()
        

        print(f"\nParsing dataset: {dataset_name}")


        try:
            start = timer()
            pred_prop = program(list_csv_data )
            end = timer()
            pred_dic = pred_dic | pred_prop
            total_time += end-start
        except Exception as exc:
            print(f"WARNING : this file {dataset_name} is ignored because of the error : {exc}\n" )
            import traceback 
            print (traceback.format_exc())
            pred_prop= {}
            nb_file_ignored +=1

    write_in_json(  pred_dic, os.sep.join([output_results,prediction_name]))

    return total_time, nb_file_ignored/len(datasets_list) ; 




# Reading and executing the code submitted by the participants
program_file = os.path.join(submission_program, 'program.py')


if os.path.isfile(program_file):
    with open(program_file, 'r') as file:
        program_code = file.read()
        exec(program_code, globals())
else:
    print(f"File not found: {program_file}")


if 'program' in globals():
    pass
else:
    print("The 'program' function is not defined in the submitted code.")


time_easy,perc_files_missed_easy = generate_prop_dic(prefix_file="file_easy",
                  prediction_name="output_easy.json")

time_hard,perc_files_missed_hard = generate_prop_dic(prefix_file="file_hard",
                  prediction_name="output_hard.json")


#### wirte profinling infos


write_in_json(dic_res={"time_easy":time_easy, 
                       "perc_files_missed_easy": perc_files_missed_easy,
                       "time_hard":time_hard,
                       "perc_files_missed_hard":perc_files_missed_hard},
              file=os.sep.join([output_results,"profiling.json"])
              )


