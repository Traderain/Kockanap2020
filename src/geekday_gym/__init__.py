from gym.envs.registration import register

register(
    id='Geekday-v0',
    entry_point='geekday_gym.envs:GeekdayGym',
    max_episode_steps=50,
)