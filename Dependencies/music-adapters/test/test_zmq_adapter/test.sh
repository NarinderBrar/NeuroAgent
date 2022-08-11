#!/bin/bash
python sender.py&
LD_PRELOAD=$HOME/opt/MUSIC.install/lib/libmusic.so.1 env PATH=$HOME/opt/music-adapters.build/:$PATH mpirun -np 2 --oversubscribe ~/opt/MUSIC.install/bin/music test.music&
python receiver.py
