# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 500
FPS = 60

# Colors
SKY_COLOR = (100, 150, 255)  # Brighter blue
GROUND_COLOR = (100, 200, 100)  # Grass green
PLAYER_COLOR = (255, 50, 50)  # Red
BLOCK_COLOR = (150, 75, 0)  # Brown brick
BLOCK_SHADOW = (100, 50, 0)  # Darker brown
PIT_COLOR = (30, 30, 30)  # Dark gray/black
GOAL_COLOR = (255, 215, 0)  # Gold
COIN_COLOR = (255, 223, 0)  # Gold/Yellow
ENEMY_COLOR = (150, 0, 150)  # Purple
CLOUD_COLOR = (255, 255, 255, 150)  # Semi-transparent white
SPIKE_COLOR = (80, 80, 80)  # Dark gray
SPIKE_OUTLINE = (50, 50, 50)  # Darker gray

# Player settings
PLAYER_SIZE = 30
PLAYER_SPEED = 6  # Increased speed for easier movement
JUMP_FORCE = -15  # Stronger jump for easier obstacle clearing
GRAVITY = 0.45  # Slightly lower gravity for better control

# Game settings
GROUND_Y = 400
MAX_STEPS = 1200  # Increased time limit for longer level

# Coin settings
COIN_RADIUS = 10
COIN_VALUE = 10  # Points per coin
COIN_COLLECT_REWARD = 5  # RL reward for collecting a coin

# AI/RL settings
LEARNING_RATE = 0.15
DISCOUNT_FACTOR = 0.99
EPSILON_START = 1.0  # Start with full exploration
EPSILON_MIN = 0.05  # Minimum exploration rate
EPSILON_DECAY = 0.997  # Decay rate per episode

# Actions - Including combined actions for better performance
ACTIONS = {
    0: "NONE",
    1: "LEFT", 
    2: "RIGHT",
    3: "JUMP",
    4: "RIGHT+JUMP",  # Critical for jumping over obstacles while moving!
    5: "LEFT+JUMP"
}
NUM_ACTIONS = 6

# Level-specific settings (optional - for future use)
LEVEL_COLORS = {
    1: {
        'sky': (100, 150, 255),
        'ground': (100, 200, 100)
    },
    2: {
        'sky': (120, 170, 255),
        'ground': (90, 180, 90)
    },
    3: {
        'sky': (80, 130, 255),
        'ground': (80, 160, 80)
    }
}

# Reward values for different events
REWARDS = {
    'goal_reached': 100,
    'coin_collected': COIN_COLLECT_REWARD,
    'coin_bonus_multiplier': 2,  # Multiply coins by this at goal
    'pit_death': -50,
    'spike_death': -40,
    'enemy_death': -35,
    'block_collision': -30,
    'forward_movement': 0.5,  # Per pixel forward
    'step_penalty': -0.05,  # Small penalty to encourage speed
    'backward_movement': -0.3,  # Discourage going backwards
    'timeout': -20,  # Failed to complete in time
    'jump_over_pit': 2  # Bonus for successfully jumping over pit
}

# State space parameters (for documentation)
STATE_SPACE = {
    'obstacle_type': ['none', 'pit', 'block', 'spike', 'enemy'],  # 0-4
    'distance_bucket': ['very_close', 'close', 'medium_close', 'medium', 'medium_far', 'far', 'none'],  # 0-6
    'jump_state': ['on_ground', 'jumping_up', 'at_peak', 'falling'],  # 0-3
    'over_pit': ['safe', 'over_pit'],  # 0-1
    'obstacle_width': ['narrow', 'wide']  # 0-1
}

# Training parameters
TRAINING_DEFAULTS = {
    'episodes_per_level': {
        1: 2000,  # Level 1 - easier, needs less training
        2: 2500,  # Level 2 - medium difficulty
        3: 3000   # Level 3 - harder, needs more training
    },
    'progressive_training_episodes': 1500  # Episodes per level in progressive mode
}

# Display settings
SHOW_DEBUG_STATE = True  # Show current state on screen
SHOW_POLICY_SAMPLES = 10  # Number of policy samples to show after training

# File names for saving/loading
SAVE_FILES = {
    'q_table_level_1': 'q_table_level1.json',
    'q_table_level_2': 'q_table_level2.json',
    'q_table_level_3': 'q_table_level3.json',
    'q_table_all_levels': 'q_table_all_levels.json',
    'stats_level_1': 'training_stats_level1.json',
    'stats_level_2': 'training_stats_level2.json',
    'stats_level_3': 'training_stats_level3.json',
    'stats_all_levels': 'training_stats_all_levels.json'
}

# Level difficulty parameters (for level generation)
LEVEL_PARAMS = {
    1: {
        'pit_widths': [60, 70],
        'block_heights': [40, 50],
        'spacing_min': 180,
        'spacing_max': 250,
        'num_patterns': 8,
        'coins_per_pattern': 4
    },
    2: {
        'pit_widths': [70, 90],
        'block_heights': [50, 60],
        'spacing_min': 150,
        'spacing_max': 220,
        'num_patterns': 10,
        'coins_per_pattern': 5
    },
    3: {
        'pit_widths': [75, 100],
        'block_heights': [55, 65],
        'spacing_min': 120,
        'spacing_max': 200,
        'num_patterns': 12,
        'coins_per_pattern': 5
    }
}

# Performance monitoring
PRINT_PROGRESS_EVERY = 25  # Print training progress every N episodes
WIN_RATE_WINDOW = 100  # Calculate win rate over last N episodes