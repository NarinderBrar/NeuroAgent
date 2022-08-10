#!/bin/bash
gymz-controller gym gym_config.json &
mpirun -np 6 music config.music