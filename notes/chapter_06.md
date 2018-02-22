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
                    -  ![Execution stack example](https://github.com/bitcoinbook/bitcoinbook/blob/develop/images/mbc2_0604.png)
                - TXs are valid if the top result on the stack is TRUE
                - unlocking script & locking script are executed seperately
                    - evaultes unlocking first
                    - if the result of executing the locking script with the stack data copied from unlocking script is "TRUE"
                        - Succeeded in resolving the conditions imposed by the locking script
        - Pay-to-Public-Key-Hash (P2PKH) script
            - Used to pay a user
            - Vast majority of payments on the network
            - Locking script that locks the output to a public key hash ( bitcoin address )
                - Output locked by a P2PKH script can be unlocked by presenting:
                    1. public key
                    2. digital signatures created by the private key
                - Format: 
                    - `<Receiver Sig> <Receiver Public Key> OP_DUP OP_HASH160 <Receiver Sig> OP_EQUALVERIFY OP_CHECKSIG`
                - ![P2PKH example pt.1.](https://github.com/bitcoinbook/bitcoinbook/blob/develop/images/mbc2_0605.png)
                - ![P2PKH example pt.2.](https://github.com/bitcoinbook/bitcoinbook/blob/develop/images/mbc2_0606.png)

## 6.5 Digital Signatures (ECDSA)
- Elliptic Curve Digital Signature Algorithm
- Used for digital signatures based on elliptic curve private / public key pairs
- Used by OP_CHECKSIG, OP_CHECKSIGVERIFY, OP_CHECKMULTISIG, OP_CHECKMULTISIGVERIFY
    - Any time you see those in a locking script
    - The unlocking script must contain an ECDSA signature
    - Neither the signature nor the input have to belong or be applied by same owner
        - In addition, each transaction input and any signature it may contain is completely independent of each other
        - Therefore, multiple parties can collaborate to construct transactions and sign only one input each
            - See "CoinJoin" &rightarrow; creates multi-party transactions for privacy
- **Purposes:**
    1. Proves that the owner of the private key, has authorized the spending of those funds.
    2. Holds the proof of authorization as undeniable
    3. The signature proves that the transaction is immutable after being signed
- **How do digital signatures work?** In two parts:
    1. An algorithm for creating a signature, using a private key (the signing key), to sign a message (the transaction)
        - **What's needed?**
            - dA is the signing private key
            - m is the transaction
            - F_hash is the hashing function
            - F_sig is the signing algorithm
            - Sig= (R, S) is the resulting signature
                - Where R and S are serialized into a byte-stream using an ISO encoding scheme called DER
        - **What's DER?**
            - Destinguished Encoding Rules used for *serlization of signatures*
            - Consists of nine elements:
                - 0x30 - start of DER
                - 0x45 - length of sequence (69 bytes)
                - 0x02 - an integer value follows
                - 0x21 - the length of the integer (33 bytes)
                - **R value in hex**
                - 0x02 - another integer follows
                - 0x20 - the length of the integer (32 bytes)
                - **S value in hex**
                - A suffix (0x01) indicating the type of hash used (SIGHASH_ALL)
            - Important parts are the R, and S values
    2. An algorithm that allows anyone to verify the signature given the message and pub. key (without priv. key)
        - **How do ECDSAs present proof of ownership, without revealing the private key?**
            - To do so we need:
                - A signature made out of serialized byte-streams of **R & S** according to **DER**
                - Serialized transaction
                - The public key cirresponding to the private key, used to to create the signature
            - Only the owner of the priv. key can provide all of these
            - Algo. returns TRUE if the signature is valid for this message and public key
        - **What is SIGHASH?**
            - Digital signatures applied to messages, which imply commitment by the signer to specific transaction data (inputs, outputs and other tx fields - can be partial or all)
                - **We can know which part of the transaction's data is included in the hash using a SIGHASH flag.**
                    - Single byte, every signature has it
                    - Types: ALL, NONE, SINGLE
                    - Use: multiple participants collaborating outside the bitcoin network and updating a partially signed transaction
                    - Can be combined with SIGHASH_ANYONECANPAY to create different payment scenarios with SIGHASH byte, using bitwise 'OR'
        - **How do we perform ECDSA Math?**
            - The signature algorithm generates temporary private public key pair
                - Used by F_sig, in calculation of R and S values
                - `k` is a random number used as following: `P = k*G` to generate temporary P
                - `P` is the temporary public key, and `G` is the elliptic curve generator constant point
                - `S = (k^(-1)) * ( Hash(m) + dA * R ) mod p`
                    - `k` is temporary private key
                    - `R` is the x coord of the temp. public key
                    - `dA` is the signing private key
                    - `m` is the transaction data
                    - `p` is the prime order of the elliptic curve
                - Verification is inverse
                    - P = (S^(-1)) * Hash(m) * G + (S^(-1)) * R * Qa
                        - where Qa is the public key of the transaction conductor (Alice for example)
            - Don't understand? That's fine me neither 😅
                - Try [this](<http://bit.ly/2r0HhGB>)
## 6.6 Bitcoin Addresses, Balances, and Other Abstractions
- When looking at transaction structure, we understand that behind the scenes, pay scripts (with lock and unlock functions) replace the concept of bitcoin addresses and balances. Perhaps, we could say that these concepts are completely absent from the system except in th users' wallets.

- **"So what's the information displayed in the blockchain explorer?"**
    - Information retrieved from the previous transaction UTXOs and their locking scripts, to produce balances, and, recepients
    - Then, the extracted public key hash which is encoded to Base58Check, to produce the public key
- **How are balances produced?**
    - **Total received**
        - Decode the Base58Check encoding of the bitcoin address to receive the 160-bit Pub. Key hash
        - Search through the DB of tx's looking for outputs with P2PKH locking scripts that contain the Pub Key hash
        - We calculate the total balance by summing up the value of all such transactions and values.
    - **Current balances**
        - From the UTXO (unspent txs output) set, we sum up the value of all unspent outputs referencing the questioned Pub. Key hash
- **How easy it is to do so?**
    - Have to index and search through dozens, hundreds, or even hundreds of thousands of TXs
    - This is done by consturcting mnay higher-level abstractions classes that search, inspect, and, manipulate many different transactions,
- **Why are we doing so?**
    - To provide a simplistic view of bitcoin transactions, that resembles bank checks from onse sener to one recipient
- Some transactions are not deocded and can be found at the following [link](<https://blockchain.info/strange-transactions>)