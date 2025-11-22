import random
import json
from collections import defaultdict
from mario_config import *

class QLearningAgent:
    """Q-Learning agent optimized for coin collection and speed"""
    
    def __init__(self):
        self.q_table = defaultdict(lambda: [0.0] * NUM_ACTIONS)
        self.epsilon = EPSILON_START
        self.learning_rate = LEARNING_RATE
        self.discount_factor = DISCOUNT_FACTOR
        self.action_counts = defaultdict(lambda: [0] * NUM_ACTIONS)
    
    def get_action(self, state, explore=True):
        """Select action using epsilon-greedy policy"""
        if explore and random.random() < self.epsilon:
            # Smart exploration: prefer forward and jump actions
            rand = random.random()
            if rand < 0.35:
                return 2  # RIGHT
            elif rand < 0.55:
                return 4  # RIGHT+JUMP
            elif rand < 0.75:
                return 3  # JUMP
            else:
                return random.randint(0, NUM_ACTIONS - 1)
        else:
            q_values = self.q_table[state]
            max_q = max(q_values)
            best_actions = [i for i, q in enumerate(q_values) if q == max_q]
            action = random.choice(best_actions)
            self.action_counts[state][action] += 1
            return action
    
    def update_q_value(self, state, action, reward, next_state, done):
        """Update Q-value using TD learning"""
        current_q = self.q_table[state][action]
        
        if done:
            target_q = reward
        else:
            max_next_q = max(self.q_table[next_state])
            target_q = reward + self.discount_factor * max_next_q
        
        self.q_table[state][action] = current_q + self.learning_rate * (target_q - current_q)
    
    def decay_epsilon(self):
        """Decay exploration rate"""
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)
    
    def train(self, game, episodes):
        """Train the agent"""
        stats = {
            'episode_rewards': [],
            'episode_steps': [],
            'episode_scores': [],
            'episode_times': [],
            'coins_collected': [],
            'coin_percentages': [],
            'success_rate': [],
            'epsilon_values': [],
            'perfect_runs': 0
        }
        
        wins = 0
        perfect_runs = 0
        
        print(f"{'Episode':<10}{'Result':<8}{'Time':<10}{'Score':<10}{'Coins':<15}{'Epsilon':<12}{'Win Rate':<12}")
        print("-" * 90)
        
        for episode in range(episodes):
            state = game.reset()
            total_reward = 0
            steps = 0
            
            while True:
                action = self.get_action(state, explore=True)
                next_state, reward, done = game.step(action)
                
                self.update_q_value(state, action, reward, next_state, done)
                
                total_reward += reward
                steps += 1
                state = next_state
                
                if done:
                    break
            
            if game.win:
                wins += 1
                if game.coins_collected == game.total_coins:
                    perfect_runs += 1
            
            self.decay_epsilon()
            
            # Record statistics
            stats['episode_rewards'].append(total_reward)
            stats['episode_steps'].append(steps)
            stats['episode_scores'].append(game.score)
            stats['episode_times'].append(game.time_taken)
            stats['coins_collected'].append(game.coins_collected)
            coin_pct = (game.coins_collected / game.total_coins * 100) if game.total_coins > 0 else 0
            stats['coin_percentages'].append(coin_pct)
            stats['epsilon_values'].append(self.epsilon)
            
            # Calculate win rate
            if episode >= 99:
                recent_wins = sum(1 for i in range(episode - 99, episode + 1) 
                                if game.score > 0 and stats['episode_steps'][i] < MAX_STEPS)
                win_rate = recent_wins / 100
            else:
                win_rate = wins / (episode + 1)
            
            stats['success_rate'].append(win_rate)
            
            # Print progress every 50 episodes
            if (episode + 1) % 50 == 0:
                avg_time = sum(stats['episode_times'][max(0, episode-49):episode+1]) / min(50, episode+1)
                avg_score = sum(stats['episode_scores'][max(0, episode-49):episode+1]) / min(50, episode+1)
                avg_coins = sum(stats['coins_collected'][max(0, episode-49):episode+1]) / min(50, episode+1)
                avg_coin_pct = sum(stats['coin_percentages'][max(0, episode-49):episode+1]) / min(50, episode+1)
                
                result = f"{wins}/{episode+1}"
                coin_str = f"{avg_coins:.1f}/{game.total_coins} ({avg_coin_pct:.0f}%)"
                
                print(f"{episode+1:<10}{result:<8}{avg_time:<10.1f}{int(avg_score):<10}{coin_str:<15}{self.epsilon:<12.4f}{win_rate:<12.2%}")
        
        # Calculate final statistics
        final_win_rate = sum(1 for i in range(max(0, episodes - 100), episodes) 
                            if stats['episode_scores'][i] > 0) / min(100, episodes)
        
        avg_final_score = sum(stats['episode_scores'][max(0, episodes-100):]) / min(100, episodes)
        avg_final_coins = sum(stats['coins_collected'][max(0, episodes-100):]) / min(100, episodes)
        avg_final_coin_pct = sum(stats['coin_percentages'][max(0, episodes-100):]) / min(100, episodes)
        avg_final_time = sum(stats['episode_times'][max(0, episodes-100):]) / min(100, episodes)
        
        stats['final_win_rate'] = final_win_rate
        stats['avg_final_score'] = avg_final_score
        stats['avg_final_coins'] = avg_final_coins
        stats['avg_final_coin_pct'] = avg_final_coin_pct
        stats['avg_final_time'] = avg_final_time
        stats['perfect_runs'] = perfect_runs
        stats['total_episodes'] = episodes
        stats['q_table_size'] = len(self.q_table)
        
        print("\n" + "="*90)
        print(" TRAINING COMPLETE!")
        print("="*90)
        print(f"Performance (last 100 episodes):")
        print(f"   • Win Rate: {final_win_rate:.2%}")
        print(f"   • Avg Score: {int(avg_final_score)}")
        print(f"   • Avg Coins: {avg_final_coins:.1f}/{game.total_coins} ({avg_final_coin_pct:.1f}%)")
        print(f"   • Avg Time: {avg_final_time:.1f}s")
        print(f"   • Perfect Runs: {perfect_runs}")
        print(f"\n Q-table size: {len(self.q_table)} states")
        print(f" Final epsilon: {self.epsilon:.4f}")
        print("="*90)
        
        return stats
    
    def save_q_table(self, filename):
        """Save Q-table to file"""
        q_dict = {str(k): v for k, v in self.q_table.items()}
        action_dict = {str(k): v for k, v in self.action_counts.items()}
        data = {
            'q_table': q_dict,
            'action_counts': action_dict,
            'epsilon': self.epsilon
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f" Q-table saved: {filename} ({len(q_dict)} states)")
    
    def load_q_table(self, filename):
        """Load Q-table from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.q_table = defaultdict(lambda: [0.0] * NUM_ACTIONS)
        for k, v in data['q_table'].items():
            state = eval(k)
            self.q_table[state] = v
        
        if 'action_counts' in data:
            self.action_counts = defaultdict(lambda: [0] * NUM_ACTIONS)
            for k, v in data['action_counts'].items():
                state = eval(k)
                self.action_counts[state] = v
        
        self.epsilon = data.get('epsilon', EPSILON_MIN)
        print(f" Loaded Q-table: {len(self.q_table)} states (epsilon: {self.epsilon:.4f})")
    
    def print_policy_sample(self, num_states=10):
        """Print sample of learned policy"""
        if len(self.q_table) == 0:
            print("\n  No policy learned yet (Q-table is empty)")
            return
            
        print(f"\n Top {num_states} Learned Strategies:")
        print("-" * 100)
        print(f"{'State Description':<60} | {'Best Action':<20} | {'Q-value':<10}")
        print("-" * 100)
        
        sorted_states = sorted(self.q_table.items(), 
                              key=lambda x: max(x[1]), reverse=True)[:num_states]
        
        for state, q_values in sorted_states:
            best_action = q_values.index(max(q_values))
            best_q = max(q_values)
            
            # Parse state for better readability
            obs_type_map = {0: 'None', 1: 'Pit', 2: 'Block', 3: 'Spike', 4: 'Enemy'}
            dist_map = {0: 'VeryClose', 1: 'Close', 2: 'Medium', 3: 'MedFar', 4: 'Far', 5: 'VeryFar', 8: 'None'}
            jump_map = {0: 'Ground', 1: 'Rising', 2: 'Peak', 3: 'Falling'}
            coin_dist_map = {0: 'Nearby', 1: 'Close', 2: 'MedFar', 8: 'None'}
            coin_height_map = {0: 'Low', 1: 'Mid', 2: 'High'}
            
            # state = (obstacle_type, distance_bucket, jump_state, over_pit, nearest_coin_dist, nearest_coin_height)
            state_desc = (f"Obs:{obs_type_map.get(state[0], '?'):<6} Dist:{dist_map.get(state[1], '?'):<8} "
                         f"Jump:{jump_map.get(state[2], '?'):<7} Pit:{state[3]} "
                         f"Coin:{coin_dist_map.get(state[4], '?'):<6}@{coin_height_map.get(state[5], '?')}")
            
            print(f"{state_desc:<60} | {ACTIONS[best_action]:<20} | {best_q:<10.2f}")
        
        print("-" * 100)