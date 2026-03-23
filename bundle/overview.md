# Overview                 
                           
Welcome to 1st Gricad data challenge. 

You have to retrieve fictive person name, adress and date of born from different csv files and gather them into a single json formated file. 

## Goal of the Data challenge

You have to create a function that parse a CSV file.  A baseline of this function already exist **Look at the tab** `how to get started` to start smoothly ~UwU~.  
EAch csv files are passed as a list of rows in the function argument : `list_rows_one_file`.

Csv files will look like this : 

-  File0.csv : 
```
    "0","Stéphanie","Lebrun","61, boulevard de Peltier\n82421 Paris","2010-08-08"
    "90","Gabrielle","Schmitt","7, boulevard Germain\n79264 Sainte Richardnec","2006-12-07"
    "979","Olivie","Michel","14, rue Éric Goncalves\n90423 Lacombe","1972-05-26"
    "592","Sophie","Berger","7, chemin Renault\n84405 Valléeboeuf","04/04/2000"
```

-File1.csv : 
```
    865,Capucine,Briand,4, chemin de Jean\n97260 Sainte Véronique,1970-08-02
    20,Luce,Berger,14, chemin Bertrand Pages\n93207 Guichard,1980-02-17
    745,Chantal,Lefort,887, avenue Marchal\n56881 Morvan,
    315,,,,2002-02-08
```

The `program` function should return a dictionnary with the json format : 
```{json}
 { "0" : 
     {  
     "first_name": "Stéphanie",
     "last_name": "Lebrun",
     "adress": "61, boulevard de Peltier\n82421 Paris",
     "date": "2010-08-08"
     }
   ...
 }
```


**Beware :** ! CSV format is not your friend ! 
Many mistake and typo are expected inside CSV.

The main goal of this challenge is to think and fix these mistakes. 