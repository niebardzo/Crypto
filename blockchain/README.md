# Flask Blockchain

## What is the project?

The project is the implementation of the node in the network which works as a miner of blockchain. It is based on flask webserver.

## Features

The running node can do several things.
It is listening for transactions to be made.
It can make a consensus with other nodes in the network, which version of Blockchain is valid.
It can mine a new block and add it to the blockchain.

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
flask run --port=5000
```

The node should be running on your machine on the default port.

## Config File

The config file could be found under the name **config.json**. The following schema should be used:

```
{
    "wallet": "<Miner_wallet>",
    "peers": [{
            "ip": "<ip_of_node>",
            "port": "<port_of_node>"
        },
        {
            "ip": "<ip_of_node>",
            "port": "<port_of_node>"
        },
        {
            "ip": "<ip_of_node>",
            "port": "<port_of_node>"
        }
    ]
}
```

You could add or delete as many peers as it is needed. In a basic configuration I have added 3 nodes on localhost, then run the application in 3 terminals on different ports.

## How to communicate with the node?

The communication with the node is establish using HTTP, to make HTTP request I will use **curl**. The node contains 3 HTTP endpoints:

**1. /trans**

This endpoint is to send the transaction. It should be sent in the specific JSON schema:
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
The curl example which sends amount of **100** coins from **wallet1** to **wallet2**:

```
curl "localhost:5000/trans" -X POST -H "Content-Type: application/json" -d '{"from": "wallet1", "to": "wallet2", "amount": 100}'

```

**2. /mine**

This endpoint was created to start a process of mining a new block. To mine a new block simply makes a GET request to that endpoint:
```
curl "localhost:5000/mine" -X GET
```

**3. /get_blockchain**

This endpoint was created to exchange information about blockchain between nodes. To retrieve the whole blockchain send a GET request to this endpoint:
```
curl "localhost:5000/get_blockchain" -X GET
```


## How is the consensus made?

In the current form, the consensus algorithm is rather simple. Before adding the newly mined block to the blockchain, the node wants to get the most current version of the blockchain which is the longest valid blockchain.
The method which implements the consensus is the part of Blockchain class:

```
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

```
So if one of the nodes in the network has longer Blockchain than the Blockchain which is in the memory of our node, the node is checking the integrity of the blocks in the blockchain. If everything is fine the longest blockchain is the new valid blockchain.

## How is the proof of work made?

The proof of work is done the same as in the bitcoin algorithm. To mine the new block the node needs to calculate the hash of the whole block consists of few factors:
- Timestamp,
- Transactions data,
- Previous block hash,
- Special number.

So the work which needs to be done is to find the special number which will result in the hash with **number** of 0 in the beginning (difficulty).
The method of Block class which implements that behaviour is below:
```
def mine_block(self, difficulty):
        while self.hash[:int(difficulty)] != '0'* int(difficulty):
            self.nonce += 1
            self.hash = self.generate_hash()
```

## Tests

To run tests, **pytest** has to be installed. Then go to the project directory and type:

```
pytest
```


## Plans for the future:

- [x] Implement reading miner wallet address from the config file.
- [x] Implement reading nodes in the network from the config file.
- [x] Write unit tests.
- [ ] Implement better algorithm for consensus.
- [x] Implement difficulty growth
