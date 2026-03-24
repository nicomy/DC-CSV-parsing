##################################################################################################
### PLEASE only edit the program function between YOUR CODE BEGINS/ENDS HERE                   ###
##################################################################################################


########################################################
### Package dependencies /!\ DO NOT CHANGE THIS PART ###
########################################################
import subprocess
import sys
import importlib
import json
import os 

def program(list_rows_one_file):

  ##
  ## YOUR CODE BEGINS HERE
  ##

  # required_packages = ["sklearn","pandas",'scipy',.. add you package ]
  # install_and_import_packages(required_packages)

  dic_results = {}
  for line in list_rows_one_file : 
    list_column  = line.split(',')
    list_column = [x.replace('"','') for x in list_column]
    id = list_column[0]
    dic_results[id] = {"first_name": list_column[1],
                       "last_name": list_column[2],
                       "address": list_column[3].replace("\\n","\n"),
                       "date": list_column[4].removesuffix("\n")}


    # exemple  of dictionnary output 
    # { "0" : 
    #     {  
    #     "first_name": "Stéphanie",
    #     "last_name": "Lebrun",
    #     "adress": "61, boulevard de Peltier\n82421 Paris",
    #     "date": "2010-08-08"
    #     }
    # }
  return dic_results
  ##
  ## YOUR CODE ENDS HERE
  ##



##############################################################
### Generate a json /!\ DO NOT CHANGE THIS PART ###
##############################################################




# Install and import each package
def install_and_import_packages(required_packages):
    def try_pip_install(package_name):
      """Try pip install; detect externally-managed-environment error."""
      try:
          subprocess.check_call(
              [sys.executable, "-m", "pip", "install", package_name]
          )
          return True
      except subprocess.CalledProcessError as e:
          if "externally-managed-environment" in str(e):
              return False  # pip blocked by PEP 668
          raise  # real error unrelated to PEP 668
  

    def try_conda_install(package_name):
        """Attempt conda install."""
        try:
            subprocess.check_call(["conda", "install", "-y", package_name])
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    for package in required_packages:
        try:
            globals()[package] = importlib.import_module(package)
        except ImportError:
            print('impossible to import, installing packages',package)
            package_to_install = 'scikit-learn' if package == 'sklearn' else package
            pip_ok = try_pip_install(package_to_install)

            if pip_ok:
              globals()[package] = importlib.import_module(package)
              continue

            # Pip failed due to externally-managed environment (Debian, Conda etc.)
            print("pip installation blocked by externally-managed environment.")
            print(f"Trying conda install: {package_to_install}")

            conda_ok = try_conda_install(package_to_install)

            if conda_ok:
                globals()[package] = importlib.import_module(package)
                continue
            print(f"Unable to install package {package_to_install} automatically.")


# List of required packages
required_packages = [
  "pandas",
  "zipfile",
  "inspect",
]
install_and_import_packages(required_packages)


dir_name = "data"+os.sep

datasets_list = [filename for filename in os.listdir(dir_name) if filename.startswith("file")]


pred_dic = {}
for dataset_name in datasets_list :

    file= os.path.join(dir_name,dataset_name)
    
    with open(file,'r') as f : 
        list_csv_data = f.readlines()
    


    print(f"generating prediction for dataset: {dataset_name}")

    cleaned_name=dataset_name.replace("file", "").removesuffix(".csv")

    # pred_prop = program(list_csv_data )
    try:
        pred_prop = program(list_csv_data )
    except Exception as exc:

        print(f"WARNING : this file {dataset_name} is ignored because of the error : {exc}" )
        import traceback 
        print (traceback.format_exc())

        print("However the zip is still being produced.")
        # print(exc) 
        pred_prop = {}
    # validate_pred(pred_prop, nb_samples=mix_rna.shape[1], nb_cells=ref_bulkRNA.shape[1], col_names=ref_bulkRNA.columns)
    pred_dic = pred_dic | pred_prop

############################### 
### Code submission mode

# we generate a zip file with the 'program' source code

if not os.path.exists("submissions"):
    os.makedirs("submissions")

# we save the source code as a Python file named 'program.py':
with open(os.path.join("submissions", "program.py"), 'w') as f:
    f.write(inspect.getsource(program))

date_suffix = pandas.Timestamp.now().strftime("%Y_%m_%d_%H_%M_%S")




# we create the associated zip file:
zip_program = os.path.join("submissions", f"program_{date_suffix}.zip")
with zipfile.ZipFile(zip_program, 'w') as zipf:
    zipf.write(os.path.join("submissions", "program.py"), arcname="program.py")


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))
if os.path.exists("attachement"):
    with zipfile.ZipFile(zip_program, 'a', zipfile.ZIP_DEFLATED) as zipf:
        zipdir('attachement/', zipf)


print(zip_program)




# Generate a zip file with the prediction
if not os.path.exists("submissions"):
    os.makedirs("submissions")

prediction_name = "output.json"


def write_in_json(dic_res,file):
    json_pers = json.dumps(dic_res, indent=2, sort_keys=True,  ensure_ascii=False)
    with open(file,"w") as f :
        f.write(json_pers)


# convert keys to int to sort them
pred_dic= {int(k):v for k,v in pred_dic.items()}
write_in_json(  pred_dic, os.path.join("submissions", prediction_name))

# (,predi_dic)



# Create the associated zip file:
zip_results = os.path.join("submissions", f"results_{date_suffix}.zip")
with zipfile.ZipFile(zip_results, 'w') as zipf:
    zipf.write(os.path.join("submissions", prediction_name), arcname=prediction_name)

print(zip_results) 

