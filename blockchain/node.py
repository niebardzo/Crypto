from flask import Flask
from flask import request
from flask_expects_json import expects_json
import hashlib
import datetime
import time
import requests
import json


class Block:
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
		while self.hash[:int(difficulty)] != '0'* int(difficulty):
			self.nonce += 1
			self.hash = self.generate_hash()


class Blockchain:
	def __init__(self, difficulty):
		self.chain = []
		self.difficulty = difficulty


	def create_first_block(self):
		first_block = Block(datetime.datetime.now(), "First Block", "0")
		first_block.mine_block(self.difficulty)
		self.chain.append(first_block)


	def get_last_block_hash(self):
		last_block = self.chain[-1]
		return last_block.hash


	def add_block(self, data):
		new_block = Block(datetime.datetime.now(), data, self.get_last_block_hash())
		new_block.mine_block(self.difficulty)
		self.chain.append(new_block)


	def check_chain_validity(self):
		for i in range(1 ,len(self.chain)):
			current_block = self.chain[i]
			previous_block = self.chain[i-1]

			if current_block.hash != current_block.generate_hash():
				return False
			if current_block.previous_block_hash != previous_block.hash:
				return False
		return True


	def reach_consensus(self):
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

coin = Blockchain(5)
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

