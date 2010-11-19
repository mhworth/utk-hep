# install necessary packages
yum install httpd mysql-devel httpd-devel mysql-server gcc-c++ vim bzip2-devel zlib-devel gdbm-devel ncurses-devel readline-devel sqlite-devel

# Get Python 2.6
mkdir ~/tmp
cd ~/tmp
wget http://python.org/ftp/python/2.6.6/Python-2.6.6.tgz
tar -xzvf Python-2.6.6.tgz
cd Python-2.6.6
./configure --prefix=/usr/local
make -j2
make install

 
# After python -V returns 2.6.6, run install-python-packages.sh
