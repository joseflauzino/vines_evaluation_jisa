#!/usr/bin/python
import argparse
import os

def run_ping(ip_address, rounds):
	print("Measuring latency to %s" % ip_address)
	print("Wait until the %s test rounds have been completed." % rounds)
	cmd = "ping %s -c %s > output/tmp/tmp.txt" % (ip_address, rounds)
	os.system(cmd)

def save_file(platform, vnfs, rounds):
	output_dir = "output/%sx" % (rounds)
	output_file_name = "/%s-%svnfs.txt" % (platform, vnfs)
	if os.path.isdir(output_dir) == False:
		os.mkdir(output_dir)
	file = output_dir + output_file_name
	cmd = "cat output/tmp/tmp.txt | awk -F' ' '{ print $7 }' | awk -F'=' '{ print $2}' | awk '!/^$/' > %s" % file
	os.system(cmd)

def main():
	# Initialize parser
	parser = argparse.ArgumentParser()

	# Adding optional arguments
	parser.add_argument("-p", "--platform", default="cloudstack", required = False,
					help = "Platform name (cloudstack or openstack) - case sensitive. Default: cloudstack")
	parser.add_argument("-v", "--vnfs", required = True, help = "Total number of VNFs")
	parser.add_argument("-i", "--ip-address", required = True, help = "The IP address of the network service running iperf3. ")
	parser.add_argument("-r", "--rounds", required = True, help = "The number of test rounds.")

	# Read arguments from command line
	args = parser.parse_args()

	# Initialize variables
	platform = "cloudstack"
	rounds = None
	ip_address = None
	vnfs = None

	# Get arguments
	if args.platform:
		platform = args.platform
	if args.vnfs:
		vnfs = args.vnfs
	if args.ip_address:
		ip_address = args.ip_address
	if args.rounds:
		rounds = args.rounds

	run_ping(ip_address, rounds)
	save_file(platform, vnfs, rounds)

if __name__ == "__main__":
	main()