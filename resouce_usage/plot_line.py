import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import sys

matplotlib.rcParams.update({'font.size': 14})

# number of VNF in the chain
labels = ['2', '3', '4', '5']
n = 0

def make_plot(plot,cloudstack,openstack,file_name,metric):
    plot.rcParams['axes.axisbelow'] = True
    x = np.arange(len(labels))  # the label locations
    width = 0.25  # the width of the bars
    fig, ax = plot.subplots()
    ax.grid(True,linestyle='--',axis='y')
    if metric == "cpu":
        rects1 = ax.plot(x, cloudstack['avg'], c='#2980b9' ,label='CloudStack/Vines', marker='^', markersize=10.0, zorder=1)
        rects2 = ax.plot(x, openstack['avg'], c='#c0392b' ,label='OpenStack/Tacker', marker='o', markersize=10.0, zorder=0.9)
        ax.set_ylabel('CPU Usage [%]')
        ax.legend(loc='lower right')
    else:
        rects1 = ax.plot(x, cloudstack[0]['avg'], c='#2980b9' ,label='CloudStack/Vines RAM', marker='^', markersize=10.0, zorder=1)
        rects2 = ax.plot(x, cloudstack[1]['avg'], c='#2980b9' ,label='CloudStack/Vines SWAP', marker='>', markersize=10.0, zorder=0.9)
        rects3 = ax.plot(x, openstack[0]['avg'], c='#c0392b' ,label='OpenStack/Tacker RAM', marker='o', markersize=10.0, zorder=0.8)
        rects4 = ax.plot(x, openstack[1]['avg'], c='#c0392b' ,label='OpenStack/Tacker SWAP', marker='x', markersize=10.0, zorder=0.7)
        ax.set_ylabel('Memory Usage [%]')
        ax.legend(loc='upper right')
    ax.set_xlabel('VNFs in the chain')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim([0,100])
    fig.tight_layout()
    plot.savefig(file_name)

def read_file(file_name):
    return json.loads(open(file_name, 'r').read())

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))

def calc_average(values):
    average = sum(values)/len(values)
    return average

def calc_error(conjunto,average):
    std_deviation = np.std(np.array(conjunto))
    confidence_interval = scipy.stats.norm.interval(0.95, loc=average, scale=std_deviation)
    return confidence_interval[1]-average

def main():
    metric = "cpu"
    cloudstack_data_join = []
    openstack_data_join = []
    for x in range(0,3):
        cloudstack_data = {'avg': [],'error': []}
        openstack_data = {'avg': [], 'error': []}
        cloudstack_avg=[]
        cloudstack_conf_interval = []
        openstack_avg = []
        openstack_conf_interval = []
        if x == 1:
            metric = "mem"
        elif x == 2:
            metric = "swap"
        print("Making %s plot" % metric)
        for i in range(len(labels)):
            cloudstack_cpu = read_file("output/"+str(n)+"x/cloudstack-"+str(labels[i])+"vnfs("+metric+").txt")['data']
            cloudstack_avg.append(calc_average(cloudstack_cpu))
            cloudstack_conf_interval.append(calc_error(cloudstack_cpu, cloudstack_avg[i]))
            cloudstack_data['avg'].append(truncate(cloudstack_avg[i], 2))
            cloudstack_data['error'].append(cloudstack_conf_interval[i])
            openstack_cpu = read_file("output/"+str(n)+"x/openstack-"+str(labels[i])+"vnfs("+metric+").txt")['data']
            openstack_avg.append(calc_average(openstack_cpu))
            openstack_conf_interval.append(calc_error(openstack_cpu,openstack_avg[i]))
            openstack_data['avg'].append(truncate(openstack_avg[i], 2))
            openstack_data['error'].append(openstack_conf_interval[i])
        if x > 0: # it is memory
            cloudstack_data_join.append(cloudstack_data)
            openstack_data_join.append(openstack_data)
            if x == 2: # it is the last memory type (SWAP), so run plot!
                metric = "mem"
                output_file_name = "plot/%s-%sx(line).pdf" % (metric, n)
                make_plot(plt,cloudstack_data_join,openstack_data_join,output_file_name,metric)
            continue
        output_file_name = "plot/%s-%sx(line).pdf" % (metric, n)
        make_plot(plt,cloudstack_data,openstack_data,output_file_name,metric)

if __name__ == "__main__":
    msg = """
    Incorrect usage.
    The correct mode is: python plot_line.py <n>

    n           number of the test rounds
    """
    if len(sys.argv) != 2:
        sys.exit(msg)
    n = int(sys.argv[1])
    main()