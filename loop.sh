search_dir=./conf/
output2='base vm'
rm finalFeature.txt
touch finalFeature.txt

for entry in "$search_dir"*
do
   echo "$entry"
   output=$((python3 verifyVMstatus.py) 2>&1)
   #echo "$output"
   if [ $output > 0 ]
    then
    	echo "============ shutdown vm $output2 ====================="
	xl destroy myvm
        output=$((python3 verifyVMstatus.py) 2>&1)
        while [ $output > 0 ] 
        do
            output=$((python3 verifyVMstatus.py) 2>&1)
        done
    fi
    output2=output
    xl create "$entry"
    sleep 10s
    output3=$((python3 verifyVMstatus.py) 2>&1)
    if [ $output3 >0 ]
    then
    source tmprun.sh  "$entry"
    #tester si les tests suites on reussi
    python3 readTestSuiteResult.py "$entry"  1
    rm /mnt/nfs_share/test.txt
    rm testSuiteResult.txt
    echo "we have create domU with flags of $entry file  and run test suite"
    else
     python3 readTestSuiteResult.py "$entry"  0
    fi
done
