from simulation.unity_simulator import comm_unity

comm = comm_unity.UnityCommunication()

env_id = 0 # env_id ranges from 0 to 6
comm.reset(env_id)

s, g = comm.environment_graph()

comm.add_character('Chars/Male4', initial_room='kitchen')
comm.add_character('Chars/Female1', initial_room='kitchen')

# comm.add_camera(position=[0,10,0], rotation=[0,0,0])

# Put salmon in microwave
script = [
    '<char0> [WalkForward] () | <char1> [walk] <salmon> (328)',
    '<char0> [TurnRight] () | <char1> [grab] <salmon> (328)',
    '<char0> [TurnRight] () | <char1> [open] <microwave> (314)',
    '<char0> [TurnRight] () | <char1> [putin] <salmon> (328) <microwave> (314)',
    '<char0> [TurnRight] () | <char1> [close] <microwave> (314)'
]

for script_instruction in script:
    comm.render_script([script_instruction], recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])