i=1
cd containers
sudo docker ps > process.txt
while [ $i != 11 ]
do
    # if ! grep -w "NCC-Container-$i" process.txt
    # then 
    #     cd NCC-Container-$i
    #     sudo docker start NCC-Container-$i
    #     cd ..
    # fi
    cd NCC-Container-$i
    sudo docker start NCC-Container-$i
    cd ..
    i=`expr $i + 1`
done

sudo rm process.txt
