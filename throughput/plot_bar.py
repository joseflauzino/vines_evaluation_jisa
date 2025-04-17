import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import sys

#matplotlib.rcParams.update({'font.size': 16})
#plt.rcParams['axes.axisbelow'] = True

matplotlib.rcParams.update({'font.size': 18})
matplotlib.rc('axes', labelsize=24)

# number of VNF in the chain
# labels = ['2', '3','4','5']
labels = ['2', '4','6','8','10']
n = 0
bandwith = ""
def make_plots(cloudstack,openstack,file_name):
    x = ['2', '4','6','8','10'] #np.arange(len(labels))  # the label locations
    #width = 0.25  # the width of the bars
    width = 0.4  # the width of the bars
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.99, top=1, wspace=0, hspace=0)
    ax.grid(True,linestyle='--',axis='y')
    rects1 = ax.bar(x, cloudstack['avg'], width, capsize=5, yerr=cloudstack['error'], edgecolor='black', color='white', ls='-', hatch= 'xxx')
    #rects1 = ax.bar(x - width/2, cloudstack['avg'], width, capsize=5, yerr=cloudstack['error'], edgecolor='black', color='white', ls='-', hatch= 'xxx', label='CloudStack/Vines')
    #rects2 = ax.bar(x + width/2, openstack['avg'], width, capsize=5, yerr=openstack['error'], edgecolor='black', color='white', ls='-', hatch= '//', label='OpenStack/Tacker')
    ax.set_ylabel('Throughput [Mbps]')
    ax.set_xlabel('Number of VNFs in the chain')
    ax.set_xticks(x)
    #ax.set_xticklabels(labels)
    #ax.legend(loc='upper right')
    fig.tight_layout()
    plt.savefig(file_name)

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
    output_file_name = "plot/throughput-%sx-%s(bar).pdf" % (n,bandwith)
    cloudstack_data = {'avg': [],'error': []}
    openstack_data = {'avg': [], 'error': []}
    cloudstack_avg=[]
    cloudstack_conf_interval = []
    openstack_avg = []
    openstack_conf_interval = []
    for i in range(len(labels)):
        cloudstack_deploy = read_file("output/"+str(n)+"x-"+bandwith+"/cloudstack-"+str(labels[i])+"vnf")['throughput']
        cloudstack_avg.append(calc_average(cloudstack_deploy))
        cloudstack_conf_interval.append(calc_error(cloudstack_deploy, cloudstack_avg[i]))
        cloudstack_data['avg'].append(truncate(cloudstack_avg[i], 2))
        cloudstack_data['error'].append(cloudstack_conf_interval[i])
        openstack_deploy = read_file("output/"+str(n)+"x-"+bandwith+"/openstack-"+str(labels[i])+"vnf")['throughput']
        openstack_avg.append(calc_average(openstack_deploy))
        openstack_conf_interval.append(calc_error(openstack_deploy,openstack_avg[i]))
        openstack_data['avg'].append(truncate(openstack_avg[i], 2))
        openstack_data['error'].append(openstack_conf_interval[i])

    make_plots(cloudstack_data,openstack_data,output_file_name)

if __name__ == "__main__":
    msg = """
    Incorrect usage.
    The correct mode is: python plot_bar.py <n> <bandwith>

    n         number of the test rounds
    bandwith  int value + G (Gigabit) or M (Megabit). ex: 1G 
    """
    if len(sys.argv) != 3:
        sys.exit(msg)
    n = int(sys.argv[1])
    bandwith = str(sys.argv[2])
    main()