from faker import Factory
import json 
import os
# from random import randint,sample,random
import random
import math
from datetime import datetime





##### generate folders and parameters 

path_groundtruth="data_groundtruth/"
groundtruth_file_easy = path_groundtruth+"truth_easy.json"
groundtruth_file_hard = path_groundtruth+"truth_hard.json"

eval_nb_csv_file_easy =  20
# eval_nb_persons_easy = 10000
eval_nb_persons_easy = eval_nb_csv_file_easy * 250


eval_nb_csv_file_hard = 50
# eval_nb_persons_hard = 50000
eval_nb_persons_hard = eval_nb_csv_file_easy * 250





path_csv = "data_csved/"
csv_base_name_easy = "file_easy"
csv_base_name_hard ="file_hard"


starting_nb_persons = 20
starting_nb_csv_file =2

csv_base_name_starting="file_exemple"
path_csv_starting_kit = "starting_csv/"
groundtruth_file_starting = path_csv_starting_kit+ os.sep + "starting_truth.json"

# path_starting_kit="../starting_kit/"
# starting_kit_data


if not os.path.exists(path_groundtruth):
    os.makedirs(path_groundtruth)

if not os.path.exists(path_csv):
    os.makedirs(path_csv)

if not os.path.exists(path_csv_starting_kit):
    os.makedirs(path_csv_starting_kit)



########## Shitify parameters

original_date_format='%d/%m/%Y'
list_date_format_easy= [original_date_format,'%d-%m-%Y','%Y-%m-%d','%m/%d/%Y','%Y:%m:%d:00:00', "%c" , '%d,%m,%Y']
list_date_format_hard = list_date_format_easy + ["%A %d %B %Y", "%d%m%Y",'%m/%d/%y' "Week:%V-%d/%m/%Y-time:%H%S" ]


list_seperator_easy = ['\t' , ',' , ';' , '|']
list_seperator_hard = list_seperator_easy + [random.randint(1,10)*" ", random.randint(2,5)*"\t"]



list_delim_easy =["",'"']
list_delim_hard =list_delim_easy +['`', '“',]



###################################
## Generate Groundtruth  ##
###################################


### Generate and preproc of the groundtruth
def generate_groundtruth(nb_persons):

    fake = Factory.create('fr_FR')

    dic_pers = {}
    for id in range(nb_persons) :
        # name = fake.name()
        first_name = fake.first_name()
        last_name = fake.last_name()

        address = fake.address()
        date = fake.date(pattern = original_date_format)
        dic_pers[id] = {"first_name":first_name,"last_name":last_name,"address":address,"date":date}

    return(dic_pers)

def remove_data(dic_pers,nb_missing_datas=200):
    nb_person= len(dic_pers)
    
    for i in range(nb_missing_datas):
        id = random.randint(0,nb_person-1)
        nb_values = len(dic_pers[id])
        key_2_wipe = list(dic_pers[id].keys())[random.randint(0,nb_values-1)]
        dic_pers[id][key_2_wipe]=""
    
    return dic_pers

def write_groundtruth_in_json(dic_pers,groundtruth_file):
    json_pers = json.dumps(dic_pers, indent=2, sort_keys=True,  ensure_ascii=False)

    with open(groundtruth_file,"w") as f :
        f.write(json_pers)

Headers = ["id","first_name","last_name","address", "date" ]

###################################
## Generate and shitify csv  ##
###################################

### Genereate random splits
def create_random_split(dic_pers,nb_file):
    rand_list =   [random.random() for x in range(nb_file)]

    result = [ math.floor(i * len(dic_pers) / sum(rand_list)) for i in rand_list ] 
    for i in range(len(dic_pers) - sum(result)): 
        result[random.randint(0,nb_file-1)] += 1
    return(result)

def random_split(dic_pers,nb_file):
    list_split_size = create_random_split(dic_pers,nb_file)
    l_keys = list(dic_pers.keys())
    #list of list of ids
    list_id_per_file =  []
    for size in list_split_size:
        selected_keys = random.sample(l_keys, size)
        list_id_per_file.append(selected_keys)
        for id_to_remove in selected_keys : 
            l_keys.remove(id_to_remove)
    return(list_id_per_file)



### Shitify functions : 
def change_date_format(str_date_origin,str_format_output,original_date_format=original_date_format): 
    if (str_date_origin ==''):
        return('')
    else : 
        return(datetime.strptime(str_date_origin,original_date_format ).strftime(str_format_output))



# def remove_end_line(str_csv):
#     if random.radnom() < 0.3  # remove all \n character
#         res_csv= str_csv.replace("\n", ' ')
#     else :
#         res_csv = ""
#         for line in str_csv.split('\n'):
#             if random.radnom() < 0.4 : 
#                 res_csv += line.replace("\n", ' ')
#             else : 
#                 res_csv += line
#     return res_csv


# def encode(str_csv):
#     var = 
#     # binaire, base64, UTF-8, UTF-16, Latin-1, ASCII, UNICODE
#     str_csv.encode(random.sample(var,1)[0])
#     return str_csv


## parameter to 
def shitify_row(list_row,shitify_params):
    if (shitify_params.Shuffle_cells_params["activate"] and random.random()  < shitify_params.Shuffle_cells_params["probability"]):
        random.shuffle(list_row)
    
    # if (shitify_params.add_columns['activate'] and random.random()  < shitify_params.add_columns["probability"] ):


    return list_row




