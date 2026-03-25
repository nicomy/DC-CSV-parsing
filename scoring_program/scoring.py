
import argparse
import os
import subprocess
import json


##############################################
### SESSION
## input data directory :


parser = argparse.ArgumentParser("Programme ingestion")
parser.add_argument("input", help="Input data directory ", type=str)
parser.add_argument("output", help="Output directory (where predictions are written)", type=str)
parser.add_argument("program", help="Directory where the ingestion program is located ", type=str)
args = parser.parse_args()


# input = "test_output"
# output = "test_output"
# program ="test_output"

print("Input :")
print(list(os.walk(args.input)))
print("")
print("Output :")
print(list(os.walk(args.output)))
print("")
print("Program :")
print(list(os.walk(args.program)))
print("")

###  EVALUATION function


def percentage_of_correct_rows(dic_truth, dic_pred):
    # print("evaluatig results")
    nb_total_rows = len(dic_truth)
    nb_correct_rows = 0 
    for id,dic_truth_values in dic_truth.items():
        # print(dic_truth_values)
        if id not in dic_pred : 
            continue
        dic_pred_values = dic_pred[id]
        if dic_truth_values == dic_pred_values :
            nb_correct_rows +=1
    # print(nb_correct_rows)
    return (nb_correct_rows/nb_total_rows)

def percentage_correct(dic_truth, dic_pred,sub_key=None):
    nb_total_rows = len(dic_truth)
    if sub_key =="names" : 
        nb_total_rows *=2

    nb_correct_sub_keys= 0 
    for id,dic_truth_values in dic_truth.items():
        if id not in dic_pred : 
            continue
        dic_pred_values = dic_pred[id]
        
        if sub_key ==None : 
            if dic_truth_values == dic_pred_values :
                nb_correct_sub_keys +=1
        elif sub_key =="names" : 
            for name in ["last_name","first_name"] :
                if dic_truth_values[name] == dic_pred_values[name] :
                    nb_correct_sub_keys +=1
        else : 
            if dic_truth_values[sub_key] == dic_pred_values[sub_key] :
                    nb_correct_sub_keys +=1

    return (nb_correct_sub_keys/nb_total_rows)


###########################################################
# Reading files and scoring function
###########################################################


def score(dataset_lvl_name = "easy" , profiling_file = "profiling.json"):
    print(f"\n\nScoring {dataset_lvl_name} dataset")

    groundthruth_name= "truth_"+dataset_lvl_name+".json"
    truth_file = args.input + os.sep +'ref' + os.sep + groundthruth_name

    with open(truth_file) as f : 
        dic_truth = json.load(f)

    participant_file_name= "output_"+dataset_lvl_name+".json"
    prediction_file = args.input+os.sep+ "res" +os.sep+ participant_file_name

    with open(prediction_file) as fp : 
        dic_prediction = json.load(fp)

    
    
    with open(os.sep.join([args.input,'res',profiling_file])) as  profiling :
        dic_prof = json.load(profiling)
        time_name ="time_" + dataset_lvl_name
        time= dic_prof[time_name]
        
        files_missed_name = 'perc_files_missed_' + dataset_lvl_name
        percentage_files_missed =dic_prof[files_missed_name]

    # percentage 
    # percentage_correct_rows = percentage_of_correct_rows(dic_truth=dic_truth,dic_pred=dic_prediction)
    percentage_correct_rows = percentage_correct(dic_truth=dic_truth,dic_pred=dic_prediction,sub_key=None)
    print("percentage of correct rows : ",percentage_correct_rows)

    percentage_correct_names = percentage_correct(dic_truth=dic_truth,dic_pred=dic_prediction,sub_key="names")
    print("percentage of correct names : ",percentage_correct_names)

    percentage_dates = percentage_correct(dic_truth=dic_truth,dic_pred=dic_prediction,sub_key="date")
    print("percentage of correct dates : ",percentage_dates)

    percentage_address = percentage_correct(dic_truth=dic_truth,dic_pred=dic_prediction,sub_key="address")
    print("percentage of correct address : ",percentage_address)

    print(f"Time to parse all files : {time}")
    print(f"Percentage of files missed : {percentage_files_missed}")

    dic_res = {
        "percentage_rows_"+dataset_lvl_name : percentage_correct_rows      , 
        "percentage_names_"+dataset_lvl_name : percentage_correct_names       , 
        "percentage_dates_"+dataset_lvl_name : percentage_dates       , 
        "percentage_address_"+dataset_lvl_name : percentage_address       ,
        "percentage_files_missed_"+dataset_lvl_name : percentage_files_missed       ,
        "time_"+dataset_lvl_name : time       
    }
    
    return dic_res
        





dic_res_easy = score(dataset_lvl_name = "easy")
dic_res_hard = score(dataset_lvl_name = "hard")

print("Output :")
print(os.listdir(args.output))
print("")



def write_in_json(dic_res,file):
    json_pers = json.dumps(dic_res, indent=2, sort_keys=True,  ensure_ascii=False)
    with open(file,"w") as f :
        f.write(json_pers)


# output_name ="scores_"+dataset_lvl_name+".txt"
output_name ="scores.json"

output_file = args.output+os.sep + output_name

write_in_json(  dic_res_easy| dic_res_hard, output_file)


# groundthruth_name = "truth_easy.json"
# truth_file = args.input + os.sep +'ref' + os.sep + groundthruth_name

# with open(truth_file) as f : 
#     dic_truth = json.load(f)

# participant_file_name = "output_easy.json"
# prediction_file = args.input+os.sep+ "res" +os.sep+ participant_file_name

# with open(prediction_file) as fp : 
#     dic_prediction = json.load(fp)


# # percentage 
# percentage_correct_rows = percentage_of_correct_rows(dic_truth=dic_truth,dic_pred=dic_prediction)

# print("percentage of correct rows : ",percentage_correct_rows)


# output_file = args.output+os.sep +"scores_easy.txt"

# with open(output_file,'w') as f_output : 
#     f_output.write("percentage : " + str(percentage_correct_rows))

# print("Output :")
# print(os.listdir(args.output))
# print("")





