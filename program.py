import os
from World import World

params = {
    "world_size": (40, 40),
    "num_agents": 1330,
    "same_pref": {                                             
        "red": 0.4,
        "blue": 0.7
    },
    "max_iter": 100,
    "agent_prop": 0.3,   # red = agent_prop * num_agents       
    "to_screen": True,                                         
    "to_file": True,                                           
    "out_path": f"""{os.getcwd()}\\results.csv""",
    "move_anyway": False                                       
}

world = World(params)
world.run()
