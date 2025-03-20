from gymnasium.envs.registration import register

register(
     id="ship-ice-v0",
     entry_point="benchnpin.environments.ship_ice_nav:ShipIceEnv",
     max_episode_steps=300,
)

register(
     id="box-delivery-v0",
     entry_point="benchnpin.environments.box_delivery:BoxDeliveryEnv",
     max_episode_steps=30000,
)

register(
     id="maze-NAMO-v0",
     entry_point="benchnpin.environments.maze_NAMO:MazeNAMO",
     max_episode_steps=400,
)


register(
     id="area-clearing-v0",
     entry_point="benchnpin.environments.area_clearing:AreaClearingEnv",
     max_episode_steps=30000,
)