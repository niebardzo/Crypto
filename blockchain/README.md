# Intruduction

## What is the project?

The project is implemetation of node in the network which works as a miner of blockchain. It is based on flask webserver.

## Features

The running node is able to do several things.
It is listining for transactions to be made.
It is able to make a consesus with other nodes in the network, which version of Blockchain is valid.
It is able to mine new block and add it to the blockchain.

## Requirements

All requirements are specified in Pipfile. The best way to install is using **pipenv** being in the folder with Pipfile.

```
pipenv install --dev
pipenv shell
```

Or use standard pip3:

```
pip3 install --requirements
```

## Running the node

Export the FLASK_APP env variable and run flask.

```
export FLASK_APP=node.py
flask run
```

The node should be running on your machine on default port.

## How to communicate with the node?

The communication with the node is establish using HTTP, to make HTTP request I will use **curl**. The node contains of 3 HTTP endpoints:

**1. /trans**

This endpoint is to send the transaction. It should be send in the specific json schema:
```
trans_schema = {
	'type' : 'object',
	'properties': {
	'from': {'type': 'string'},
	'to': {'type': 'string'},
	'amount':{'type': 'number'}
	},
	'required': ['from', 'to', 'amount']
	}
```
The curl example which sends amount of **100** coins from ***wallet1** to **wallet2**:

```
curl "localhost:5000/trans" -X POST -H "Content-Type: application/json" -d '{"from": "wallet1", "to": "wallet2", "amount": 100}'

```

**2. /mine**

This endpoint was created to start a proccess of mining a new block. To mine a new block simply make a GET request to that endpoint:
```
curl "localhost:5000/mine" -X GET
```

**3. /get_blockchain**

This endpoint was created to exchange information about blockchain between nodes. To retrive the whole blockchain send a GET request to this endpoint:
```
curl "localhost:5000/get_blockchain" -X GET
```


## How is the consensus made?

In the current form the consensus algorythm is rather simple. Before adding the the new mined block to the blockchain, the node wants to get the most current version of the blockchain which is the longest valid blockchain.
The method which implements the consesus is the part of Blockchain class:

```
def reach_consensus(self):
		for url in peers:
			blocks = requests.get(url + '/get_blockchain').body
			blocks = json.loads(blocks)
			if len(blocks) > len(self.chain):
				new_blockchain = Blockchain(self.difficulty)
				for block in blocks:
					block = json.loads(block)
					new_blockchain.chain.append(Block(block.timestamp, block.data, block.previous_block_hash))
				if new_blockchain.check_chain_validity():
					self.chain = new_blockchain.chain

```
So if one of the nodes in the network has longer Blockchain than the Blockchain which is in the memory of our node, the node is checking the integrity of the blocks in the blockchain. If everything is fine the longest blockchain is the new valid blockchain.

## How is the proof of work made?

The proof of work is done the same as in the bitcoin algorythm. To mine the new block the node needs to calculate the hash of the whole block consists of few factors:
- Timestamp,
- Transactions data,
- Previous block hash,
**- Special number.**

So the work which needs to be done is to find the special number which will result in the hash with **number** of 0 in the beginning (difficulty).
The method of Block class which implements that behaviour is below:
```
def mine_block(self, difficulty):
		while self.hash[:int(difficulty)] != '0'* int(difficulty):
			self.nonce += 1
			self.hash = self.generate_hash()
```

## Plans for the future:

- [ ] Implement reading miner wallet address from the config file.
- [ ] Implement reading nodes in the network from config file.
- [ ] Write unit tests.
- [ ] Implement better algorythm for consensus.
- [ ] Implement difficulty growth
