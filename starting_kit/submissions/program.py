def program(list_rows_one_file):

  ##
  ## YOUR CODE BEGINS HERE
  ##

  # required_packages = ["sklearn","pandas",'scipy']
  # install_and_import_packages(required_packages)

  dic_results = {}
  for line in list_rows_one_file : 
    list_column  = line.split(',')
    list_column = [x.replace('"','') for x in list_column]
    id = list_column[0]
    dic_results[id] = {"first_name": list_column[1],
                       "last_name": list_column[2],
                       "adress": list_column[3].replace("\\n","\n"),
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
