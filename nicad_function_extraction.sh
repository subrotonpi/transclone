if [ -z "$1" ];
    then
        echo "No system name provided."
    else
        sys_name=$1 #edit this
        echo "processing system: $sys_name"
fi

# sys_name=$1

cp -R storage/systems/$sys_name NiCad/systems/$sys_name
cd NiCad
./nicad6 functions java systems/$sys_name/
mv systems/$sys_name'_functions.xml' ../storage/$sys_name'_functions_java.xml'

./nicad6 functions py systems/$sys_name/
mv systems/$sys_name'_functions.xml' ../storage/$sys_name'_functions_py.xml'

rm -R systems/$sys_name/
cd ..