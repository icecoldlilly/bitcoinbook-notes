# Chapter 05
- At a high level, a wallet is an application that serves as the primary user interface

- controls access to a user’s money, managing keys and addresses, tracking the balance, and creating and signing transactions.

- from a programmer’s perspective, the word "wallet" refers to the data structure used to store and manage a user’s keys.

- wallets are containers for private keys, usually implemented as structured files or simple databases.

- we summarize the various technologies used to construct user-friendly, secure, and flexible bitcoin wallets

- The "coins" are recorded in the blockchain on the bitcoin network.

- Users control the coins on the network by signing transactions with the keys in their wallets

- a bitcoin wallet is a keychain.

- Each user has a wallet containing keys

- Wallets are really keychains containing pairs of private/public keys

- Users sign transactions with the keys, thereby proving they own the transaction outputs

- The coins are stored on the blockchain in the form of transaction outputs

- There are two primary types of wallets, distinguished by whether the keys they contain are related to each other or not.

- nondeterministic wallet

- each key is independently generated from a random number.

- not related to each other.

- known as a JBOK wallet from the phrase "Just a Bunch Of Keys."

- deterministic wallet

- all the keys are derived from a single master ke

- seed

- keys

- are related to each other and can be generated again if one has the original seed.

- key derivation methods

- ost commonly used derivation

- tree-like structure

- hierarchical deterministic

- HD wallet.

- Deterministic wallets are initialized from a seed

- make these easier

- encoded as English words

- mnemonic code words

- disadvantage of random keys

- if you generate many of them you must keep copies of all of them

- Each key must be backed up, or the funds it controls are irrevocably lost if the wallet becomes inaccessible

- Address reuse reduces privacy by associating multiple transactions and addresses with each other

- A Type-0 nondeterministic wallet is a poor choice of wallet, especially if you want to avoid address reuse because it means managing many keys, which creates the need for frequent backups

- nondeterministic wallets is discouraged for anything other than simple tests

- industry-standard–based HD wallet with a mnemonic seed for backup.

- Deterministic, or "seeded," wallets are wallets that contain private keys that are all derived from a common seed

- use of a one-way hash function

- seed is a randomly generated number that is combined with other data

- index number or "chain code"

- a single backup at creation time is sufficient

- seed is sufficient to recover all the derived keys

- most advanced form

- HD wallet defined by the BIP-32 standard

- a parent key can derive a sequence of children keys

- tree structure

- the tree structure can be used to express additional organizational meaning,

- The second advantage of HD wallets is that users can create a sequence of public keys without having access to the corresponding private keys

- This allows HD wallets to be used on an insecure server or in a receive-only capacity, issuing a different public key for each transaction.

- The public keys do not need to be preloaded or derived in advance

- yet the server doesn’t have the private keys that can spend the funds.

- They are even more useful if they are combined with a standardized way of creating seeds from a sequence of English words that are easy to transcribe, export, and import across wallets

- mnemonic

- standard is defined by BIP-39

- can import and export seeds for backup and recovery using interoperable mnemonics.

- If you are implementing a bitcoin wallet, it should be built as a HD wallet, with a seed encoded as mnemonic code for backup, following the BIP-32, BIP-39, BIP-43, and BIP-44

- Mnemonic code words are word sequences that represent (encode) a random number used as a seed to derive a deterministic wallet.

- That sequence of words is the wallet backup and can be used to recover and re-create all the keys in the same or any compatible wallet application.

- Mnemonic words are often confused with "brainwallets."

- The primary difference is that a brainwallet consists of words chosen by the user, whereas mnemonic words are created randomly by the wallet and presented to the user.

- mnemonic words much more secure, because humans are very poor sources of randomness.

- Mnemonic codes are defined in BIP-39

- BIP-39 was proposed by the company behind the Trezor hardware wallet and is incompatible with Electrum’s implementation

- BIP-39 has now achieved broad industry support

- BIP-39 defines the creation of a mnemonic code and seed, which we describe here in nine steps.

- Mnemonic words are generated automatically by the wallet using the standardized process defined in BIP-39

- The mnemonic words represent entropy with a length of 128 to 256 bits.

- used to derive a longer (512-bit) seed

- use of the key-stretching function PBKDF2.

- deterministic wallet and derive its keys.

- two parameters: the mnemonic and a salt.

- salt

- make it difficult to build a lookup table enabling a brute-force attack

- salt has another purpose

- additional security factor protecting the seed

- allows the introduction of a passphrase

- PBKDF2 key-stretching function is the

- mnemonic

- salt is composed of the string constant "mnemonic" concatenated with an optional user-supplied passphrase string

- PBKDF2 stretches the mnemonic and salt parameters using 2048 rounds of hashing with the HMAC-SHA512 algorithm,

- producing a 512-bit value as its final output. That 512-bit value is the seed

- The BIP-39 standard allows the use of an optional passphrase in the derivation of the seed.

- mnemonic is stretched with a salt consisting of the constant string "mnemonic"

- If a passphrase is used, the stretching function produces a different seed from that same mnemonic

- every possible passphrase leads to a different seed. Essentially, there is no "wrong" passphrase

- The set of possible wallets is so large (2512) that there is no practical possibility of brute-forcing or accidentally guessing one that is in use.

- A second factor (something memorized) that makes a mnemonic useless on its own

- If the wallet owner is incapacitated or dead and no one else knows the passphrase, the seed is useless and all the funds stored in the wallet are lost forever.

- considering the possibility of surviving the owner and allowing his or her family to recover the cryptocurrency estate.

### HD wallets
**Summary:** HD wallets are created from a single root seed, which is a 128-, 256-, or 512-bit random number.
  1. Every key in the HD wallet is deterministically derived from this root seed,
  2. Which makes it possible to re-create the entire HD wallet from that seed in any compatible HD wallet
  3. We could do so by simply transferring only the mnemonic that the root seed is derived from.

**Question:**  How do you create such wallet? (Graphically)

- ![Wallet creation work flow](https://github.com/bitcoinbook/bitcoinbook/blob/develop/images/mbc2_0509.png)

**Question:** So how do you derive a private child key of an HD wallet?
- HD wallets use a child key derivation (CKD) function to derive child keys from parent keys.
  - The child key derivation functions are based on a one-way hash function that combines:
    - A parent private or public key (ECDSA uncompressed key)
    - A seed called a chain code (256 bits)
    - An index number (32 bits)
  - These three items (parent key, chain code, and index) are combined and hashed to generate children keys, as follows.
  - **Algorithm:**
    - `hash = HMAC-SHA512(parent public key + chain code + index)`
      - `childChainCode = rightHalf256(hash)`
      - ` childPrivateKey = leftHalf256(hash)`


- **Remember the following:**
  - Knowing a child key does not make it possible to find its siblings, unless you also have the chain code and the parent key
  - The initial chain code seed (at the root of the tree) is made from the seed, while subsequent child chain codes are derived from each parent chain code.
  -  Each parent can create 2^31 children for infinite amount of generations
  -  Keys cannot be distinguished from nondeterministic keys
- **Uses of a child private key:**
  - To make a public key and a bitcoin address.
  - Sign off transactions and spend anything belonging to this child
- **Where can it be used?**
  - Wallet websites like coinbase, [copay.io](https://github.com/bitpay/bitcore-wallet-service), etc...
  - 