# Installation

## on macOS

1.  Install brew
2.  `brew install autoconf automake libtool pkgconfig wget`
3.  `brew install boost`
4.  `brew install libbitcoin`
5.  After installation compile code as following: `g++ -std=c++11 -o addr addr.cpp $(pkg-config --cflags --libs libbitcoin)`

