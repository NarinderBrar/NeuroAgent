https://towardsdatascience.com/beginners-guide-to-custom-environments-in-openai-s-gym-989371673952

1.) Edit
/home/narinder/.local/lib/python3.8/site-packages/gym/envs/__init__.py

register(
    id='FooEnv-v0',
    entry_point='gym.envs.foo_env:FooEnv',
    reward_threshold=200,
    )

2.) Copy foo_env folder and paste in the follwing folder
/home/narinder/.local/lib/python3.8/site-packages/gym/envs/

3.)sudo gedit /.local/lib/python3.8/site-packages/gymz/gym_wrapper.py

4.) Run Unity Simulator

5.) Run folloing commands
gymz-controller gym gym_config.json
mpirun -np 6 music config.music
python bodySimulation.py