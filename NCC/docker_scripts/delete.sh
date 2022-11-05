/bin/bash stop.sh
i=1
cd ..
rm -r containers > /dev/null 2>&1
while [ $i != 11 ]
do
    docker kill NCC-Container-$i > /dev/null 2>&1
    docker rm NCC-Container-$i > /dev/null 2>&1
    i=`expr $i + 1`
done
