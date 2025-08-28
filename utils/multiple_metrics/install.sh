sudo apt-get update
#install c-sharp environment
sudo apt-get install mono-runtime mono-complete -y
#install php
sudo apt-get install php -y
#install javascript
sudo apt-get install nodejs npm -y
#install typescript
# mkdir -p /usr/lib/npm/
# tar -xzf /zips/node-v16.14.0-linux-x64.tar.gz -C /usr/lib/npm/
# export PATH=$PATH:/usr/lib/npm/node-v16.14.0-linux-x64/bin/
npm install -g typescript
#install java
mkdir -p /usr/lib/jvm
sudo tar -xzf /root/zip/jdk-8u421-linux-x64.tar.gz -C /usr/lib/jvm

# Get the actual extracted directory name
JAVA_DIR=$(ls /usr/lib/jvm/ | grep jdk | head -1)
export JAVA_HOME="/usr/lib/jvm/$JAVA_DIR"

# Set environment variables permanently
echo "export JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> ~/.bashrc

# Also set for current session
export PATH=$JAVA_HOME/bin:$PATH

echo "Java installed at: $JAVA_HOME"
echo "JAVA_HOME and PATH have been added to ~/.bashrc"
echo "Please run 'source ~/.bashrc' or restart your terminal to apply changes"

#c++
sudo apt-get install libboost-all-dev -y
# cd /zips/boost_1_76_0
# ./bootstrap.sh --prefix=/usr/local
# sudo ./b2 install
# export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH