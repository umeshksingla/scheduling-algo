#!/usr/local/bin/python3

'''
File:		 utils.py
Description: Implementation of a packet etc used in scheduling algorithms
Author:		 Umesh Singla
Date:		 Oct 21, 2017
Python:		 v3.6.3
'''


class Packet(object):
	"""
	A Packet
	"""
	def __init__(self, source, arrivalTime, size):
		self.source = source
		self.arrivalTime = arrivalTime
		self.payload = 'someinfo'
		self.size = size


class Source(object):
	"""
	A Packet Source
	"""
	def __init__(self, name, pc, t, size, w):
		self.name = name
		self.weight = w

		self.packetCount = pc
		self.packetInterval = t 
		self.packetSize = size


class System(object):
	"""
	"""
	def __init__(self):
		pass


def getSources():
	"""
	Returns a list of Sources transmitting packets
	"""
	sources = []
	with open('input', 'r') as input:
		for l in input:
			l = l.split()
			source = Source(l[0], int(l[1]), int(l[2]), int(l[3]), 1)
			sources.append(source)
	return sources


def getPackets(sources):
	"""
	Returns a list of Packets (not in order of arrival times)
	"""
	Packets = []
	for source in sources:
		t = 0
		for i in range(0, source.packetCount):
			p = Packet(source.name, t, source.packetSize)
			Packets.append(p)
			t = t + source.packetInterval
	return Packets


def initialize():
	"""
	Returns all the sources and packets available to the algo
	"""
	sources = getSources()
	packets = getPackets(sources)
	return sources, packets