sudo apt-get update -y
sudo apt-get remove -y --purge man-db
sudo apt-get install -y libc-bin

wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
sudo apt-get install -y mongodb-org
wget http://131.123.42.38/lmcrs/v1.0.0/srcml_1.0.0-1_ubuntu20.04.deb
sudo dpkg -i srcml_1.0.0-1_ubuntu20.04.deb
wget http://131.123.42.38/lmcrs/v1.0.0/srcml-dev_1.0.0-1_ubuntu20.04.deb
sudo dpkg -i srcml-dev_1.0.0-1_ubuntu20.04.deb