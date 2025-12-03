

cd data
rm -r data_csved
rm -r data_groundtruth
python generate_data.py
cd ..


rm -rf starting_kit/data
mkdir -p starting_kit/data
cd starting_kit/data
ln -s ../../data/starting_csv/file0.csv .
ln -s ../../data/starting_csv/file1.csv .


