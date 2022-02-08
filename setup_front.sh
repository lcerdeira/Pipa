#!/bin/zsh
#caminho para o diretorio
caminho_dir=$(pwd)
cd UI
npm install
quasar build -m electron
cd 
cd ../../../
cd usr/share/icons
sudo mkdir Pipa
cd Pipa
caminho_icon=$(pwd)
cd ../../../../
cd usr/local/bin
sudo mkdir Pipa
cd Pipa
caminho_prin=$(pwd)
cd
cd $caminho_dir
cd UI/src/assets
sudo cp PipaLogo2.png $caminho_icon

cd
cd $caminho_dir
cd .. 
sudo cp -r pipa_090421 $caminho_prin

