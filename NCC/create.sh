i=1
mkdir containers
cd containers
while [ $i != 11 ]
do
    mkdir Container$i
    cd Container$i
    echo "Container$i" >> ../container.txt 
    sudo docker run -d -it -v "$PWD":/src python bash | head -c 12 >> ../container.txt
    echo " " >> ../container.txt
    cd ..
    i=`expr $i + 1`
done
