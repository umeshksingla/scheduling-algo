#!/usr/local/bin/python3

'''
File:		 rr.py
Description: Round Robin scheduling algorithm for a router
Author:		 Umesh Singla
Date:		 Oct 21, 2017
Python:		 v3.6.3
'''

from utils import Packet
from utils import initialize

def max_iterations(sources):
	"""
	"""
	x = max(sources, key=lambda x: x.packetCount * x.packetInterval)
	return x.packetCount * x.packetInterval


def rr(queue):
	"""
	Since it's not Weight RR, simply 1-2-3-..n order is being followed
	for deciding the order
	"""
	q = sorted(queue, key=lambda x: x.source)
	return q


def run():
	"""
	"""
	sources, packets = initialize()
	order = []
	max_iters = max_iterations(sources)
	for t in range(0, max_iters + 1):
		packetQueue = []
		for source in sources:
			if t % source.packetInterval == 0 and source.packetCount:
				packetQueue.append(Packet(source.name, t, source.packetSize))
				source.packetCount = source.packetCount - 1
		if len(packetQueue):
			packetQueue = rr(packetQueue)
			order.extend(packetQueue)

	for p in order:
		print(p.source, end=' ')
	print()


if __name__ == '__main__':
	s = run()