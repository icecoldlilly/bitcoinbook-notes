[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

# Bitcoin Book Notes
This repository contains personal notes and code snippets I have been aggrigating while reading ["The Bitcoin Book"](http://github.com/bitcoinbook/bitcoinbook)
### Compiling

In order to obtain the latest copy of the book,
Please make sure you have the following installed:

#### macOS
```
brew install git
brew install asciidoc
```
#### Linux
```
apt-get / yum install git
apt-get / yum install asciidoc
```

Then please use the following snippet:
```
git clone https://github.com/bitcoinbook/bitcoinbook
git checkout 'develop'
a2x -f epub --no-xmllint ./book.asciidoc
```
### Notes

I have extracted the notes from iBooks using [Klib](<http://klib.me>), feel free to use the same tool.
### Code

You can check out the code for this repo at [/code](/code/)

Here are some more [notes](/code/README.md) in regards to the code snippets