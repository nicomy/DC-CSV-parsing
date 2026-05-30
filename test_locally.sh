


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
    test_output
