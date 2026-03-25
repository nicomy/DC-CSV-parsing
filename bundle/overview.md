# Overview                 
                           
Welcome to 1st Gricad data challenge. 

You have to retrieve fictive person name, adress and date of born from different csv files and gather them into a single json formated file. 

## Goal of the Data challenge

You have to create a function that parse a CSV file.  A baseline of this function already exist **Look at the tab** `how to get started` to start smoothly ~UwU~.  
EAch csv files are passed as a list of rows in the function argument : `list_rows_one_file`.

Csv files will look like this : 

The 

-  File0.csv : 
```
"17","Thierry","De Sousa","29, rue de Blanchard\n65701 BuissonVille","16/11/2005"
"16","Danielle","Fernandez","41, avenue Legros\n79170 Saint Sophieboeuf","18/10/2014"
"6","Simone","Coste","24, boulevard Julien\n58641 HoarauVille","26/08/2016"
"18","Philippine","Bazin","76, chemin Olivier\n97373 Berger","23/12/2005"
"0","Margaux","Antoine","14, rue Martins\n95846 Rousset-les-Bains","26/01/1971"
"7","Pierre","Payet","67, boulevard De Sousa\n44558 Saint Valentine","03/06/1975"
"8","Diane","Leclercq","chemin de Le Goff\n02778 Blanchardboeuf","28/01/1977"
"9","Guillaume","Grenier","25, avenue de Joubert\n25387 Fernandesnec","29/10/1973"
```

-File1.csv : 
```
19;Nath;Carpentier;47, rue de Carpentier\n74108 Bernier-la-Forêt;07-03-1975
2;Alexandre;Guilbert;83, chemin de Allard\n64142 Gillet-les-Bains;10-05-1983
0;Philippe;Lemoine;30, avenue de Mercier\n47411 Paris-les-Bains;20-07-1981
3;Élise;Delannoy;724, rue Potier\n14392 Sainte Brigitte;08-09-1979
```

The `program` function should return a dictionnary with the json format : 
```{json}
{
  "0": {
    "address": "14",
    "date": " rue Martins\\n95846 Rousset-les-Bains",
    "first_name": "Margaux",
    "last_name": "Antoine"
  },
   ...
 }
```


**Beware :** ! CSV format is not your friend ! 
Many mistake and typo are expected inside CSV.

The main goal of this challenge is to think and fix these mistakes. 