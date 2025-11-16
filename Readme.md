\# Super Mario RL - Powered-Up Coin Adventure

A Mario platformer with **ALL obstacles** (Pits, Blocks, Spikes, Enemies) made **easy to beat** through **SUPER MARIO POWERS** using Reinforcement Learning!

## The Perfect Balance

**ALL obstacle types included** - Full game experience!
**SUPER MARIO POWERS** - Speed 7, Jump -16, Better control!
**Obstacles made easier** - Smaller, well-spaced
**Long level** with ~200 coins
**Safe zones** between obstacles
**Gentler penalties** - Focus on learning
**High success rate** - 80%+ completions!

## Game Objective

**Complete Adventure with SUPER POWERS:**

1.  **Use your enhanced abilities** - Fast & high jumps!
2.  **Collect ~200 coins** throughout the level
3.  **Navigate ALL obstacle types** - made easier
4.  **Reach the goal** - totally achievable!
5.  **Maximize score** - perfect runs possible!

## SUPER MARIO POWERS

```python
Speed:    7  (+40% faster than normal!)
Jump:    -16  (+14% higher than normal!)
Gravity: 0.4  (+20% better air control!)
Time:    1500 steps (87% more time!)
```

**Mario is POWERED UP to easily handle everything!**

## 🌟 Features

- **Beginner-Friendly Level** with ~150 coins
- **Easy obstacles** - small pits and low blocks only
- **Well-spaced design** - no consecutive obstacles
- **Better movement** - faster speed (6) and stronger jump (-15)
- **More time** - 1200 steps to complete
- **Perfect Run Bonus** - collect all coins for extra reward
- **Smart AI** that learns to complete the level consistently

## Scoring System

```
Final Score = Base Points + Coin Bonus + Time Bonus + Perfect Bonus

• Coin Collected: +10 points each
• Completion Bonus: +200 points
• Coin Bonus: +5 per coin at goal
• Time Bonus: Up to +50 points (faster = more)
• Perfect Bonus: +100 points (all coins collected)
```

**Maximum Possible Score: ~2500+ points!**

## ⚙️ Easy Mode Settings

```python
# Player (Enhanced for easier gameplay)
PLAYER_SPEED = 6          # Faster movement
JUMP_FORCE = -15          # Stronger jump
GRAVITY = 0.45            # Better control

# Level (Longer and easier)
MAX_STEPS = 1200          # More time
Obstacles: Only pits & blocks (no spikes/enemies)
Spacing: 280-320 pixels between obstacles
Pit Width: 50 pixels (easy to jump)
Block Height: 40 pixels (easy to clear)

# Penalties (Reduced)
Pit: -80 (was -100)
Block: -40 (was -50)
Step: -0.02 (was -0.05)
```

## 🎮 How to Play

### Installation

```bash
pip install pygame
```

### Run the Game

```bash
python main.py
```

### Game Modes

#### 1️ Human Play Mode

Play the game yourself and try to beat your best time!

**Controls:**

- **Arrow Keys**: Move left/right
- **SPACE**: Jump
- **RIGHT + SPACE**: Jump while moving (recommended!)
- **ESC**: Quit

**Tips:**

- This version is designed to be completable!
- Obstacles are well-spaced - take your time
- Better jump means you can clear obstacles easily
- More time limit - no need to rush
- Focus on collecting coins, the level is forgiving

#### AI Train Mode

Train an AI agent to master the level

**Training Focus:**

- Complete the level consistently
- Collect coins throughout
- Navigate easy obstacles
- Achieve high win rate (80%+)

**Recommended Episodes:** 2000-3000 (easier = faster learning!)

**Training Output:**

```
Episode   Result  Time      Score     Coins           Epsilon     Win Rate
----------------------------------------------------------------------------------
50        32/50   42.5      280       78.2/150 (52%)  0.7784      64.00%
100       68/100  38.2      520       105.8/150 (71%) 0.6058      68.00%
500       410/500 32.1      890       132.5/150 (88%) 0.2156      82.00%
1000      850/1000 28.3     1250      142.3/150 (95%) 0.0852     85.00%
```

#### AI Test Mode

Watch your trained AI play and optimize!

**What to observe:**

- Route optimization
- Coin collection strategy
- Jump timing
- Trade-offs between speed and coins

## RL Details

### State Space

The AI observes:

- **Obstacle type** (pit, block, spike, enemy)
- **Distance to obstacle** (very close → far)
- **Jump state** (ground, rising, peak, falling)
- **Over pit** (safe/dangerous)
- **Nearest coin distance** (nearby, close, far)
- **Nearest coin height** (low, mid, high)

