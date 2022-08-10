from simulation.unity_simulator import comm_unity

YOUR_FILE_NAME = "/home/narinder/Documents/VirtualHome/simulation/unity_simulator/linux_exec.x86_64" # Your path to the simulator
port= "8080"

comm = comm_unity.UnityCommunication(
    file_name=YOUR_FILE_NAME,
    port=port
)

env_id = 0 # env_id ranges from 0 to 6
comm.reset(env_id)

comm.add_character('Chars/Male2')

script = ['<char0> [WalkForward] ({})']
success, message = comm.render_script(script, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])
print(success)
print(message)

import time
time.sleep(2)

script = ['<char0> [TurnRight] ({})']
success, message = comm.render_script(script, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])

print(success)
print(message)
