#!/usr/local/bin/python3

'''
File:		 fifo.py
Description: FIFO scheduling algorithm for a router
Author:		 Umesh Singla
Date:		 Oct 21, 2017
Python:		 v3.6.3
'''

from utils import initialize


def run():
	"""
	"""
	sources, packets = initialize('nw')
	order = sorted(packets, key=lambda x: x.arrivalTime)
	for p in order:
		print(p.source, end=' ')
	print()


if __name__ == '__main__':
	run()