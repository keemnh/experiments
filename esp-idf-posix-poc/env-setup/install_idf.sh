#!/usr/bin/env bash
brew install python3 git cmake ninja
git clone --recursive https://github.com/espressif/esp-idf.git ~/RiF/esp-idf
cd ~/RiF/esp-idf && ./install.sh