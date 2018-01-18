git clone https://github.com/libbitcoin/libbitcoin ./lib
cd ./lib
brew install autoconf automake libtool pkgconfig wget
brew install boost
chmod +x install.sh
sudo ./install.sh