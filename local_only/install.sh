#!/bin/bash
export DSS_VERSION='11.0.0'
export PY_VERSION='3.7.9'
export USER=dku
mkdir dataiku
echo 'Downloading...'
curl https://downloads.dataiku.com/public/studio/$DSS_VERSION/dataiku-dss-$DSS_VERSION.tar.gz --output dataiku-dss-$DSS_VERSION.tar.gz
tar -xvf dataiku-dss-$DSS_VERSION.tar.gz 
echo '⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱⏱'
echo 'Installing deps ⏱...'
sudo apt-get update
sudo apt-get install jq make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y
sudo apt-get install git-core -y
echo '🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍🐍'
echo 'Installing pyenv & python 🐍...'
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
sed -Ei -e '/^([^#]|$)/ {a \
export PYENV_ROOT="$HOME/.pyenv"
a \
export PATH="$PYENV_ROOT/bin:$PATH"
a \
' -e ':a' -e '$!{n;ba};}' ~/.profile
echo 'eval "$(pyenv init --path)"' >>~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'alias design="/home/$USER/dataiku/design/bin/dss start"' >> ~/.bashrc
source ~/.profile
source ~/.bashrc
pyenv install $PY_VERSION 
pyenv global $PY_VERSION
echo '🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦🐦'
echo 'Installing dataiku 🐦...'
sudo -i "/home/$USER/dataiku-dss-$DSS_VERSION/scripts/install/install-deps.sh" -yes
./dataiku-dss-$DSS_VERSION/installer.sh -t design -d ./dataiku/design -p 11000 -P $(which python)
sudo -i "/home/$USER/dataiku-dss-$DSS_VERSION/scripts/install/install-boot.sh" "/home/$USER/dataiku/design" $USER
echo '👆Automatic server boot is already done👆'
rm -f ~/dataiku-dss-$DSS_VERSION.tar.gz 
/home/$USER/dataiku/design/bin/dss start
echo 'Done ✅'
echo '###################################################'
echo '              http://localhost:11000'
echo '###################################################'
exec bash