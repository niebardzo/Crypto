from flask import Flask
from flask import request
from flask_expects_json import expects_json
import hashlib
import datetime
import time
import requests
import json


class Block:
	"""The class which implements the block in the blockchain behaviour. The block consists of timestamp, data, prvious block hash, special number,
	 and hash of the block itself."""
	def __init__(self, timestamp, data, previous_block_hash, nonce = None):
		self.timestamp = timestamp
		self.data = data
		self.previous_block_hash = previous_block_hash
		if nonce is None:
			self.nonce = 0
		else:
			self.nonce = nonce
		self.hash = self.generate_hash()
		


	def generate_hash(self):
		sha256 = hashlib.sha256()
		sha256.update((str(self.timestamp)+str(self.data)+str(self.previous_block_hash)+str(self.nonce)).encode('utf-8'))
		return sha256.hexdigest()


	def mine_block(self, difficulty):
		"""Find a special number which will generate the hash of the whole block if appropiate number of 0 at the beggining, based on difficulty."""
		while self.hash[:int(difficulty)] != '0'* int(difficulty):
			self.nonce += 1
			self.hash = self.generate_hash()


class Blockchain:
	"""Blockchain class with inital difficulty value of 2."""
	def __init__(self, difficulty = None):
		self.chain = []
		if difficulty is None:
			self.difficulty = 2
		else:
			self.difficulty = difficulty


	def create_first_block(self):
		"""Method to create first genesis block and append it to the blockchain."""
		first_block = Block(datetime.datetime.now(), "First Block", "0")
		first_block.mine_block(self.difficulty)
		self.chain.append(first_block)


	def get_last_block_hash(self):
		"""Method to retrive latest block in the blockchain."""
		last_block = self.chain[-1]
		return last_block.hash


	def add_block(self, data):
		"""Method to add new block to the blockchain and grow the difficulty in every 10 mined blocks."""
		new_block = Block(datetime.datetime.now(), data, self.get_last_block_hash())
		new_block.mine_block(self.difficulty)
		self.chain.append(new_block)
		if len(self.chain)%10 == 0:
			self.difficulty = self.difficulty + 1


	def check_chain_validity(self):
		"""Checks the validity of every block in the blockchain"""
		for i in range(1 ,len(self.chain)):
			current_block = self.chain[i]
			previous_block = self.chain[i-1]

			if current_block.hash != current_block.generate_hash():
				return False
			if current_block.previous_block_hash != previous_block.hash:
				return False
		return True


	def reach_consensus(self):
		"""Connects to all the peers in networks and finds the longest valid blockchain."""
		for peer in peers:
			url = "http://"+ str(peer["ip"]) + ":" + str(peer["port"])
			try:
				blocks = requests.get(url + '/get_blockchain').json()
			except requests.RequestException:
				continue
			if len(blocks) > len(self.chain):
				new_blockchain = Blockchain(self.difficulty)
				for block in blocks:
					new_blockchain.chain.append(Block(block["timestamp"], block["data"], block["previous_block_hash"], block["nonce"]))
				if new_blockchain.check_chain_validity():
					self.chain = new_blockchain.chain



node = Flask(__name__)

with open("config.json", "r") as config:
	try:
		config_file = json.loads(config.read())
	except json.decoder.JSONDecodeError:
		print("Wrong config file.")
		exit()

nodes_transactions = []

#From Configuration file
miner_wallet = config_file["wallet"]

#From configuration file.
peers = config_file["peers"]


trans_schema = {
	'type' : 'object',
	'properties': {
	'from': {'type': 'string'},
	'to': {'type': 'string'},
	'amount':{'type': 'number'}
	},
	'required': ['from', 'to', 'amount']
	}

coin = Blockchain()
coin.create_first_block()
coin.reach_consensus()


@node.route('/trans', methods=['POST'])
@expects_json(trans_schema)
def transaction():
	if request.method == 'POST':
		new_transaction = request.get_json()
		nodes_transactions.append(new_transaction)
		return 'You have successfully submitted the transaction.'



@node.route('/mine', methods=['GET'])
def mine():
	nodes_transactions.append({
		'from': 'rewards', 'to': miner_wallet, 'amount': 1
		})

	data = {'transactions': list(nodes_transactions)}
	coin.reach_consensus()
	coin.add_block(data)
	nodes_transactions.clear()
	return json.dumps({'timestamp': str(coin.chain[-1].timestamp),
		'data': str(coin.chain[-1].data),
		'hash': str(coin.chain[-1].hash)
		})


@node.route('/get_blockchain', methods=['GET'])
def get_blockchain():
	blockchain_to_send = []
	for block in coin.chain:
		block_to_send = {
			'timestamp': str(block.timestamp),
			'data': str(block.data),
			'previous_block_hash': str(block.previous_block_hash),
			'nonce': str(block.nonce)
		}
		blockchain_to_send.append(block_to_send)
	return json.dumps(blockchain_to_send)

