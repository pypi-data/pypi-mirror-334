from gymnasium.envs.registration import register

register(
     id="CliffCircular-v1",
     entry_point="cliffcircular.cliffcircular:CliffCircularEnv",
     kwargs={
         'render_mode': 'human',
         'extra_cliff_num': 1,
         'reset_extra_cliff_on_episode_begin': True,
         'obs_side_len': 5,
         'obs_include_loc': False,
         'obs_include_past_actions_num': 0,
         'disable_no_op_act': False,
         'cost_downscale_denom': 5,
         'punish_meaningless_action': False,
         'boost_finish_reward': False,
         'max_episode_steps': 32,
     }
)