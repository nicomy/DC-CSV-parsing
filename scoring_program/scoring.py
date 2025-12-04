
import argparse
import os
import subprocess
import json


##############################################
### SESSION
## input data directory :


parser = argparse.ArgumentParser("Programme ingestion")
parser.add_argument("program", help="Directory where the ingestion program is located ", type=str)
parser.add_argument("input", help="Input data directory ", type=str)
parser.add_argument("output", help="Output directory (where predictions are written)", type=str)
args = parser.parse_args()





# input = "test_output"
# output = "test_output"
# program ="test_output"

print("Input :")
print(os.listdir(args.input))
print("")
print("Output :")
print(os.listdir(args.output))
print("")
print("Program :")
print(os.listdir(args.program))
print("")

###  EVALUATION function


def percentage_of_correct_rows(dic_truth, dic_pred):
    print("evaluatig results")
    nb_total_rows = len(dic_truth)
    nb_correct_rows = 0 
    for id,dic_truth_values in dic_truth.items():
        print(dic_truth_values)
        if id not in dic_pred : 
            continue
        dic_pred_values = dic_pred[id]
        print(dic_pred_values)
        print()
        if dic_truth_values == dic_pred_values :
            nb_correct_rows +=1
    print(nb_correct_rows)
    return (nb_correct_rows/nb_total_rows)








###########################################################
# Reading files and scroring function
###########################################################




groundthruth_name = "truth.json"
truth_file = args.input + os.sep +'ref' + os.sep + groundthruth_name

with open(truth_file) as f : 
    dic_truth = json.load(f)

participant_file_name = "output.json"
prediction_file = args.input+os.sep+ "res" +os.sep+ participant_file_name

with open(prediction_file) as fp : 
    dic_prediction = json.load(fp)


# percentage 

percentage_correct_rows = percentage_of_correct_rows(dic_truth=dic_truth,dic_pred=dic_prediction)

print("percentage of correct rows : ",percentage_correct_rows)


output_file = args.output+os.sep +"scores.txt"

with open(output_file,'w') as f_output : 
    f_output.write("percentage : " + str(percentage_correct_rows))

print("Output :")
print(os.listdir(args.output))
print("")
