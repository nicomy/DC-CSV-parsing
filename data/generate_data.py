from faker import Factory
import json 
import os
# from random import randint,sample,random
import random
import math
from datetime import datetime



## Global var , maybe not the ideal choice ... 
fake = Factory.create('fr_FR')  
HEADERS = ["id","first_name","last_name","address", "date" ]

##### generate folders and parameters 

path_groundtruth="data_groundtruth/"
groundtruth_file_easy = path_groundtruth+"truth_easy.json"
groundtruth_file_hard = path_groundtruth+"truth_hard.json"

eval_nb_csv_file_easy =  25
# eval_nb_persons_easy = 10000
eval_nb_persons_easy = eval_nb_csv_file_easy * 250


eval_nb_csv_file_hard = 100
# eval_nb_persons_hard = 50000
eval_nb_persons_hard = eval_nb_csv_file_easy * 250





path_csv = "data_csved/"
csv_base_name_easy = "file_easy"
csv_base_name_hard ="file_hard"


starting_nb_persons = 20
starting_nb_csv_file =2

csv_base_name_starting="file_exemple"
path_csv_starting_kit = "starting_csv/"
groundtruth_file_starting = path_csv_starting_kit+ os.sep + "truth_starting.json"

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
list_date_format_hard = list_date_format_easy + ["%A %d %B %Y", "%d%m%Y",'%m/%d/%y', "Week:%V-%d/%m/%Y-time:%H%S" ]


list_seperator_easy = ['\t' , ',' , ';' , '|']
list_seperator_hard = list_seperator_easy + [random.randint(1,10)*" ", random.randint(2,5)*"\t"]



list_delim_easy =["",'"']
list_delim_hard =list_delim_easy +['`', '“',"-"]



###################################
## Generate Groundtruth  ##
###################################


### Generate and preproc of the groundtruth
def generate_groundtruth(nb_persons):

    

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



###################################
## Generate   ##
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



###################################
## Shitify Calss and function    ##
###################################


### Shitify functions : 
def change_date_format(str_date_origin,str_format_output,original_date_format=original_date_format): 
    if (str_date_origin ==''):
        return('')
    else : 
        return(datetime.strptime(str_date_origin,original_date_format ).strftime(str_format_output))



class Shitify:
    l_date_format = None
    l_separator = None
    l_delim = None
    add_header = None
    Shuffle_cells_params = None
    add_columns = None
    dic_delete_end_char = None
    
    list_encode = None # not used

    l_index_order= None  # For shufflung datas


    dic_dat_type_faker_fun_generator = {"license_plate":fake.license_plate,"catch_phrase":fake.catch_phrase, "company":fake.company  }
    index_insert_new_col = None
    new_col_fun_gen = None
    new_HEADERS = HEADERS.copy()


    # license_plate 

    def __init__(self, l_date_format,
                  l_separator,
                    list_delim,
                    add_header=True,
                    # dic_shitify_function=None,
                    Shuffle_cells_params = {"activate": False,"probability" : 0.2},
                    add_columns= {"activate": False,"probability" : 0.5},
                    dic_delete_end_char= {"activate": False,"probability" : 0.1},
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

        # self.index_order= None
        

    def set_cells_order_index(self,nb_cells):
            # nb_cells = len(dic_pers[id].values())
        if (self.Shuffle_cells_params["activate"] and random.random()  < self.Shuffle_cells_params["probability"]):
            self.l_index_order = list(range(nb_cells))
            random.shuffle(self.l_index_order)
        else:
            self.l_index_order = None

    def get_new_cells_order(self,list_row): 
        if(self.l_index_order is not None):
            print(list_row)
            print(self.l_index_order)
            print(self.new_HEADERS)
            print(self.index_insert_new_col)
            return [list_row[i] for i in self.l_index_order]
        else :
            return list_row
    
    def set_new_col_gen(self, nb_cells):
        self.new_HEADERS = HEADERS.copy()  
        self.index_insert_new_col = None
        self.new_col_fun_gen = None
        if (self.add_columns["activate"] and random.random() < self.add_columns["probability"]):
            self.index_insert_new_col = random.randint(0, nb_cells)
            col_name = random.choice(list(self.dic_dat_type_faker_fun_generator.keys()))
            self.new_col_fun_gen = self.dic_dat_type_faker_fun_generator[col_name]
            self.new_HEADERS.insert(self.index_insert_new_col, col_name)
        # else:


    def set_header(self):
        if not self.add_header:
            return ""
        return self.get_new_cells_order(self.new_HEADERS)


    # def set_header(self):
    #     if(not self.add_header):
    #         return ""
    #     else :
    #         return self.get_new_cells_order(self.new_HEADERS)

    def generate_new_list_with_added_column(self,list_row):
        if (self.index_insert_new_col is None ):
            return list_row
        else : 
            new_data =self.new_col_fun_gen()
            # print(new_data, self.index_insert_new_col)
            list_row.insert(self.index_insert_new_col,new_data)
            return list_row





def write_csv(file_name,str2write):
    with open(file_name,'w') as f:
        f.write(str2write)









###############
### main functions ###
##############

#### format to str and csv format. 
def to_str_csv_format(dic_pers,list_id,delimiter='"', 
                      str_date_format=original_date_format,
                      separator=",",
                      shitify_params =None):
    str_row = ""

    for id in list_id:

        
        dic_pers[id]["date"] = change_date_format(dic_pers[id]["date"],str_date_format)
        dic_pers[id]['address'] = dic_pers[id]['address'].replace('\n','\\n')

        list_row = [str(id)]+ list(dic_pers[id].values())
        # list_row =  list(dic_pers[id].values())


        list_row = shitify_params.generate_new_list_with_added_column(list_row) 
        list_row = shitify_params.get_new_cells_order(list_row)   

        str_row += delimiter + (delimiter+separator+delimiter).join(list_row) + delimiter

        if(not(shitify_params and shitify_params.dic_delete_end_char["activate"] and random.random() < shitify_params.dic_delete_end_char["probability"])) : 
            str_row += '\n'
    return(str_row)
     

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

        nb_cells = len(dic_pers[0].values())
        shitify_params.set_new_col_gen(nb_cells)      
        shitify_params.set_cells_order_index(len(shitify_params.new_HEADERS))
        l_headers = shitify_params.set_header() 


        print(f"file_name : {file_name}, date_format : {str_date_format}, delimiter={delimiter},separator={separator}")

        header_str =""
        if shitify_params.add_header :
            header_str = delimiter + (delimiter+separator+delimiter).join(l_headers) + delimiter +'\n'




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




    #                 Shuffle_cells_params = {"activate": False,"probability" : 0.2},
    #                 add_columns= {"activate": False,"probability" : 0.5},
    #                 dic_delete_end_char= {"activate": False,"probability" : 0.1},
    #                 list_encode =None # ["ascii",'utf_32',"UTF-8", "ISO-8859-15","UNICODE"] 
    #                 ):



#generate easy _files
Shitify_easy = Shitify(list_date_format_easy,
                       list_seperator_easy,
                       list_delim_easy,
                       Shuffle_cells_params = {"activate": True,"probability" : 0.1},
                       add_columns= {"activate": True,"probability" : 0.1},
                       )

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
                       dic_delete_end_char= {"activate": True,"probability" : 0.1},
                       Shuffle_cells_params = {"activate": True,"probability" : 0.3},
                       add_columns= {"activate": True,"probability" :   0.25},
                       list_encode = None )# ["UTF-8","ascii",'utf_32', "ISO-8859-15","UNICODE"] ) #"ascii"

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


