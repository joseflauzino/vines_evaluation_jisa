import sys
import os
import psutil
import time
import json

platform = ""
qtd_vnf = 0
n = 0

cpu_usage = []
mem_usage = []
swap_usage = []
x = {'data':[]}

def monitore_cpu_usage():
	cpu_usage.append(psutil.cpu_percent(interval=0.2))

def monitore_mem_usage():
	m_usage = psutil.virtual_memory()
	subtotal = (float(m_usage.used) / float(m_usage.total))
	mem_usage.append(subtotal*100)

def monitore_swap_usage():
	sw_usage = psutil.swap_memory()
	swap_usage.append(float(sw_usage.percent))

def save_file(data_type):
	output_dir = "output/%sx" % (n)
	output_file_name = "/%s-%svnfs(%s).txt" % (platform, qtd_vnf, data_type)
	if os.path.isdir(output_dir) == False:
		os.mkdir(output_dir)
	if data_type == "cpu":
		x['data'] = cpu_usage
	elif data_type == "mem":
		x['data'] = mem_usage
	else:
		x['data'] = swap_usage
	file_name = output_dir + output_file_name
	with open(file_name,"w") as file:
		file.write(json.dumps(x))

def main():
	for i in range(1,n+1):
		monitore_cpu_usage()
		monitore_mem_usage()
		monitore_swap_usage()
		time.sleep(1)
	save_file("cpu")
	save_file("mem")
	save_file("swap")
	print("Done.")

if __name__ == "__main__":
	msg = """
	Incorrect usage.
	The correct mode is: python run.py <platform> <qtd_vnf> <n>

	platform  platform name (cloudstack or openstack) - case sensitive
	qtd_vnf   max number of VNFs
	n         number of the test rounds
	"""
	if len(sys.argv) != 4:
		sys.exit(msg)

	platform = str(sys.argv[1])
	qtd_vnf = int(sys.argv[2])
	n = int(sys.argv[3])
	main()