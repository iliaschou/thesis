rm -r netdata-helmchart
git clone https://github.com/netdata/helmchart.git netdata-helmchart

python3 mod_port.py $3
cp netdata-helmchart/charts/netdata/values.yaml values.yaml

helm install $2 ./netdata-helmchart/charts/netdata -n $1 
sleep 120
wget -O netdata.conf http://localhost:$3/netdata.conf
sleep 2
python3 mod_conf.py $1
sleep 1
helm upgrade -f netdata-helmchart/charts/netdata/values.yaml $2 netdata/netdata -n $1
sleep 10
inotifywait -m -r -e create,delete /var/log/containers |
while read dir event filename; do
        echo $filename
	if [[ $filename == *"netdata"* ]]; then 
	   continue
           fi	   
        if [[ $filename == *"$1"* ]]; 
         then
         sleep 60
	 wget -O netdata.conf http://localhost:$3/netdata.conf
         sleep 2
         python3 mod_conf.py $1
         sleep 1
         helm upgrade -f netdata-helmchart/charts/netdata/values.yaml $2 netdata/netdata -n $1
         rm netdata.conf
        fi 
done
