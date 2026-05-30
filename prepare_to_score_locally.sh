pushd data
rm -r data_csved
rm -r data_groundtruth
python generate_data.py
popd

rm -rf starting_kit/data
mkdir -p starting_kit/data
pushd starting_kit/data
# ln -s ../../data/starting_csv/*.csv .
ln -s ../../data/starting_csv/* .  
popd


rm -rf test_output

rm -rf test_output
mkdir -p test_output/res/
mkdir -p test_output/ref

pushd test_output/ref/
ln -s ../../data/data_groundtruth/* .
popd 

pushd test_output/res/ 
ln -s ../../data/data_csved/* .
popd


echo "READY"