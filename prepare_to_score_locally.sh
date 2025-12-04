
rm -rf test_output
mkdir -p test_output/res/
mkdir -p test_output/ref

# cp data/data_ground_truth/*  test_output/ref/ 
pushd test_output/ref/
ln -s ../../data/data_groundtruth/* .
popd 

pushd test_output/res/ 
ln -s ../../data/data_csved/* .
popd



# cp -r starting_kit/attachement starting_kit/submissions

# cp starting_kit/submissions/prediction.rds test_output/res/ 


echo "READY"