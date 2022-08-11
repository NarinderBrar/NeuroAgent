in ~/.bashrc
alias python=python3

sudo apt-get install build-essential
sudo apt-get install python3-dev
sudo apt-get install libssl-dev
sudo apt-get install freeglut3-dev
sudo apt install automake
sudo apt install libopenmpi-dev
sudo apt install python3.8-distutils
sudo apt-get install libzmq3-dev
sudo apt install pkg-config libjsoncpp-dev libzmq3-dev libblas-dev libgsl-dev

mpirun --version

pip3 install numpy
pip3 install scipy
pip3 install matplotlib
pip3 install pyzmq

##Cmake
--------------------------------------------------------------
version=3.19
build=1
mkdir cmake
cd camke
wget https://cmake.org/files/v$version/cmake-$version.$build.tar.gz
tar -xzvf cmake-$version.$build.tar.gz
cd cmake-$version.$build/

./bootstrap
make
sudo make install
--------------------------------------------------------------

##MPI4PY
--------------------------------------------------------------
mpi4py-3.0.3.zip
python3 setup.py install
--------------------------------------------------------------

##Cython
--------------------------------------------------------------
cython-0.29.21.zip
python3 setup.py install
--------------------------------------------------------------

##MUSIC
--------------------------------------------------------------
MUSIC-release-1.1.17.zip

./autogen.sh
./configure --with-python=/usr/bin/python3
sudo make
sudo make install

move all files 
(config  __init__.py  pybuffer.la  pybuffer.so  __pycache__  pymusic.la  pymusic.so )
from:
/usr/local/lib/python3.8/dist-packages/music
to:
/usr/local/lib/python3.8/dist-packages/music

export PATH=/usr/local/bin/music:$PATH
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

music --version

Test examples:
MUSIC/examples
mpirun -np 4 music demo.music
MUSIC/pymusic/examples
mpirun -np 4 music helloworld.music
--------------------------------------------------------------

##MUSIC Adapter
--------------------------------------------------------------
mkdir build

cmake \
-DCMAKE_INSTALL_PREFIX:PATH=/home/user/Documents/music-adapters/build \
-DMUSIC_ROOT_DIR=/usr/local/bin/music \
/home/user/Documents/music-adapters

if cmake does not find mpi.h
cmake \
-DCMAKE_INSTALL_PREFIX:PATH=<PREFIX> -DMUSIC_ROOT_DIR=<MUSIC_INSTALL_PREFIX> -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpic++ <music-adapters_SOURCE>

Found MUSIC: /usr/local/lib/libmusic.so

make
make install

export PATH=/home/user/Documents/music-adapters/build/bin:$PATH
export LD_LIBRARY_PATH=/home/user/Documents/music-adapters/build/lib:$LD_LIBRARY_PATH
--------------------------------------------------------------

##NEST Simulator
--------------------------------------------------------------
mkdir build

NEST 3.3.zip

cmake \
-DCMAKE_INSTALL_PREFIX:PATH=/home/user/Documents/nest-simulator/build -Dwith-mpi=ON \
-Dwith-music=ON \
/home/user/Documents/nest-simulator

make
make install
make installcheck

export PYTHONPATH=/home/user/Documents/nest-simulator/build/lib/python3.8/site-packages:$PYTHONPATH
--------------------------------------------------------------

##VirtualHome
--------------------------------------------------------------
virtualhome-2.2.0.zip
linux_exec_2.2.0.zip

export PYTHONPATH=/home/user/Documents/NEST/build/lib/python3.8/site-packages:/home/user/Documents/VirtualHome:$PYTHONPATH
--------------------------------------------------------------

##OpenAI Gym
--------------------------------------------------------------
pip3 install gym
pip3 install gymz

https://towardsdatascience.com/beginners-guide-to-custom-environments-in-openai-s-gym-989371673952

move gym env in the following folder
/home/user/.local/lib/python3.8/site-packages/gym/envs/
--------------------------------------------------------------

sudo ln -s /usr/bin/python3 /usr/bin/python

in the python files
#!/usr/bin/env python3

Edit
/home/user/.local/lib/python3.8/site-packages/gym/envs/__init__.py

register(
    id='FooEnv-v0',
    entry_point='gym.envs.foo_env:FooEnv',
    reward_threshold=200,
    )

Copy foo_env folder and paste in the follwing folder
/home/user/.local/lib/python3.8/site-packages/gym/envs/

sudo gedit /.local/lib/python3.8/site-packages/gymz/gym_wrapper.py

Run Unity Simulator

Run folloing commands
gymz-controller gym gym_config.json
mpirun -np 6 music config.music
python bodySimulation.py


https://github.com/INM-6/nestrl-tutorial