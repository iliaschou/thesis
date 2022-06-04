import sys
import os

netdata_file = open("netdata.conf")
flag = False
my_cgroups = []
for line in netdata_file:
    if '[plugin:cgroups]' in line:
        flag = True
        continue
    if sys.argv[1] in line:
        temp_line = line.replace('# ', '')
        temp_line = temp_line.replace('= no', '= yes')
        my_cgroups.append(temp_line)
    if flag and '[' in line:
        break

r_file = open(os.path.join(os.getcwd(), "values.yaml"), 'r')
w_file = open(os.path.join(os.getcwd(), "temp_values.yaml"), 'w')

flags = [False, False, False]
for line in r_file:
    if line == 'child:\n':
        flags[0] = True
    if flags[0] and line == '  configs:\n':
        flags[0] = False
        flags[1] = True
    if flags[1] and line == '    stream:\n':
        flags[1] = False
        flags[2] = True
    if flags[2]:
        w_file.write('''        [global]
          hostname = {0}
        [plugins]
          cgroups = yes
          timex = no
          tc = no
          diskspace = no
          proc = no
          enable running new plugins = no
          check for new plugins every = 60
          slabinfo = no
          freeipmi = no
          go.d = no
          charts.d = no
          ioping = no
          node.d = no
          fping = no
          python.d = no
          apps = no
          perf = no
          checks = no
          idlejitter= no
        [plugin:cgroups]
          enable new cgroups detected at run time = no\n'''.format(sys.argv[1]))
        flags[2] = False
        for cgroup in my_cgroups:
            w_file.write('''        ''' + cgroup)
    w_file.write(line)

r_file.close()
w_file.close()

os.remove(os.path.join(os.getcwd(), "netdata-helmchart","charts", "netdata", "values.yaml"))
os.rename(os.path.join(os.getcwd(), "temp_values.yaml"), os.path.join(os.getcwd(), "netdata-helmchart", "charts", "netdata", "values.yaml"))
