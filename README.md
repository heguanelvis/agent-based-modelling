# Simple ABM Implementation
Thomas Schelling created an agent based model using checker boards to simulate the creation of segregated neighborhoods, in a society where no individual necessarily has a strong preference for segregation. To see a simulation with a visual component, visit the bottom of this page: http://nifty.stanford.edu/2014/mccown-schelling-model-segregation/

### Running the model
Specify the parameters in program.py file and execute the file, you will see a result.csv within the same directory

### params
1. same_pref: the percentage of neighbors that need to be the same kind as the agent to make the agent happy (there are two types of agent: red and blue)

2. agent_prop: the percentage of agents that are red; the percentage of blue = 1 - agent_prop

3. move_anyway: true if the agent moves to a random free location first and checks happiness afterwards; false if the agent checks happiness before moving to the location