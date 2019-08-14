# Hybrid Reward Architecture with Stanford CS221 Pacman

The motivation behind this is Stanford CS221 Pacman homework where we had to implement Expectimax with a static evaluation function and the top three scores were rewarded. 
After finishing CS221 read the Hybrid Reward Architecture paper from: https://papers.nips.cc/paper/7123-hybrid-reward-architecture-for-reinforcement-learning.pdf and decided to make the Pacman a bit smarter using Reinforcement Learning. 

The Fruit Collection task example from the HRA paper was taken as basis for this implementation. 

The following GFVs and Heads were defined:
    
    - one head/gvf per food point and capsules
    - two heads for the ghosts and a number of gvfs equal to the number of possible pacman locations, i.e. all locations not having a wall. At each pacman location the heads are reset to the gvfs corresponding to their current location. 
    - for the scared ghosts a similar approach was taken as for the regular ghosts 
    - diversification explorer head which adds random q values between [0, 20] for a configurable number of steps to allow each episode to start randomly
    
Each GVF is configured with virtual rewards and the calculated q values are at the end multiplied by the actual game rewards/points.

At the end to aggregate the q values, two aggregation methods were implemented, as described in the orginal paper: 

    - a linear aggregator summing all q values and then taking the action with the largest q value
    - a custom aggregator taking all heads with a positive reward and normalizes them and adding the negative q values weighted by a weight vector

See hra/config.yaml for the set of configurable parameters.

A pre-trained HRA Pacman on 200 games is available in this repo and a series of ten games can be viewed here: https://www.youtube.com/watch?v=iDUfI4soSxI

To let pacman with HRA play, type: python pacman.py -l smallClassic -p HRAAgent
To train pacman with HRA, type: python pacman.py -l smallClassic -p HRAAgent -a learn=True -q -n 200

For help, type:  python pacman.py -h 
See http://inst.eecs.berkeley.edu/~cs188 for more information about the pacman game.

Enjoy!
