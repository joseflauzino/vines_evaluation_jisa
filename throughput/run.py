#!/usr/bin/python
# coding=utf-8
import os
import json
import argparse

def clean_data():
	cmd = "cat output/tmp/tmp.txt | awk -F' ' '{ print $7 }' | awk '!/^$/' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?' > output/tmp/tmp2.txt"
	os.system(cmd)

def read_json_file(output_dir, output_file):
	if os.path.isdir(output_dir) == False:
		os.mkdir(output_dir)
	file_name = output_dir + output_file
	with open(file_name, 'w') as file:
		file.write('{"throughput":[]}')
	return json.loads(open(file_name, 'r').read())

def read_result(file_name):
	f = open(file_name, 'r')
	text = f.readlines()
	f.close()
	if len(text) > 2:
		del text[-1]
		del text[-1]
	float_list = []
	for i in text:
		float_list.append(float(i))
	return float_list

def save_file(file_name,data):
	open(file_name, 'w').write(json.dumps(data))

def main():
	# Initialize parser
	parser = argparse.ArgumentParser()

	# Adding optional arguments
	parser.add_argument("-p", "--platform", default="cloudstack", required = False,
					help = "Platform name (cloudstack or openstack) - case sensitive. Default: cloudstack")
	parser.add_argument("-v", "--vnfs", required = True, help = "Total number of VNFs")
	parser.add_argument("-i", "--ip-address", required = True, help = "The IP address of the network service running iperf3. ")
	parser.add_argument("-r", "--rounds", required = True, help = "The number of test rounds.")
	parser.add_argument("-b", "--bitrate", required = False, help = "Int value + G (Gigabit) or M (Megabit). Ex: 1G. " \
					"Default: unlimited")

	# Read arguments from command line
	args = parser.parse_args()

	# Initialize variables
	platform = "cloudstack"
	rounds = None
	bitrate = "unlimited"
	vnfs = None
	cmd = "iperf3"

	# Get arguments
	if args.platform:
		platform = args.platform
	if args.vnfs:
		vnfs = args.vnfs
	if args.ip_address:
		cmd += " -c " + args.ip_address
	if args.rounds:
		rounds = args.rounds
		cmd += " -t " + rounds
	if args.bitrate:
		bitrate = args.bitrate
		cmd += " -b " + bitrate

	cmd += " > output/tmp/tmp.txt"
	print("Command:",cmd)
	os.system(cmd)
	
	output_dir = "output/%sx-%s" % (rounds,bitrate)
	output_file = "/%s-%svnf" % (platform,vnfs)
	output_path = output_dir+output_file

	data = read_json_file(output_dir, output_file)
	clean_data()
	result = read_result("output/tmp/tmp2.txt")
	data["throughput"] = result
	save_file(output_path, data)

	print("Done.\nThe output can be found at:",output_path)

if __name__ == "__main__":
	main()