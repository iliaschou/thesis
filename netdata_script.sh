echo " Waiting for alert pod... "
inotifywait -m -r -e create,delete /var/log/containers |
  while read dir event filename; do
    if [[ $filename == *"$1"* ]]; then
      if [[ $filename == *"netdata-alert"* ]]; then
        echo "Alert pod detected! Installing monitoring service..."
        sleep 3
        rm -r netdata-helmchart
        git clone https://github.com/iliaschou/netdata-helmchart.git
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
        killall inotifywait
    fi
  fi
done

inotifywait -m -r -e create,delete /var/log/containers |
    while read dir event filename; do
       echo $filename
       if [[ $filename == *"$1"* ]]; then
          if [[ $filename == *"netdata-alert"* ]]; then
             echo "Terminating service..."
             sleep 3
             helm delete $2 -n $1
             killall inotifywait
             exit
          fi
       fi
       if [[ $filename == *"netdata"* ]]; then
          continue
          fi
       if [[ $filename == *"$1"* ]];
        then
        echo "new pod under target namespace detected, Netdata will now upgrade"
        sleep 60
        wget -O netdata.conf http://localhost:$3/netdata.conf
        sleep 2
        python3 mod_conf.py $1
        sleep 1
        helm upgrade -f netdata-helmchart/charts/netdata/values.yaml $2 netdata/netdata -n $1
        rm netdata.conf
        fi
done
