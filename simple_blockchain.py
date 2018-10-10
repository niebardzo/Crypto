""" This is the simplest implementation of blockchain. The blocks are connected into chain because every next block contains 
previous block's hash. What is defining the block is hash of timestamp, data and previous block's hash."""


import hashlib
import datetime
import time

class Block:
	def __init__(self, timestamp, data, previous_block_hash):
		self.timestamp = timestamp
		self.data = data
		self.previous_block_hash = previous_block_hash
		self.hash = self.generate_hash()


	def generate_hash(self):
		sha256 = hashlib.sha256()
		sha256.update((str(self.timestamp)+str(self.data)+str(self.previous_block_hash)).encode('utf-8'))
		return sha256.hexdigest()


def create_block(last_block, data):
	timestamp = datetime.datetime.now()
	return Block(timestamp=timestamp,data=data, previous_block_hash=last_block.hash)


# Create a first Block in Blockchain
blockchain = [Block(timestamp=datetime.datetime.now(), data="First Block", previous_block_hash="0")]
while True:
	new_block = create_block(blockchain[-1], "Adding new block to blockchain")
	blockchain.append(new_block)
	print("Block created at {} with the hash {}".format(new_block.timestamp, new_block.hash))
	time.sleep(0.5)