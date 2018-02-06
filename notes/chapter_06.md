# Chapter 06 - Transactions

## 6.2 - Details

- Transactions aren't as simple as appearing on the GUI

## 6.3 - TXIO (transaction input / output) 

- **Transaction output** - indivsible chunks of bitcoin currency, recorded on the blockchain , and recognized as valid by the entire network.
    - **Transaction types:**
        1. **Unspent transaction outputs / UTXO** - all available and spendable outputs
            - Grows / Shrink as UTXOs are created / consumed.
            - Tracked by every full-node client in the UTXO set (nodes the UTXO belongs to).
            - Receving bitcoin &rightarrow; detected a UTXO that can be spent with one of the keys controlled by that wallet.
                - The wallet's "balance" is calculated by scanning the blockchain and aggregating the value of any UTXO that wallet can spend with its keys.
            - Outputs are represented *discretely*  as (integer) multiples of satoshis (eight decimal places of bitcoin 0.0000000x) which are *indivsible*
                - An unspent output can only be consumed in its entirety by a transaction
            - **Question:** What if I have UTXO of 20 bitcoins and I want to pay only 1?
                - In this case, our UTXO is larger (20 BTC) than the desired sum (1 BTC). Therefore, the transaction we conduct will generate a new UTXO that will represent the change left (19 BTC) in our wallet afterwards.
                - And vice versa, if UTXO is too small, it'll be combined with another UTXO / bigger UTXO will be found and used instead.
            - **Summary:**
            - We gather that UTXO cannot be modified other than transferring to a new owner (new key).
            - assembly of spendable UTXO is done behind the scenes by user's wallet automatically
                - **When is it relevant?** only relevant if you're programatically constructing raw transactions from UTXO)
        2. **Coinbase transaction** - the first transaction in each block
            - placed by the "winning" miner
            - creates a new bitcoin as a mining reward payable to that miner
                - doesn't consume UTXO &rightarrow; special input called "coinbase"
            - **Question:** input or output, which one came first?
                - output. funded by the coinbase transaction.
                - If block has no transactions it can still be created and coinbase will still be generated and paid to the miner of the block.
    - **Properties:**
        - An amount of bitcoin, denominated in satoshis, the smallest bitcoin unit
        - A cryptographic puzzle (locking / witness script) that determines the conditions required spend the output
    - **Formatting:**
        - **Question:** In what form transactions transmitted over the network?
            - Using serialization / deserialization to and from byte-stream
        - **Question:** What do we serialize?
            - Everything in the transaction
                - Amount (bitcoin value in satoshis)
                - Locking-Script Size (length of locking script)
                - Locking Script (script for defining spending conditions)
- **Transaction inputs** - identify which UTXO will be consumed and provide proof of ownership through an unlocking script.

    - To build a transaction:
        1. the wallet select from UTXO it controls
        2. the wallet creates one input pointing to each one of the used UTXO
        3. the wallet unlocks the UTXO with an unlocking script
    - 