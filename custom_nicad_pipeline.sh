if [ -z "$1" ];
    then
        echo "No system name provided."
    else
        # sys_name=$1 #edit this
        echo "processing system: $1"
fi

# parent_directory=$(cd .. && pwd)

sys_path=$1
sys_name=$(echo "$sys_path" | awk -F'/' '{print $NF}')

echo $sys_name
# echo $parent_directory


cp -R $sys_path NiCad/systems/$sys_name

cd NiCad
./nicad6 functions java systems/$sys_name/
cd ..
mv NiCad/systems/$sys_name'_functions.xml' storage/$sys_name'_functions_java.xml'

cd NiCad
./nicad6 functions py systems/$sys_name/
cd ..
mv NiCad/systems/$sys_name'_functions.xml' storage/$sys_name'_functions_py.xml'

rm -R NiCad/systems/$sys_name/
cd ..
