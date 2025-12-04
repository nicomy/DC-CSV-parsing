# moved insde prepare_to_score_locally
# pushd data
# rm -r data_csved
# rm -r data_groundtruth
# python generate_data.py
# popd


# rm -rf starting_kit/data
# mkdir -p starting_kit/data
# pushd starting_kit/data
# ln -s ../../data/starting_csv/file0.csv .
# ln -s ../../data/starting_csv/file1.csv .
# popd

bash prepare_to_score_locally.sh



echo "execute starting kit"
pushd starting_kit
rm -rf submissions
python submission_script.py
popd 


pushd test_output/res/ 
ln -s  ../../starting_kit/submissions/program.py .
# ln -s  ../../starting_kit/submissions/output.json .
popd


python ingestion_program/ingestion.py \
    ingestion_program \
    test_output/res \
    test_output/res \
    test_output/res

python scoring_program/scoring.py  \
    test_output \
    test_output \
    scoring_program

# Rscript ingestion_program/ingestion.R \
#     ingestion_program \
#     input_data \
#     test_output/res \
#     starting_kit/submissions

# Rscript scoring_program/scoring.R  \
#     test_output \
#     test_output \
#     scoring_program
