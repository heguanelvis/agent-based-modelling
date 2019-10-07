from Agent import Agent
from numpy import random, mean

class World():
    def __init__(self, params):
        assert(params["world_size"][0] * params["world_size"][1] >
               params["num_agents"]), "Grid too small for number of agents."
        self.params = params
        self.reports = {}

        self.grid = self.build_grid(params["world_size"])
        self.agents = self.build_agents(
            params["num_agents"], params["same_pref"]
        )

        self.init_world()

    def build_grid(self, world_size):
        """create the world that the agents can move around on"""

        locations = [(i, j) for i in range(world_size[0])
                     for j in range(world_size[1])]
        return {l: None for l in locations}

    def build_agents(self, num_agents, same_pref):
        """generate a list of Agents that can be iterated over"""

        def _kind_picker(i, agent_prop):
            if i < round(num_agents * agent_prop):
                return "red"
            else:
                return "blue"

        agents = [Agent(self, _kind_picker(
            i, self.params["agent_prop"]), same_pref) for i in range(num_agents)]
        random.shuffle(agents)
        return agents

    def init_world(self):
        """a method for all the steps necessary to create the starting point of the model"""

        for agent in self.agents:
            loc = self.find_vacant()
            self.grid[loc] = agent
            agent.location = loc

        assert(all([agent.location is not None for agent in self.agents])
               ), "Some agents don't have homes!"
        assert(sum([occupant is not None for occupant in self.grid.values()]) == self.params["num_agents"]
               ), "Mismatch between number of agents and number of locations with agents."

        self.reports["overall_integration"] = []
        self.reports["red_integration"] = []
        self.reports["blue_integration"] = []

    def find_vacant(self, return_all=False):
        """
        finds all empty patches on the grid and returns a random one, 
        unless kwarg return_all == True,
        then it returns a list of all empty patches
        """

        empties = [loc for loc, occupant in self.grid.items()
                   if occupant is None]
        if return_all:
            return empties
        else:
            choice_index = random.choice(range(len(empties)))
            return empties[choice_index]

    def locate_neighbors(self, loc):
        """given a location, return a list of all the patches that count as neighbors"""

        include_corners = True

        x, y = loc
        cardinal_four = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        if include_corners:
            corner_four = [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
            neighbors = cardinal_four + corner_four
        else:
            neighbors = cardinal_four

        x_max = self.params["world_size"][0] - 1
        y_max = self.params["world_size"][1] - 1

        def _edge_fixer(loc):
            x, y = loc
            if x < 0:
                x = x_max
            elif x > x_max:
                x = 0

            if y < 0:
                y = y_max
            elif y > y_max:
                y = 0

            return (x, y)

        neighbors = [_edge_fixer(loc) for loc in neighbors]
        return neighbors

    def split_kind(self):                                            
        self.agents_split = {"red": [], "blue": []}
        for agent in self.agents:
            if agent.kind == "red":
                self.agents_split["red"].append(agent)
            else:
                self.agents_split["blue"].append(agent)

    def report_integration(self, kind="all"):                        
        if kind == "all":
            diff_neighbors = []
            for agent in self.agents:
                diff_neighbors.append(sum(
                    [not a for a in agent.am_i_happy(neighbor_check=True)]
                ))
            self.reports["overall_integration"].append(
                round(mean(diff_neighbors), 2))
        else:
            diff_neighbors = {kind: []}
            for agent in self.agents_split[kind]:
                diff_neighbors[kind].append(sum(
                    [not a for a in agent.am_i_happy(neighbor_check=True)]
                ))
            self.reports[f"""{kind}_integration"""].append(
                round(mean(diff_neighbors[kind]), 2))

    def run(self):
        """handle the iterations of the model"""

        log_of_happy = []
        log_of_moved = []
        log_of_stay = []

        log_of_happy_red = []                                        
        log_of_moved_red = []
        log_of_stay_red = []

        log_of_happy_blue = []
        log_of_moved_blue = []
        log_of_stay_blue = []

        self.split_kind()
        self.report_integration()
        self.report_integration("red")
        self.report_integration("blue")

        log_of_happy.append(sum([a.am_i_happy()
                                 for a in self.agents]))
        log_of_moved.append(0)
        log_of_stay.append(0)

        log_of_happy_red.append(sum([a.am_i_happy()
                                     for a in self.agents_split["red"]]))
        log_of_moved_red.append(0)
        log_of_stay_red.append(0)

        log_of_happy_blue.append(sum([a.am_i_happy()
                                      for a in self.agents_split["blue"]]))
        log_of_moved_blue.append(0)
        log_of_stay_blue.append(0)

        for iteration in range(self.params["max_iter"]):
            random.shuffle(self.agents)

            moves = [{agent.kind: agent.move(self.params["move_anyway"])}     
                     for agent in self.agents]
            move_results_red = list(map(lambda e: e["red"],
                                        list(filter(lambda agent: list(agent.keys())[0] == "red",
                                                    moves))))
            move_results_blue = list(map(lambda e: e["blue"],
                                         list(filter(lambda agent: list(agent.keys())[0] == "blue",
                                                     moves))))
            move_results_all = list(map(lambda e: list(e.values())[0],
                                        moves))

            self.split_kind()
            self.report_integration()
            self.report_integration("red")
            self.report_integration("blue")

            num_happy_at_start = sum(
                [r == 0 for r in move_results_all])      
            num_moved = sum([r == 1 for r in move_results_all])
            num_stayed_unhappy = sum([r == 2 for r in move_results_all])

            num_happy_at_start_red = sum([r == 0 for r in move_results_red])
            num_moved_red = sum([r == 1 for r in move_results_red])
            num_stayed_unhappy_red = sum([r == 2 for r in move_results_red])

            num_happy_at_start_blue = sum([r == 0 for r in move_results_blue])
            num_moved_blue = sum([r == 1 for r in move_results_blue])
            num_stayed_unhappy_blue = sum([r == 2 for r in move_results_blue])

            log_of_happy.append(num_happy_at_start)
            log_of_moved.append(num_moved)
            log_of_stay .append(num_stayed_unhappy)

            log_of_happy_red.append(num_happy_at_start_red)
            log_of_moved_red.append(num_moved_red)
            log_of_stay_red .append(num_stayed_unhappy_red)

            log_of_happy_blue.append(num_happy_at_start_blue)
            log_of_moved_blue.append(num_moved_blue)
            log_of_stay_blue .append(num_stayed_unhappy_blue)

            if log_of_moved[-1] == log_of_stay[-1] == 0:
                print(
                    "Everyone is happy!  Stopping after iteration {}.".format(iteration))
                break
            elif log_of_moved[-1] == 0 and log_of_stay[-1] > 0:
                print("Some agents are unhappy, but they cannot find anywhere to move to.  Stopping after iteration {}."
                      .format(iteration))
                break

        self.reports["log_of_happy"] = log_of_happy
        self.reports["log_of_moved"] = log_of_moved
        self.reports["log_of_stay"] = log_of_stay

        self.reports["log_of_happy_red"] = log_of_happy_red
        self.reports["log_of_moved_red"] = log_of_moved_red
        self.reports["log_of_stay_red"] = log_of_stay_red

        self.reports["log_of_happy_blue"] = log_of_happy_blue
        self.reports["log_of_moved_blue"] = log_of_moved_blue
        self.reports["log_of_stay_blue"] = log_of_stay_blue

        self.report(self.params["to_screen"], self.params["to_file"])

    def report(self, to_screen=True, to_file=True):                         
        """report final results after run ends"""

        reports = self.reports

        if to_screen:                                                       
            print("\nAll results begin at time=0 and go in order to the end.\n")
            print("The average number of neighbors an agent has not like them:",
                  reports["overall_integration"])
            print("The average number of neighbors a red agent has not like them:",
                  reports["red_integration"])                               
            print("The average number of neighbors a blue agent has not like them:",
                  reports["blue_integration"])                              
            print("The number of happy agents:",
                  reports["log_of_happy"])
            print("The number of moves per turn:",
                  reports["log_of_moved"])
            print("The number of agents who failed to find a new home:",
                  reports["log_of_stay"])
            print("The number of happy red agents:",
                  reports["log_of_happy_red"])                              
            print("The number of red moves per turn:",
                  reports["log_of_moved_red"])
            print("The number of red agents who failed to find a new home:",
                  reports["log_of_stay_red"])
            print("The number of happy blue agents:",
                  reports["log_of_happy_blue"])
            print("The number of blue moves per turn:",
                  reports["log_of_moved_blue"])
            print("The number of blue agents who failed to find a new home:",
                  reports["log_of_stay_blue"])

        if to_file:                                                         
            
            out_path = self.params["out_path"]
            with open(out_path, "w") as f:
                headers = "turn,overall_integration,red_integration,blue_integration,"
                headers += "num_happy,num_moved,num_stayed,num_happy_red,num_moved_red,num_stayed_red,"
                headers += "num_happy_blue,num_moved_blue,num_stayed_blue\n"
                f.write(headers)

                for i in range(len(reports["log_of_happy"])):               
                    line = ",".join([str(i),
                                     str(reports["overall_integration"][i]),
                                     str(reports["red_integration"][i]),
                                     str(reports["blue_integration"][i]),
                                     str(reports["log_of_happy"][i]),
                                     str(reports["log_of_moved"][i]),
                                     str(reports["log_of_stay"][i]),
                                     str(reports["log_of_happy_red"][i]),
                                     str(reports["log_of_moved_red"][i]),
                                     str(reports["log_of_stay_red"][i]),
                                     str(reports["log_of_happy_blue"][i]),
                                     str(reports["log_of_moved_blue"][i]),
                                     str(reports["log_of_stay_blue"][i]),
                                     "\n"
                                     ])
                    f.write(line)
            print("\nResults written to:", out_path)
