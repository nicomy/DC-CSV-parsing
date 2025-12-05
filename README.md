# GDC-CSV


We want to include 

## Getting started




install env.  

```
mamba create -n gdc_env
conda install faker
```


genereate CSVs and grountruth.json


```
cd data 
python generate_data.py
```

## Shitify datas

idea: 
- column names with several languages or even no name 
- order of column are mixed
- missing datas 
- remove comas
- change date format

To add shitify ideas, edit the file : 
"data/generate_data.py"


## Some explanations (in French ^^): 
-je génère la vérité qui ressemble  à ça  (dans le code je manipule tout en dictionnaire) : 
```
    # { "0" : 
    #     {  
    #     "first_name": "Stéphanie",
    #     "last_name": "Lebrun",
    #     "adress": "61, boulevard de Peltier\n82421 Paris",
    #     "date": "2010-08-08"
    #     }
        ...
    # }

```
 -   Je supprime aléatoirement quelques champ de données.
- Je sauvegarde la vérité sous forme de json. 


  -  Je répartis aléatoirement les données vérités en n sous fichiers/données qui sont merdifié 
      *  je change aléatoirement le format de la date pour l'instant j'ai ça comme autre format  : 
        	list_date_format= ['%d/%m/%Y','%m/%d/%Y','%Y:%m:%d:00:00']
       * Certains fichier csv ne contiennent pas de quotes entre les champ
  -  File0.csv : 
    ```
        "110","Auguste","Girard","25, avenue Pichon\n21754 Texiernec","2025-03-13"
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

Pour l'évaluation: 

    - Je lis les prédictions de json vers dictionnaire et pareil pour la verité. 
    - je me base sur l'id du dictionnaire vérité pour voir si ça existe dans le dictionnaire predit / reconstruit par le code des participants... 
    - Si ```dic_verités[id] == dic_predi[id]``` alors je compte la ligne comme juste.
    - Avec la baseline (méthode qu'on donne au participants pour simplifier le démarrage) on a un score de 16 % de ligne bien reconstruite. 


## Ack.

CREATED WITHOUT IA :> 