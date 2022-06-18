#!/bin/bash
subtasks=( "testcases" )
mkdir -p out
mkdir -p pre
mkdir -p report
cd ./tests
prefix="" ;
score=0;
dirlist=(`ls`) ;
OUTPUT_DIRECTORY="out/"
PREPROCESSED_DIRECTORY="pre/"
TEST_DIRECTORY="tests/"
REPORT_DIRECTORY="report/"
NUMBER_OF_ALL_FAILURES=0
cd ../
for folder in ${dirlist[*]}
do
	NUMBER_OF_PASSED=0
	NUMBER_OF_FAILED=0
	echo "Subtask $folder -------------------------------------"
	cd ./out
	mkdir -p $folder
	cd ../report
	mkdir -p $folder
	cd ..
	cd ./tests
	cd $folder	
	testlist=(`ls ${prefix}*.d`);
	cd ../../
	for filelist in ${testlist[*]}
	do
		filename=`echo $filelist | cut -d '.' -f1`;
		output_filename="$filename.out"
		output_asm="$filename.s"
		program_input="$filename.in"
		report_filename="$filename.report.txt"
		echo "Running Test $filename -------------------------------------"
		if command -v python3; then
			python3 main.py -i "$folder/$filelist" -o "$folder/$output_asm"
		else
			python main.py -i "$folder/$filelist" -o "$folder/$output_asm"
		fi
		if [ $? -eq 0 ]; then
			echo "MIPS Generated Successfuly!"
		spim -a -f "$OUTPUT_DIRECTORY$folder/$output_asm" < "$TEST_DIRECTORY$folder/$program_input" > "$OUTPUT_DIRECTORY$folder/$output_filename"
		if [ $? -eq 0 ]; then
			echo "Code Executed Successfuly!"
			if command -v python3; then
				python3 comp.py -a "$OUTPUT_DIRECTORY$folder/$output_filename" -b "$TEST_DIRECTORY$folder/$output_filename" -o "$REPORT_DIRECTORY$folder/$report_filename"
			else
				python comp.py -a "$OUTPUT_DIRECTORY$folder/$output_filename" -b "$TEST_DIRECTORY$folder/$output_filename" -o "$REPORT_DIRECTORY$folder/$report_filename"
			fi
			if [[ $? = 0 ]]; then
				((NUMBER_OF_PASSED++))
				echo "++++ test passed"
			else
				((NUMBER_OF_FAILED++))
				echo "---- test failed !"
			echo
			fi
			fi 
		else
			echo "Code did not execute successfuly!"
			((NUMBER_OF_FAILED++))
		fi
		
	done
	
	echo "Passed : $NUMBER_OF_PASSED"
	echo "Failed : $NUMBER_OF_FAILED"
	
done

