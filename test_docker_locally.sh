
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

# Rscript ingestion_program/ingestion.R \
#     ingestion_program \
#     input_data \
#     test_output/res \
#     starting_kit/submissions

# Rscript scoring_program/scoring.R  \
#     test_output \
#     test_output \
#     scoring_program


docker_name=python

echo "Running ingestion Program, super user (sudo) is needed to run docker."
sudo docker run --rm  -v $PWD/ingestion_program:/app/program  -v $PWD/test_output/res:/app/output -v $PWD/starting_kit/submissions:/app/ingested_program  -w /app/program -v $PWD/data/data_csved:/app/input_data/ $docker_name python /app/program/ingestion.py /app/program /app/input_data /app/output /app/ingested_program #>> logs

echo "Ingestion progam done"


echo "Running Scoring Program"
sudo docker run --rm  -v $PWD/scoring_program:/app/program  -v $PWD/data/data_groundtruth:/app/data/data_groundtruth -v $PWD/data/data_csved:/app/data/data_csved -v $PWD/test_output:/app/output   -w /app/program     -v $PWD/test_output:/app/input     $docker_name  python /app/program/scoring.py /app/input /app/output /app/program #>> logs
echo "Scoring program done"


echo "Test if the output file scores.txt exist"
filename='test_output/scores.txt'
if [ -f $filename ]; then
    echo 'SUCESS! The result file exists.'
else
    echo 'FAILURE! The file does not exist.'
    exit 1
fi