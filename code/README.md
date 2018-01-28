# Installation

#### Example 01 on macOS
1. Install the following
```bash
brew install autoconf automake libtool pkgconfig wget
brew install boost
brew install libbitcoin
```
2.  After installation compile code as following: `g++ -std=c++11 -o addr addr.cpp $(pkg-config --cflags --libs libbitcoin)`

#### Example 02 Python

Install Miniconda
```bash
curl -Ok https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -b -p ~/anaconda
rm Miniconda3-latest-MacOSX-x86_64.sh
echo 'export PATH="~/anaconda/bin:$PATH"' >> ~/.bash_profile 

# Refresh basically
source .bash_profile

conda update conda
```

Use conda to create environment and install requirements:

```bash
conda create env -n "name" python=3.6
pip install bitcoin
```

#### Example 02 notes
- Python 'bit' vs Python 'bitcoin':
  - 'Bit' stores keys in a compressed manner, every conversion to hex or any other format compresses the key automatically, while 'bitcoin' is uncompressed by nature, and stores the key by 'hex'
  - 'bitcoin' allows decompression
  - 'bit' is an interface of coincurve, which isn't a full implementation of the bitcoin protcol in python