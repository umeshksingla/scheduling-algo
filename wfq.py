#!/usr/local/bin/python3

'''
File:		 wfq.py
Description: Weighted Fair Queuing scheduling algorithm for a router
			 (Assuming data linkrate to be 1 byte per ms)
Author:		 Umesh Singla
Date:		 Oct 22, 2017
Python:		 v3.6.3
'''

from multiprocessing import Process

from utils import Packet
from utils import initialize


class Queue(object):
	"""
	The first element of the self.items is the most recently inserted.
	"""
	def __init__(self):
		self.items = []

	def empty(self):
		return self.items == []

	def enqueue(self, item):
		self.items.insert(0, item)

	def dequeue(self):
		return self.items.pop()

	def size(self):
		return len(self.items)

	def getHead(self):
		return self.items[-1]


class WFQ(object):
	"""
	"""
	def __init__(self):
		self.n = 0 					# number of queues
		self.queues = [] 			# queues
		self.lastVirFinish = [] 	# last virtual finish instant
		self.linkrate = 1.0			# link rate
		self.sources = []
		self.order = []
		self.roundNo = 0
		self.lastServedTime = 0
		self.times = set()

	def re_initialize(self):
		self.n = len(self.sources)
		self.queues = [Queue(), Queue(), Queue()]
		self.lastVirFinish = [0] * self.n

	def total_weight(self):
		"""
		"""
		w = 0.0
		for s in self.sources:
			w += s.weight
		return w

	def total_packet_count_left(self):
		"""
		"""
		c = 0
		for s in self.sources:
			c += s.packetCount
		return c

	def all_queues_not_empty(self):
		"""
		"""
		a = [q.empty() for q in self.queues]
		if False in a:
			return True
		return False

	def send(self):
		"""
		Executed each time a packet to send must be selected, that is, when the
		link is idle and queues are not empty.
		"""
		while self.all_queues_not_empty():
			queueNum = self.selectQueue()
			if queueNum is None:
				pass
			else:
				packet = self.queues[queueNum - 1].dequeue()
				# print("Packet sent", packet.source, "with fn:", packet.virFinish)
				self.order.append(packet)

	def add(self, packet, queueNum):
		"""
		Executed each time a packet is received.
		"""
		packet = self.updateTime(packet, queueNum)
		self.queues[queueNum - 1].enqueue(packet)

	def round(self, t):
		"""
		"""
		self.lastServedTime = self.times.pop()
		self.roundNo += (t - self.lastServedTime)/self.total_weight()
		return self.roundNo

	def updateTime(self, packet, queueNum):
		"""
		"""
		# virStart is the virtual start of service
		virStart = max(self.round(packet.arrivalTime), self.lastVirFinish[queueNum - 1])
		packet.virFinish = virStart + packet.size/self.sources[packet.source - 1].weight
		self.lastVirFinish[queueNum - 1] = packet.virFinish
		self.times.add(packet.virFinish)
		return packet

	def selectQueue(self):
		"""
		Selects the queue with the minimal virtual finish time. Performs a
		linear search at present.
		"""
		it = 1
		queueNum = None
		minVirFinish = float("inf")

		while it <= self.n:
			queue = self.queues[it-1]
			if not queue.empty() and queue.getHead().virFinish < minVirFinish:
				minVirFinish = queue.getHead().virFinish
				queueNum = it
			it = it + 1
		return queueNum

	def receive(self):
		"""
		"""
		rem_packets = self.total_packet_count_left()
		t = 0
		while rem_packets:
			for source in self.sources:
				if t % source.packetInterval == 0 and source.packetCount:
					packet = Packet(source.name, t, source.packetSize)
					self.times.add(packet.arrivalTime)
					self.add(packet, source.name)
					# print("Packet received from", packet.source, "at", packet.arrivalTime)
					source.packetCount -= 1
			rem_packets = self.total_packet_count_left()
			t += 1

	def run(self):
		"""
		"""
		self.sources = initialize('w')
		self.re_initialize()


if __name__ == '__main__':
	s = WFQ()
	s.run()
	receiveProcess = Process(target = s.receive())
	receiveProcess.start()
	sendProcess = Process(target = s.send())
	sendProcess.start()

	for p in s.order:
		print(p.source, end=" ")
	print()