i=1
mkdir containers > /dev/null 2>&1
cd containers
while [ $i != 11 ]
do
    mkdir NCC-Container-$i > /dev/null 2>&1
    cd NCC-Container-$i
    sudo docker run -d -it --security-opt seccomp="../../filter.json" --name "NCC-Container-$i" -v "$PWD":/src python bash > /dev/null 2>&1
    cd ..
    i=`expr $i + 1`
done