### Action Space

- 0: Do nothing
- 1: Move left
- 2: Move right
- 3: Jump
- 4: **Right + Jump** (optimal for obstacles)
- 5: Left + Jump

### Reward Function

```python
Rewards:
  +5   : Collect coin
  +200 : Reach goal
  +50  : Time bonus (faster = more)
  +100 : Perfect run (all coins)
  +0.3 : Forward progress per pixel
  -100 : Fall in pit
  -60  : Hit spike
  -50  : Hit enemy or block
  -0.02: Per step (encourages efficiency)
```

### Learning Algorithm

- **Q-Learning** with Temporal Difference updates
- **Epsilon-greedy** exploration (1.0 → 0.05)
- **Learning rate**: 0.15
- **Discount factor**: 0.99

## Training Tips

### For Best Results:

1. **Start with 2000 episodes** (easier level = faster learning!)

   ```bash
   python main.py
   # Select: 2
   # Episodes: 2000
   ```

2. **Monitor these metrics:**

   - Win rate should reach 80%+ quickly
   - Coin collection should improve to 85%+
   - Level completion becomes consistent
   - Time becomes more stable

3. **Signs of good training:**

   - Win rate > 80% after 1500 episodes
   - Avg coins > 85% of total
   - Consistent completions
   - Q-table size: 600-1000 states

4. **If AI still struggles:**
   - Make obstacles even easier in config
   - Increase JUMP_FORCE to -16
   - Reduce pit widths in level generation
   - Train for 3000 episodes

## Challenge Goals

### Bronze: Complete the Level

- Reach the goal
- Time: < 50s
- Coins: > 50%

### Silver: Coin Collector

- Time: < 40s
- Coins: > 80%
- Score: > 1500

### Gold: Perfect Run

- Time: < 35s
- Coins: 100%
- Score: > 2200

## Files

```
main.py           - Game launcher
mario_env.py      - Game environment & physics
mario_agent.py    - Q-Learning AI agent
mario_config.py   - Configuration settings
q_table.json      - Trained AI model (generated)
training_stats.json - Training metrics (generated)
```

## Level Design

The level includes EASY, well-spaced challenges:

- **Coin Trails** - Ground coins (easy pickups)
- **Safe Spaces** - Long sections with just coins
- **Easy Pits** - Small (50px), well-spaced gaps
- **Single Blocks** - Low blocks easy to jump over
- **Coin Arcs** - Gentle patterns, easy to collect
- **Final Rush** - Dense coin clusters before goal (no obstacles!)

**Key Stats:**

- Total Coins: ~150
- Obstacles: 8-10 (widely spaced)
- Safe Spaces: Many!
- Pit Width: 50 pixels (easy)
- Block Height: 40 pixels (low)
- Spacing: 280-320 pixels between obstacles
- Level Length: ~5500 pixels
- Optimal Time: 30-40 seconds

## Configuration

Edit `mario_config.py` to adjust:

```python
# Difficulty
MAX_STEPS = 800          # Time limit
COIN_VALUE = 10          # Points per coin
COIN_COLLECT_REWARD = 5  # RL reward per coin

# Physics
PLAYER_SPEED = 5
JUMP_FORCE = -14
GRAVITY = 0.5

# AI Training
LEARNING_RATE = 0.15DISCOUNT_FACTOR = 0.99
EPSILON_DECAY = 0.997
```

## Performance Metrics

The game tracks:

- ️ **Completion time** (best time saved)
- **Coins collected** (% of total)
- **Final score** (with all bonuses)
- **Perfect runs** (100% coins)
- **Episode statistics** (for AI)

## Troubleshooting

**Game too hard?**

- Reduce MAX_STEPS in config
- Increase JUMP_FORCE slightly
- Train AI longer

**AI not collecting coins?**

- Increase COIN_COLLECT_REWARD
- Train for more episodes
- Check coin detection radius

**Want more coins?**

- Edit level generation in `mario_env.py`
- Duplicate coin patterns
- Adjust coin placement

## Educational Value

This project demonstrates:

- **Reinforcement Learning** - Q-Learning algorithm
- **Multi-objective optimization** - Balancing speed vs. coins
- **State space design** - Relevant features for decision-making
- **Reward shaping** - Encouraging desired behaviors
- **Exploration vs. exploitation** - Epsilon-greedy strategy

## Future Ideas

- Add more obstacle types
- Power-ups (speed boost, invincibility)
- Multiple difficulty levels
- Leaderboard system
- Replay saving
- Deep Q-Network (DQN) implementation
