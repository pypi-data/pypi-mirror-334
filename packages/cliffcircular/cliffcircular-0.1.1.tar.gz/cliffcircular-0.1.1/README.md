# CliffCircular
CliffCircular involves navigating in a gridworld circularly while avoiding falling off a cliff.



https://github.com/user-attachments/assets/e9a16fa6-43b2-44bd-be26-1585cc7d7619



## Description
The game starts with the player at a random location of the 12x12 grid world.
If the player circulates the gridworld the episode ends.

A cliff runs along gridworld boundary, as well as the center area. If the player moves to a cliff location it
will be spawned randomly in a non-cliff grid.

The player makes moves until they run around the gridworld.

The grid world data structure is 2D numpy.array, where row number is array x dimension, column number
is array y dimension.

At most 2 extra cliff can be added to the gridworld with fixed cliff locations. Whether the extra cliff locations
need to be randomly re-generated on episode begin can also be toggled on env creation.

Adapted from [Gymnasium CliffWalking](https://gymnasium.farama.org/environments/toy_text/cliff_walking/)
environment, which is adapted from Example 6.6 (page 132) from Reinforcement Learning: An Introduction
by Sutton and Barto [<a href="#cliffwalk_ref">1</a>].

With inspiration from:
[https://github.com/dennybritz/reinforcement-learning/blob/master/lib/envs/cliff_walking.py](https://github.com/dennybritz/reinforcement-learning/blob/master/lib/envs/cliff_walking.py)

## Action Space
The action shape is `(1,)` in the range `[0, 4]` indicating
which direction to move the player.

- 0: No operation
- 1: Move up
- 2: Move right
- 3: Move down
- 4: Move left

Note this environment allows no_op movement, meaning standing still is also a valid movement for the agent.
This makes the agent behavior more realistic considering future involvement of multiple agents, in which condition
not moving can be an appropriate option in either cooperative or combating game.

## Observation Space
The flattened 'obs_side_len' x 'obs_side_len' grids around agent's current location (row major, top to bottom, MultiBinary)
indicating whether there is cliff or not.

If agent's current location is included in the observation, this scalar value representing the player's
current position as current_row * nrows + current_col (where both the row and col start at 0) will be
the first element preceding the above dim-9 observation, resulting in 10-dim MultiDiscrete([144]+[2]*9) observation.

## Starting State
The extra cliff(s) will be reset randomly first.
The episode starts with the player in random non-cliff grid, for example, `[26]` (location [2, 2]).


## Reward
The reward is calculated based on the number of newly visited central track grids, which are the central layer
squared grids in all 3 valid layers of grids.
In this 12 by 12 grid world, there are 20 central grids.
Agent's current grid will be projected onto this central track to update visitedness.
Any new visit of a central grid will incur +1 reward.
If 'punish_meaningless_action' argument is toggled on, the occurrence of repeated visit of a central track
grid will incur -1 reward, if no new central grids are visited in this step.
If the agent stepped into the cliff, the episode will be terminated with 0 reward.

## Cost
For non-terminal states, the cost is defined as the ratio of the number of cliff grids in the 3 by 3 square around
agent's current location, over 10. This ratio will then be downscaled by a user-defined integer argument (by default 5),
to reduce the effect of non-critical cost compared to the terminal cost.
The terminal cost 1 will be given when the agent steps onto the cliff grid.


## Reward & Cost Design Considerations
As such definitions of reward and cost, they are designed to have the same maximum value.
Besides, the rewards are designed to be task-dependent, which is agnostic to the consequences due to environment dynamics.
On the contrary, costs are designed to be environment-dependent, which is agnostic to the task in hand.
This decoupling of rewards and costs helps the RL agent learn separately what is desired by the task and
what is restricted by the environment.

## Episode End
The episode terminates when the agent has visited all central grids, or has stepped into any cliff grid.

## Information

`step()` and `reset()` return a dict with the following keys:
- "p" - transition probability for the state.
- "state" - current state's location index in flattened format
- "c" - cost incurred at the current state

As cliff circular is not stochastic, the transition probability returned is always 1.0.

## Arguments
- 'render_mode': None, or 'human', or 'ansi', or 'rgb_array'
- 'extra_cliff_num': 2, choose from {0, 1, 2}
- 'reset_extra_cliff_on_episode_begin': True,
- 'obs_side_len': 5,
- 'obs_include_loc': False,
- 'obs_include_past_actions_num': int,
- 'disable_no_op_act': bool,
- 'cost_downscale_denom': float,
- 'punish_meaningless_action': False,
- 'boost_finish_reward': False, add +100 reward if the agent circulates gridworld successfully
- 'max_episode_steps': int,

## Installation

To install the package from PyPI, ensure you have Python 3.8 or later and run:

```bash
pip install cliffcircular
```

Alternatively, to try the latest development version, clone the GitHub repository:

```bash
git clone https://github.com/EdisonPricehan/CliffCircular
cd CliffCircular
pip install -e .
```

## Usage

```python
import gymnasium as gym
gym.make('CliffCircular-v1')
```

Or execute the sample script
```bash
python examples/run_cliffcircular.py
```


## References
<a id="cliffwalk_ref"></a>[1] R. Sutton and A. Barto, “Reinforcement Learning:
An Introduction” 2020. [Online]. Available: [http://www.incompleteideas.net/book/RLbook2020.pdf](http://www.incompleteideas.net/book/RLbook2020.pdf)

<a id="cliffwalk_ref"></a>[2] [Cliff Walking Gymnasium environment](https://gymnasium.farama.org/environments/toy_text/cliff_walking/)

## Version History
- v0: Initial version release

- v1: Add Property method to get cliff grids (for visualization purpose)
      Return 0 reward instead of -100 once stepped on cliff grid, but 1 cost will be given
      Add agent's current integer location in 'info' dict with 'state' key, for 'reset' and 'step' function returns
      Provide options to include past action(s) into agent observation
      Incorporate cost in the tuple of returned agent step, and this cost can be scaled by argument
