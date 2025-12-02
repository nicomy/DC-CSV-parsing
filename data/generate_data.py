from faker import Factory
import json 
import os
# from random import randint,sample,random
import random
import math
from datetime import datetime


nb_persons = 1000
nb_csv_file =  10



##### generate folders 

path_groundtruth="data_groundtruth/"
groundtruth_file = "truth.json"


path_csv = "data_csved/"
csv_base_name="file"


if not os.path.exists(path_groundtruth):
    os.makedirs(path_groundtruth)

if not os.path.exists(path_csv):
    os.makedirs(path_csv)




### Generate and preproc of the groundtruth
def generate_groundtruth(nb_persons):

    fake = Factory.create('fr_FR')

    dic_pers = {}
    for id in range(nb_persons) :
        # name = fake.name()
        first_name = fake.first_name()
        last_name = fake.last_name()

        adress = fake.address()
        date = fake.date()
        dic_pers[id] = {"first_name":first_name,"last_name":last_name,"adress":adress,"date":date}

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
    json_pers = json.dumps(dic_pers, indent=4,  ensure_ascii=False)

    with open(groundtruth_file,"w") as f :
        f.write(json_pers)




###################################
## Generate and shitify csv  ##
###################################

### Genereate random splits
def create_random_split(dic_pers,nb_file):
    rand_list =   [random.random() for x in range(nb_file)]
    result = [ math.floor(i * len(dic_pers) / sum(rand_list)) for i in rand_list ] 
    for i in range(len(dic_pers) - sum(result)): 
        result[random.randint(0,3)] += 1
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
def change_date_format(str_date): 
    if (str_date ==''):
        return('')
    else : 
        list_date_format= ['%d/%m/%Y','%m/%d/%Y','%Y:%m:%d:00:00']
        return(datetime.strptime(str_date, '%Y-%m-%d').strftime(random.sample(list_date_format,1)[0]))





#### format to str and csv format. 
def to_str_csv_format(dic_pers,list_id,add_quote=True,change_dates_format_chance=0.25):
    str_row = ""
    for id in list_id:
        
        # chance to change the date format
        if(random.random()<change_dates_format_chance ):
            dic_pers[id]["date"] = change_date_format(dic_pers[id]["date"])

        dic_pers[id]['adress'] = dic_pers[id]['adress'].replace('\n','\\n')

        list_row = list(dic_pers[id].values())
        if(add_quote):
            str_row += '"' + str(id) +'",'
            str_row += '"' + '","'.join(list_row) + '"'
        else :
            str_row += str(id)+',' 
            str_row += ','.join(list_row) 
        str_row += '\n'
    return(str_row)
     


def write_csv(file_name,str2write):
    with open(file_name,'w') as f:
        f.write(str2write)



####################
### main ###
##############



dic_pers = generate_groundtruth(nb_persons)
dic_pers = remove_data(dic_pers,200)
write_groundtruth_in_json(dic_pers,groundtruth_file)

list_split = random_split(dic_pers,nb_csv_file)


for i in range(0,nb_csv_file) : 
    file_name = path_csv+csv_base_name+str(i)+".csv"
    # l in list_split : 
    if(random.random()<0.1 ):
        add_quote = False
    else : 
        add_quote = True
    str_file = to_str_csv_format(dic_pers,list_split[i],add_quote)
    write_csv(file_name,str_file)

# print(json.dumps(dic_pers, indent=4,  ensure_ascii=False))

