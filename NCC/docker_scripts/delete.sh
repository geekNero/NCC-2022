/bin/bash stop.sh
i=1
cd ..
sudo rm -r containers > /dev/null 2>&1
while [ $i != 11 ]
do
    sudo docker kill NCC-Container-$i > /dev/null 2>&1
    sudo docker rm NCC-Container-$i > /dev/null 2>&1
    i=`expr $i + 1`
done
