import os
import sys

r_file = open(os.path.join(os.getcwd(), "netdata-helmchart","charts", "netdata", "values.yaml"), 'r')
w_file = open(os.path.join(os.getcwd(), "netdata-helmchart","charts", "netdata", "temp_values.yaml"), 'w')

for line in r_file:
    if 'port: 19999' in line:
        w_file.write('''  port: ''' + sys.argv[1] + '\n')
    else:
        w_file.write(line)

r_file.close()
w_file.close()

os.remove(os.path.join(os.getcwd(), "netdata-helmchart","charts", "netdata", "values.yaml"))
os.rename(os.path.join(os.getcwd(), "netdata-helmchart", "charts", "netdata", "temp_values.yaml"), os.path.join(os.getcwd(), "netdata-helmchart", "charts", "netdata", "values.yaml"))