#### format to str and csv format. 
def to_str_csv_format(dic_pers,list_id,delimiter='"', 
                      str_date_format=original_date_format,
                      separator=",",
                      shitify_params =None):
    str_row = ""

    for id in list_id:

        
        dic_pers[id]["date"] = change_date_format(dic_pers[id]["date"],str_date_format)
        dic_pers[id]['address'] = dic_pers[id]['address'].replace('\n','\\n')

        list_row = list(dic_pers[id].values())


        str_row += delimiter + str(id) +delimiter + separator
        # str_row += '"' + '","'.join(list_row) + '"'
        str_row += delimiter + (delimiter+separator+delimiter).join(list_row) + delimiter

        if(not(shitify_params and shitify_params.dic_delete_end_char["activate"] and random.radnom() < shitify_params.dic_delete_end_char["probability"])) : 
            str_row += '\n'
    return(str_row)
     


def write_csv(file_name,str2write):
    with open(file_name,'w') as f:
        f.write(str2write)


class Shitify:
    def __init__(self, l_date_format,
                  l_separator,
                    list_delim,
                    add_header=True,
                    # dic_shitify_function=None,
                    Shuffle_cells_params = {"activate": False,"probability" : 0.5},
                    add_columns= {"activate": False,"probability" : 0.5},
                    dic_delete_end_char= {"activate": False,"probability" : 0.4},
                    list_encode =None # ["ascii",'utf_32',"UTF-8", "ISO-8859-15","UNICODE"] 
                    ):
        self.l_date_format = l_date_format
        self.l_separator = l_separator
        self.l_delim = list_delim
        self.add_header = add_header
        self.Shuffle_cells_params = Shuffle_cells_params
        self.add_columns = add_columns
        # self.dic_shitify_function = dic_shitify_function
        self.dic_delete_end_char = dic_delete_end_char
        self.list_encode = list_encode






###############
### main ###
##############


#### generate evaluation datas easy 

def fun_generate_datas(path_csv, groundtruth_file , prefix_name_output, nb_persons,nb_csv_file, shitify_params,force_order=False):

    dic_pers = generate_groundtruth(nb_persons)
    dic_pers = remove_data(dic_pers,int(nb_persons/10))
    dic_pers= {int(k):v for k,v in dic_pers.items()}

    write_groundtruth_in_json(dic_pers,groundtruth_file)

    list_split = random_split(dic_pers,nb_csv_file)


    for i in range(0,nb_csv_file) : 
        file_name = path_csv+prefix_name_output+str(i)+".csv"


        ## Parameters for the whole file : 
        if(force_order):
            str_date_format= shitify_params.l_date_format[i]
            delimiter  = shitify_params.l_delim[i]
            separator  = shitify_params.l_separator[i]
        else : 
            str_date_format= random.sample(shitify_params.l_date_format,1)[0]
            delimiter  = random.sample(shitify_params.l_delim,1)[0]
            separator  = random.sample(shitify_params.l_separator,1)[0]

        if (shitify_params.Shuffle_cells_params["activate"] and random.random()  < shitify_params.Shuffle_cells_params["probability"]):
            nb_cells = len(dic_pers[id].values())
            # index= ...
            
        #todo add value to same 
        





        print(f"file_name : {file_name}, date_format : {str_date_format}, delimiter={delimiter},separator={separator}")

        header_str =""
        if shitify_params.add_header :
            header_str = delimiter + (delimiter+separator+delimiter).join(Headers) + delimiter +'\n'

        str_file = header_str + to_str_csv_format(dic_pers,list_split[i],
                                     delimiter=delimiter,
                                     str_date_format=str_date_format,
                                     separator=separator, 
                                     shitify_params= shitify_params)
        
        # random_shitify_function = random.choice(shitify_params.dic_shitify_function.keys(), shitify_params.dic_shitify_function.values())

        if(shitify_params.list_encode ) :
            encoding  = random.sample(shitify_params.list_encode,1)[0]
            str_file = str_file.encode(encoding=encoding)

        write_csv(file_name,str_file)

    return ; 


print(f"easy list separator={list_seperator_easy}")

#generate easy _files
Shitify_easy = Shitify(list_date_format_easy,list_seperator_easy,list_delim_easy)

fun_generate_datas(path_csv= path_csv,
                   prefix_name_output =csv_base_name_easy,
                   groundtruth_file=  groundtruth_file_easy,
                   nb_persons= eval_nb_persons_easy,
                   nb_csv_file= eval_nb_csv_file_easy, 
                    shitify_params = Shitify_easy
                    )

#generate_hard files

Shitify_hard = Shitify(list_date_format_hard,list_seperator_hard,list_delim_hard,
                       add_header=False,
                       list_encode = None )# ["UTF-8",'utf_32', "ISO-8859-15","UNICODE"] ) #"ascii"


fun_generate_datas(path_csv= path_csv,
                   prefix_name_output =csv_base_name_hard, 
                   groundtruth_file=  groundtruth_file_hard,
                   nb_persons= eval_nb_persons_hard,
                   nb_csv_file= eval_nb_csv_file_hard, 
                   shitify_params = Shitify_hard
                )




#### generate starting datas:

Shitify_starting = Shitify(list_date_format_easy,[",",";"],['"',''])


fun_generate_datas(path_csv= path_csv_starting_kit,
                   prefix_name_output =csv_base_name_starting, 
                   groundtruth_file=groundtruth_file_starting,
                   nb_persons= starting_nb_persons,
                   nb_csv_file= starting_nb_csv_file, 
                    shitify_params = Shitify_starting,
                    force_order=True
                    )


