class Agent():
    def __init__(self, world, kind, same_pref):
        self.world = world
        self.kind = kind
        if kind == "red":
            self.same_pref = same_pref["red"]
        else:
            self.same_pref = same_pref["blue"]
        self.location = None

    def move(self, move_anyway=False):
        """ 
        returns 0 for happy, 
        1 for unhappy but moved, 
        and 2 for unhappy and couldn't move 
        """

        happy = self.am_i_happy()

        if not happy:
            vacancies = self.world.find_vacant(return_all=True)

            i_moved = False
            if move_anyway:                                    
                choice_index = random.choice(range(len(vacancies)))
                patch = vacancies[choice_index]

                self.world.grid[self.location] = None
                self.location = patch
                self.world.grid[patch] = self
                i_moved = True

                happy_now = self.am_i_happy(loc=patch)

                if happy_now:
                    return 0
                else:
                    return 1

            else:
                for patch in vacancies:
                    will_i_like_it = self.am_i_happy(loc=patch)
                    if will_i_like_it:
                        self.world.grid[self.location] = None
                        self.location = patch
                        self.world.grid[patch] = self
                        i_moved = True
                        return 1

            if i_moved is False:
                return 2

        else:
            return 0

    def am_i_happy(self, loc=False, neighbor_check=False):
        """
        returns a boolean for whether or not an agent is happy at a location
        if loc is False, use current location, else use specified location
        """

        if not loc:
            starting_loc = self.location
        else:
            starting_loc = loc

        neighbor_patches = self.world.locate_neighbors(starting_loc)
        neighbor_agents = [self.world.grid[patch]
                           for patch in neighbor_patches]
        neighbor_kinds = [
            agent.kind for agent in neighbor_agents if agent is not None
        ]
        num_like_me = sum([kind == self.kind for kind in neighbor_kinds])

        if neighbor_check:
            return [kind == self.kind for kind in neighbor_kinds]

        if len(neighbor_kinds) == 0:
            return False

        perc_like_me = num_like_me / len(neighbor_kinds)

        if perc_like_me < self.same_pref:
            return False
        else:
            return True
