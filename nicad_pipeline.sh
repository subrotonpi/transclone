cp -R storage/systems_converted nicad/systems
cd nicad
if [ -z "$1" ]
then
      echo "No language chosen! run: nicad_pipeline.sh java "
      exit 0
else
      echo "Chosen Language: $1"
fi

#./nicad6 functions $lang systems/project_A_java default-report
#./nicad6 functions $lang systems/project_B_p2j default-report
#cd systems
#cat project_A_java_functions.xml project_B_p2j_functions.xml > systems_converted_functions.xml
#cd ..
./nicad6 functions $1 systems/systems_converted default-report
alias chrome="open -a \"Google Chrome\""
chrome systems/systems_converted_functions-blind-clones/systems_converted_functions-blind-clones-0.30-classes-withsource.html
cd ..
