# Chapter 03
- As Bob spends the payments received from Alice and other customers, he extends the chain of transactions.

- Bitcoin Core is the reference implementation of the bitcoin system, meaning that it is the authoritative reference on how each part of the technology should be implemented.

- Application developers are advised to build wallets using modern standards such as BIP-39 and BIP-32

- Bitcoin’s peer-to-peer network is composed of network "nodes," run mostly by volunteers and some of the businesses that build bitcoin applications.

- By running a node, you don’t have to rely on any third party to validate a transaction.

- Those running bitcoin nodes have a direct and authoritative view of the bitcoin blockchain, with a local copy of all the transactions, independently validated by their own system

- Bitcoin Core keeps a full copy of the blockchain by default, with every transaction that has ever occurred on the bitcoin network since its inception in 2009

- If you are developing bitcoin software and need to rely on a bitcoin node for programmable (API) access to the network and blockchain.

- When you first run bitcoind, it will remind you to create a configuration file with a strong password for the JSON-RPC interface.

- A transaction ID is not authoritative until a transaction has been confirmed.

- Absence of a transaction hash in the blockchain does not mean the transaction was not processed.

- because transaction hashes can be modified prior to confirmation in a block. After confirmation, the txid is immutable and authoritative.