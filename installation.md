# Installation

## on macOS

1.  Install brew
2.  `brew install autoconf automake libtool pkgconfig wget`
3.  `brew install boost`
4.  `brew install libbitcoin`
5.  After installation compile code as following: `g++ -std=c++11 -o addr addr.cpp $(pkg-config --cflags --libs libbitcoin)`

## Python
conda create env -n "name" python=3.6
pip install bitcoin

##Notes
- Python 'bit' vs Python 'bitcoin':
  - 'Bit' stores keys in a compressed manner, every conversion to hex or any other format compresses the key automatically, while 'bitcoin' is uncompressed by nature, and stores the key by 'hex'
  - 'bitcoin' allows decompression
  - 'bit' is an interface of coincurve, which isn't a full implementation of the bitcoin protcol in python