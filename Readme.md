# Simplified Mario RL Game

A simplified Mario-style platformer game that can be solved using Reinforcement Learning (Q-Learning with TD learning).

## Game Description

- **Player**: Red square that can move left/right and jump
- **Obstacles**: Black pits (instant death) and gray blocks (collision damage)
- **Goal**: Golden square at the end of the level
- **Objective**: Navigate through obstacles to reach the goal

## Files Structure

```
main.py           - Entry point and mode selection
game.py           - Game environment and physics
ai_agent.py       - Q-Learning agent implementation
config.py         - Game and AI configuration
README.md         - This file
q_table.json      - Saved Q-table (generated after training)
training_stats.json - Training statistics (generated after training)
```

## Installation

```bash
pip install pygame
```

## How to Run

```bash
python main.py
```

Then select one of three modes:

### 1. Human Play Mode
- Test the game environment yourself
- **Controls:**
  - LEFT/RIGHT arrows: Move
  - SPACE: Jump
  - ESC: Quit

### 2. AI Train Mode
- Train the AI agent using Q-Learning (TD learning)
- Specify number of training episodes (default: 1000)
- Training data is saved to:
  - `q_table.json` - The learned Q-values
  - `training_stats.json` - Episode statistics
- Displays training progress every 50 episodes

### 3. AI Test Mode
- Watch the trained AI play
- Requires trained model from mode 2
- Press ESC to quit

## RL Concepts Used

### Q-Learning (TD Learning)
- **Temporal Difference Learning**: Updates Q-values based on observed rewards
- **State Space**: (obstacle_type, distance, on_ground, y_position)
  - obstacle_type: 0=none, 1=pit, 2=block
  - distance: 0=very close, 1=close, 2=medium, 3=far
  - on_ground: 0=in air, 1=on ground
  - y_position: discretized vertical position
- **Action Space**: 0=none, 1=left, 2=right, 3=jump
- **Reward Function**:
  - +200: Reach goal
  - -100: Fall in pit
  - -50: Hit block
  - +0.1: Move forward
  - -0.01: Per step penalty (encourages efficiency)

### MDP Formulation
The game is formulated as a Markov Decision Process:
- **States (S)**: Discretized game states
- **Actions (A)**: Movement commands
- **Transitions (P)**: Deterministic physics
- **Rewards (R)**: Immediate feedback
- **Policy (π)**: Learned through Q-Learning

### Algorithm Details
- **Update Rule**: Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
- **Exploration**: ε-greedy (starts at 1.0, decays to 0.01)
- **Learning Rate (α)**: 0.1
- **Discount Factor (γ)**: 0.95

## Configuration

Edit `config.py` to adjust:
- Game physics (gravity, jump force, speed)
- Screen size and FPS
- AI hyperparameters (learning rate, epsilon, discount factor)
- Colors and visual settings

## Training Tips

1. **Start with 1000 episodes** for initial training
2. **Monitor success rate** - should improve over time
3. **For better results**, train for 2000-5000 episodes
4. **Epsilon decay** ensures exploration → exploitation transition
5. **Q-table size** indicates state space coverage

## Example Training Output

```
Episode   Steps     Reward         Epsilon     Success Rate   
----------------------------------------------------------------------
50        157       -15.67         0.7784      0.00%          
100       243       -24.37         0.6058      2.00%          
150       189       45.23          0.4715      8.67%          
200       124       189.56         0.3670      24.00%         
```

## Troubleshooting

**AI not improving?**
- Increase training episodes
- Adjust learning rate in `config.py`
- Check that obstacles aren't too difficult

**Game too easy/hard?**
- Modify obstacle generation in `game.py`
- Adjust physics parameters in `config.py`

**Want to reset training?**
- Delete `q_table.json` and retrain

## Future Enhancements

Potential additions:
- **A* Search**: For pathfinding visualization
- **Policy Iteration**: Alternative RL approach
- **Value Iteration**: Model-based learning
- **Multiple levels**: Curriculum learning
- **Neural network**: Deep Q-Learning (DQN)

## License

Free to use for educational purposes.