import pytest
import datetime
from .node import Block, Blockchain


class TestBlock(object):

	def test_init(self):
		time = datetime.datetime.now()
		block = Block(time, "First Block", "0")
		assert (block.timestamp == time and block.data == "First Block" and block.previous_block_hash == "0" and block.nonce == 0)

	def test_init_2(self):
		time = datetime.datetime.now()
		block = Block(time, "First Block", "0")
		assert block.hash == block.generate_hash()

	def test_mine_block(self):
		time = datetime.datetime.now()
		block = Block(time, "First Block", "0")
		block.mine_block(3)
		assert block.hash == block.generate_hash()

	def test_mine_block_2(self):
		time = datetime.datetime.now()
		block = Block(time, "First Block", "0")
		difficulty = 5
		block.mine_block(difficulty)
		assert block.hash[:int(difficulty)] == '0'* int(difficulty)


class TestBlockchain(object):
	
	def test_check_chain_validity(self):
		pass

	def test_reach_consensus(self):
		pass

