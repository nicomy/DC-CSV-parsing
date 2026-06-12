# GDC-CSV




## Getting started


Choose between Conda or pyenv 


### Install with pyenv (need of python3.12)
```
python3 -m venv dc_csv_parsing
source dc_csv_parsing/bin/activate
pip install faker pyyaml
```

### Install env with conda

```
conda create -n gdc_env
conda activate gdc_env
conda install faker pyyaml
```





test localy 
```
bash test_locally.sh
bash test_docker_locally.sh
```


generate bundle
```
bash gen_bundle.sh
```


### genereate CSVs and grountruth.json

```
cd data 
python generate_data.py
```

## Shitify datas

idea: 
- column names with several languages or even no name 
- change delimiter
- doublon
- order of column are mixed
- missing datas 
- remove comas
- change date format (add letter)
- 

To add shitify ideas, edit the file : 
"data/generate_data.py"


## differentes scroring. 


## Some explanations (in French ^^): 
-je génère la vérité qui ressemble  à ça  (dans le code je manipule tout en dictionnaire) : 
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
 -   Je supprime aléatoirement quelques champ de données.
- Je sauvegarde la vérité sous forme de json. 


  -  Je répartis aléatoirement les données vérités en n sous fichiers/données qui sont merdifié 
      *  je change aléatoirement le format de la date pour l'instant j'ai ça comme autre format  : 
        	list_date_format= ['%d/%m/%Y','%m/%d/%Y','%Y:%m:%d:00:00']
       * Certains fichier csv ne contiennent pas de quotes entre les champs

    
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

Pour l'évaluation: 

    - Je lis les prédictions de json vers dictionnaire et pareil pour la verité. 
    - je me base sur l'id du dictionnaire vérité pour voir si ça existe dans le dictionnaire predit / reconstruit par le code des participants... 
    - Si ```dic_verités[id] == dic_predi[id]``` alors je compte la ligne comme juste.
    - Avec la baseline (méthode qu'on donne au participants pour simplifier le démarrage) on a un score de 16 % de ligne bien reconstruite. 


## Retour Gricad Coding Challenge

* bien preciser les champs importants : dates, nom, et address sont les seules qui servent pour coder. 
* Ajouter un detailed results 
* montrer un exemple de l'entrée du program. 


## Ack.

CREATED MOSTLY(only ``validate_bundle.py``) WITHOUT IA :> 

