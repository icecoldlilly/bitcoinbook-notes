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

    - To build a transaction input:
        1. the wallet creates one input pointing to each one of the selected UTXO by:
            - transaction hash id AND
            - output index of UTXO (first one is 0)
        2. the wallet retrieves the details including value of transaction from reference and blockchain network.
        3. the wallet unlocks the UTXO with an unlocking script
            - digital signature and public key OR some other locking script
        4. the wallet creates sequence number
    - Note:
        - All fields have to be serialized for network transmission and deserialized for display
            - transaction hash (32 bytes) 
            - output index (4 bytes)
            - unlocking script size (1-9 bytes)
            - unlock script (variable bytes)
            - sequence number (4 bytes)
        - **Transaction fees** - compensate bitcoin miners for securing the network
            - **Question:** How?
                - Makes it economically infeasible for attackers to flood the network with transactions, when small cost on every transaction is imposed.
            - **Notes:**
                - Wallets account for fee automatically, but need to include programatically.
            - **Question:** How do we calculate transaction fees?
                - Based on the size of the transaction in kilobytes, NOT (‼️) value of transaction in bitcoin
                - affect the processing priority &rightarrow; sufficient fees = likely to be included in next block.
                - ~~Not mandatory, might be processed eventually, but no priority.~~ Not relevant anymore, they get dropped if < 0.0001 BTC is paid
                - Nowadays, influenced by market forces, based on network capacity and transaction volume.
                - all info above is irrelevant, **static fees are obselete**
                - **Use Dynamic fees instead** &rightarrow; third-party fee estimation service w/ built-in fee estimation algorithm. OR. implement your own.
                    - Will calculate based on capacity and the fees offered by "competing" transactions, or static fee will get your transactions "stuck"
                    - [Popular choice](http://bitcoinfees.21.co)
                        - `curl https://bitcoinfees.21.co/api/v1/fees/recommended`
                    - Total fees = sum(inputs) - sum(outputs) &rightarrow;
                    - &rightarrow; So, don't forget to add the change; 
                        - OR else the leftover will be counted as the transaction fee
    - **Section Summary:**
        - Example:  If you have many small payments aggrigated in your wallet, that you'd like to pass on to another wallet, your transaction will be bigger than average since it will contain many UTXOs, hence your fee will be higher

## 6.4 Transaction Scripts and Script Language
- Script Language
    - Forth-like reverse-polish notation stack-based execution language
    - &rightarrow; ❓❓❓
    - Limited in scope and executable on a range of hardware (embedded devices)
        - Minimal processing
        - Can't do fancy things like modern prog. langs can do
        - Design in that matter to make sure it's secure enough
    - **Features:**
        - Turing Incompleteness
            - No loops; just conditional flow control
                - No infinite loop / "logic bomb" can be embedded in transactions
        - Stateless verification
            - No state before / after execution
                - Execute same way on any system &rightarrow; increases predictability
                    - Valid transaction is valid for FOR everyone
- Transaction scripts
    - When transaction is validated, the unlocking script in each input is executed alongside the corrseponding locking script to see if it satisfies the spending condition.
    - Express conditions for spending
    - **Construction:** (Lock + Unlock)
        - relies on two types of scripts to validate transactions
            - Locking script
                - spending condition placed on an output
                    - it specifies the conditions that must be met to spend the output in the future
                - called `scriptPubKey` &rightarrow; contains public key or bitcoin address
                - also called *"witness script"* or *"cryptographic puzzle"*
            - Unlocking script
                - "solves", or satisfies, the conditions placed on an output by a locking script and allows the output to be spent.
                    - part of every transaction input
                    - **Common scheme:**
                        - digital signature produced by the user's wallet from his or her own private key
                -  called `scriptSig` &rightarrow; contains digital signature
                -  also called `witness` (❓ How's called same name as locking script ❓)
    -  **How does it work?**
        -  validation software will copy *unlocking script*
        -  refer to a previously existing UTXO
        -  retrieve UTXO referenced by input
        -  copy the *locking script* from that UTXO
        -  execute both *unlocking & locking scripts*
        -  input validated &rightarrow; unlocking script satisfies locking script
            -  if valid &rightarrow; allow spending
    -  **Notes:**
        -  UTXO is perm. recorded in the blockchain
            -  invariable (immutable)
            -  is unaffected by failed attempts to spend it by reference in a new transaction
            -  only valid transaction (satisfies conds. of output results in the output) is considered spent
                -  meaning &rightarrow; removed from the set of the unspent transaction outputs (UTXO set)

    - **Templates:**  (types are defined by different scripts)
        - scriptSig & scriptPubKey
            - combo of scriptSig & scriptPubKey
            - graphical representation:
                - ![scriptSig + scriptPubKey](https://github.com/bitcoinbook/bitcoinbook/blob/develop/images/mbc2_0603.png)
            - **Construction:**
                - script execution stack
                    - LIFO (Last-In-First-Out) queue
                        - push (insert)
                        - pop (emit)
                    - processing each item from left ot right.
                    - **Operators** handle the parameters ( pop / push )
                        - **How do they work?**
                            - act on parameters
                            - push result onto stack
                        - **Example:** OP_ADD
                            - pop two items from stack
                            - add them together
                            - push the resulting sum onto the stack
                            - Syntax: `2 3 OP_ADD`
                        - **Conditional operators**
                            - pops needed items
                            - evaulates items
                            - push back result
                            - Syntax: `var1 var2 OP_EQUAL`
                    -  https://github.com/bitcoinbook/bitcoinbook/blob/develop/images/mbc2_0604.png 
                - TXs are valid if the top result on the stack is TRUE
                - unlocking script & locking script are executed seperately
                    - evaultes unlocking first
                    - if the result of executing the locking script with the stack data copied from unlocking script is "TRUE"
                        - Succeeded in resolving the conditions imposed by the locking script
        - Pay-to-Public-Key-Hash (P2PKH) script
            - Used to pay a user
