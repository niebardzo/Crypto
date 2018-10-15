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
pipenv install
pipenv shell
```

## Running the node

Export the FLASK_APP env variable and run flask.

```
export FLASK_APP=node.py
flask run
```

The node should be running on your machine on default port.

## How to communicate with the node?

The communication with the node is establish using HTTP, to make HTTP request I will use curl. The node contains of 3 HTTP endpoints:
1. /trans
2. /mine
3. /get_blockchain

## How is the consensus made?

## How is the proof of work made?

## Plans for the future:

- [ ] Implement reading miner wallet address from the config file.
- [ ] Implement reading nodes in the network from configuration file.
- [ ] Implement the script which will run several nodes, clients making transaction and node which will be spoofing blockchain (false node).
