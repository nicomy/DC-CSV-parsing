pushd data
rm -r data_csved
rm -r data_groundtruth
python generate_data.py
popd


rm -rf starting_kit/data
mkdir -p starting_kit/data
pushd starting_kit/data
ln -s ../../data/starting_csv/* .
popd



# Zip folder 
zip -FS -j -r  bundle/scoring_program.zip scoring_program/
zip -FS -j -r  bundle/ingestion_program.zip ingestion_program/

zip -FS -r -j bundle/input_data.zip data/data_csved/
zip -FS -j -r  bundle/ground_truth.zip data/data_groundtruth/

cd starting_kit/ ; zip  -FS  -r  ../bundle/starting_kit.zip *  -x \*submissions\* ; cd .. ; 
zip -FS -r -j bundle.zip bundle/

python validate_bundle.py bundle.zip
