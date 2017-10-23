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


class RR(object):
	"""
	"""

	def __init__(self):
		self.last_served_source = 0

	def max_iterations(self, sources):
		"""
		"""
		x = max(sources, key=lambda x: x.packetCount * x.packetInterval)
		return x.packetCount * x.packetInterval

	def rr(self, queue, num_of_sources):
		"""
		Since it's not Weight RR, simply 1-2-3-..n order is being followed
		for deciding the order when tie but polling is used.
		"""
		present_packets = {x.source: x for x in queue}
		polled_packets = []
		fl = 1
		l = self.last_served_source
		for i in range(l + 1, num_of_sources + 1):
			if i in present_packets.keys():
				if fl:
					self.last_served_source = i
					fl = 0
				polled_packets.append(present_packets[i])
		for i in range(1, l + 1):
			if i in present_packets.keys():
				if fl:
					self.last_served_source = i
					fl = 0
				polled_packets.append(present_packets[i])
		return polled_packets

		# If decided ever to not go with polling and use last_served_packet's
		# source, then simply sort:
		# q = sorted(queue, key=lambda x: x.source)
		# return q

	def run(self):
		"""
		"""
		sources, packets = initialize('nw')
		order = []
		max_iters = self.max_iterations(sources)
		for t in range(0, max_iters + 1):
			packetQueue = []
			for source in sources:
				if t % source.packetInterval == 0 and source.packetCount:
					packetQueue.append(Packet(source.name, t, source.packetSize))
					source.packetCount = source.packetCount - 1
			if len(packetQueue):
				packetQueue = self.rr(packetQueue, len(sources))
				order.extend(packetQueue)

		for p in order:
			print(p.source, end=' ')
		print()


if __name__ == '__main__':
	s = RR()
	s.run()