import pygame
import random
from mario_config import *

class MarioGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mario RL - Coin Collection Challenge")
        self.clock = pygame.time.Clock()
        self.camera_x = 0
        self.best_time = float('inf')
        self.best_score = 0
        self.reset()
    
    def reset(self):
        """Reset game state"""
        self.player_x = 100
        self.player_y = GROUND_Y - PLAYER_SIZE
        self.player_vy = 0
        self.is_jumping = False
        self.game_over = False
        self.win = False
        self.score = 0
        self.coins_collected = 0
        self.total_coins = 0
        self.steps = 0
        self.time_taken = 0
        self.max_x = 100
        
        # Generate enhanced level with more obstacles
        self.obstacles, self.coins = self._generate_enhanced_level()
        self.total_coins = len(self.coins)
        
        return self._get_state()
    
    def _generate_enhanced_level(self):
        """Generate enhanced level with all obstacle types and better coin placement"""
        obstacles = []
        coins = []
        x = 300
        
        # Shorter, more focused pattern sequence - easier to complete
        patterns = [
            'coin_trail', 'easy_pit', 'coin_trail', 'single_block', 
            'safe_space', 'pit_coins', 'coin_arc', 'spike_coins', 
            'safe_space', 'block_coins', 'coin_trail', 'enemy_coins',
            'safe_space', 'easy_pit', 'double_block_coins', 
            'coin_maze', 'safe_space', 'final_coin_rush'
        ]
        
        for pattern in patterns:
            if pattern == 'coin_trail':
                # Simple coin trail on ground
                for i in range(8):
                    coins.append({
                        'x': x + i * 30,
                        'y': GROUND_Y - 40,
                        'collected': False
                    })
                x += 280
                
            elif pattern == 'safe_space':
                # Safe space with just a few coins
                for i in range(3):
                    coins.append({
                        'x': x + i * 40,
                        'y': GROUND_Y - 50,
                        'collected': False
                    })
                x += 180
                
            elif pattern == 'easy_pit':
                # Easy pit that's jumpable
                pit_width = random.choice([60, 70])
                obstacles.append({
                    'type': 'pit',
                    'x': x,
                    'width': pit_width
                })
                # Coins before and after pit
                coins.append({
                    'x': x - 40,
                    'y': GROUND_Y - 60,
                    'collected': False
                })
                coins.append({
                    'x': x + pit_width + 40,
                    'y': GROUND_Y - 60,
                    'collected': False
                })
                x += pit_width + 200
                
            elif pattern == 'pit_coins':
                # Pit with coins above
                pit_width = 70
                obstacles.append({
                    'type': 'pit',
                    'x': x,
                    'width': pit_width
                })
                # Coins above pit at different heights
                for i in range(5):
                    coins.append({
                        'x': x + 10 + i * 15,
                        'y': GROUND_Y - 100 - (i % 2) * 20,
                        'collected': False
                    })
                x += pit_width + 200
                
            elif pattern == 'single_block':
                # Single block obstacle
                block_height = 50
                obstacles.append({
                    'type': 'block',
                    'x': x,
                    'y': GROUND_Y - block_height,
                    'width': 40,
                    'height': block_height
                })
                # Coin on top of block
                coins.append({
                    'x': x + 20,
                    'y': GROUND_Y - block_height - 40,
                    'collected': False
                })
                x += 200
                
            elif pattern == 'block_coins':
                # Block with coins on top and around
                block_height = 50
                obstacles.append({
                    'type': 'block',
                    'x': x,
                    'y': GROUND_Y - block_height,
                    'width': 40,
                    'height': block_height
                })
                # Coin on top of block
                coins.append({
                    'x': x + 20,
                    'y': GROUND_Y - block_height - 40,
                    'collected': False
                })
                # Coins before and after block
                coins.append({
                    'x': x - 40,
                    'y': GROUND_Y - 60,
                    'collected': False
                })
                coins.append({
                    'x': x + 80,
                    'y': GROUND_Y - 60,
                    'collected': False
                })
                x += 250
                
            elif pattern == 'coin_arc':
                # Arc of coins (rainbow shape)
                for i in range(9):
                    height = 50 + abs(4 - i) * 20
                    coins.append({
                        'x': x + i * 30,
                        'y': GROUND_Y - height,
                        'collected': False
                    })
                x += 300
                
            elif pattern == 'spike_coins':
                # Spike with coins requiring jump
                obstacles.append({
                    'type': 'spike',
                    'x': x,
                    'y': GROUND_Y - 50,
                    'width': 40,
                    'height': 50
                })
                # High coins above spike
                for i in range(3):
                    coins.append({
                        'x': x - 30 + i * 30,
                        'y': GROUND_Y - 120,
                        'collected': False
                    })
                x += 250
                
            elif pattern == 'coin_challenge':
                # High coins in a line (requires multiple jumps)
                for i in range(6):
                    coins.append({
                        'x': x + i * 40,
                        'y': GROUND_Y - 140,
                        'collected': False
                    })
                x += 280
                
            elif pattern == 'enemy_coins':
                # Enemy with coins around it
                obstacles.append({
                    'type': 'enemy',
                    'x': x + 40,
                    'y': GROUND_Y - 30,
                    'radius': 15,
                    'start_x': x + 40,
                    'range': 80
                })
                # Coins that require jumping over enemy
                for i in range(4):
                    coins.append({
                        'x': x - 20 + i * 40,
                        'y': GROUND_Y - 100,
                        'collected': False
                    })
                x += 280
                
            elif pattern == 'block_stairs_coins':
                # Stairs with coins on each step
                for i in range(4):
                    height = 35 + i * 15
                    obstacles.append({
                        'type': 'block',
                        'x': x + i * 60,
                        'y': GROUND_Y - height,
                        'width': 40,
                        'height': height
                    })
                    # Coin on each step
                    coins.append({
                        'x': x + i * 60 + 20,
                        'y': GROUND_Y - height - 35,
                        'collected': False
                    })
                x += 300
                
            elif pattern == 'coin_maze':
                # Zigzag coin pattern
                for i in range(10):
                    height = 60 + (i % 3) * 35
                    coins.append({
                        'x': x + i * 25,
                        'y': GROUND_Y - height,
                        'collected': False
                    })
                x += 280
                
            elif pattern == 'double_block_coins':
                # Two blocks with gap and coins
                for i in range(2):
                    obstacles.append({
                        'type': 'block',
                        'x': x + i * 120,
                        'y': GROUND_Y - 55,
                        'width': 40,
                        'height': 55
                    })
                    # Coin on block
                    coins.append({
                        'x': x + i * 120 + 20,
                        'y': GROUND_Y - 95,
                        'collected': False
                    })
                # Coins in the gap
                for j in range(2):
                    coins.append({
                        'x': x + 60 + j * 20,
                        'y': GROUND_Y - 70,
                        'collected': False
                    })
                x += 280
                
            elif pattern == 'final_coin_rush':
                # Final section with many coins leading to goal
                # Ground coins
                for i in range(12):
                    coins.append({
                        'x': x + i * 25,
                        'y': GROUND_Y - 40,
                        'collected': False
                    })
                # High coins
                for i in range(10):
                    coins.append({
                        'x': x + 30 + i * 30,
                        'y': GROUND_Y - 110,
                        'collected': False
                    })
                x += 400
        
        # Set goal position closer - make it reachable
        self.goal_x = x + 50
        
        print(f"\n🏁 Level generated:")
        print(f"   • Obstacles: {len(obstacles)}")
        print(f"   • Coins: {len(coins)}")
        print(f"   • Goal distance: {self.goal_x} pixels")
        print(f"   • Estimated time needed: ~{self.goal_x / (PLAYER_SPEED * FPS):.1f}s at full speed")
        print()
        
        return obstacles, coins
    
    def _get_state(self):
        """Get detailed state representation for AI"""
        # Find nearest obstacle ahead
        nearest_obstacle = None
        min_dist = float('inf')
        
        for obs in self.obstacles:
            dist = obs['x'] - self.player_x
            if -20 < dist < min_dist:
                min_dist = dist
                nearest_obstacle = obs
        
        # Find nearest uncollected coin
        nearest_coin_dist = 8
        nearest_coin_height = 0
        for coin in self.coins:
            if not coin['collected']:
                coin_dist = coin['x'] - self.player_x
                if -10 < coin_dist < 200:
                    if coin_dist < 50:
                        nearest_coin_dist = 0
                    elif coin_dist < 100:
                        nearest_coin_dist = 1
                    elif coin_dist < 150:
                        nearest_coin_dist = 2
                    
                    # Check coin height
                    coin_y = coin['y']
                    if coin_y < GROUND_Y - 100:
                        nearest_coin_height = 2  # High
                    elif coin_y < GROUND_Y - 60:
                        nearest_coin_height = 1  # Medium
                    else:
                        nearest_coin_height = 0  # Low
                    break
        
        # State representation
        if nearest_obstacle is None:
            obstacle_type = 0
            distance_bucket = 8
            obstacle_width = 0
        else:
            type_map = {'pit': 1, 'block': 2, 'spike': 3, 'enemy': 4}
            obstacle_type = type_map.get(nearest_obstacle['type'], 0)
            
            if min_dist < 30:
                distance_bucket = 0
            elif min_dist < 60:
                distance_bucket = 1
            elif min_dist < 100:
                distance_bucket = 2
            elif min_dist < 150:
                distance_bucket = 3
            elif min_dist < 200:
                distance_bucket = 4
            else:
                distance_bucket = 5
            
            if nearest_obstacle['type'] == 'pit':
                obstacle_width = 1 if nearest_obstacle['width'] > 70 else 0
            elif nearest_obstacle['type'] == 'enemy':
                obstacle_width = 1
            else:
                obstacle_width = 0
        
        if not self.is_jumping:
            jump_state = 0
        elif self.player_vy < -5:
            jump_state = 1
        elif abs(self.player_vy) <= 5:
            jump_state = 2
        else:
            jump_state = 3
        
        over_pit = 0
        for obs in self.obstacles:
            if obs['type'] == 'pit':
                if (self.player_x + PLAYER_SIZE/2 > obs['x'] and 
                    self.player_x + PLAYER_SIZE/2 < obs['x'] + obs['width']):
                    over_pit = 1
                    break
        
        return (obstacle_type, distance_bucket, jump_state, over_pit, nearest_coin_dist, nearest_coin_height)
    
    def step(self, action):
        """Execute action and return (state, reward, done)"""
        self.steps += 1
        self.time_taken = self.steps / FPS
        old_x = self.player_x
        
        # Actions: 0=nothing, 1=left, 2=right, 3=jump, 4=right+jump, 5=left+jump
        if action == 1:
            self.player_x -= PLAYER_SPEED
        elif action == 2:
            self.player_x += PLAYER_SPEED
        elif action == 3:
            if not self.is_jumping:
                self.player_vy = JUMP_FORCE
                self.is_jumping = True
        elif action == 4:
            self.player_x += PLAYER_SPEED
            if not self.is_jumping:
                self.player_vy = JUMP_FORCE
                self.is_jumping = True
        elif action == 5:
            self.player_x -= PLAYER_SPEED
            if not self.is_jumping:
                self.player_vy = JUMP_FORCE
                self.is_jumping = True
        
        # Apply gravity
        self.player_vy += GRAVITY
        self.player_y += self.player_vy
        
        # Ground collision
        if self.player_y >= GROUND_Y - PLAYER_SIZE:
            self.player_y = GROUND_Y - PLAYER_SIZE
            self.player_vy = 0
            self.is_jumping = False
        
        if self.player_x < 0:
            self.player_x = 0
        
        # Update camera
        self.camera_x = max(0, self.player_x - SCREEN_WIDTH // 3)
        
        reward = 0
        done = False
        
        # Check coin collection
        for coin in self.coins:
            if not coin['collected']:
                coin_dist = ((self.player_x + PLAYER_SIZE/2 - coin['x'])**2 + 
                           (self.player_y + PLAYER_SIZE/2 - coin['y'])**2)**0.5
                if coin_dist < PLAYER_SIZE/2 + COIN_RADIUS:
                    coin['collected'] = True
                    self.coins_collected += 1
                    self.score += COIN_VALUE
                    reward += COIN_COLLECT_REWARD
        
        # Reward for forward progress
        if self.player_x > self.max_x:
            reward += (self.player_x - self.max_x) * 0.3
            self.max_x = self.player_x
        
        # Check collisions with obstacles
        for obs in self.obstacles:
            if obs['type'] == 'pit':
                if (self.player_x + PLAYER_SIZE > obs['x'] and 
                    self.player_x < obs['x'] + obs['width']):
                    if self.player_y + PLAYER_SIZE >= GROUND_Y - 2:
                        self.game_over = True
                        reward = -100
                        done = True
                    elif self.player_y < GROUND_Y - PLAYER_SIZE - 10:
                        reward += 1
                        
            elif obs['type'] == 'block':
                if (self.player_x + PLAYER_SIZE > obs['x'] + 5 and 
                    self.player_x < obs['x'] + obs['width'] - 5 and
                    self.player_y + PLAYER_SIZE > obs['y'] + 5):
                    self.game_over = True
                    reward = -50
                    done = True
                    
            elif obs['type'] == 'spike':
                if (self.player_x + PLAYER_SIZE > obs['x'] and 
                    self.player_x < obs['x'] + obs['width'] and
                    self.player_y + PLAYER_SIZE > obs['y']):
                    self.game_over = True
                    reward = -60
                    done = True
                    
            elif obs['type'] == 'enemy':
                enemy_x = obs['x']
                enemy_y = obs['y']
                dist = ((self.player_x + PLAYER_SIZE/2 - enemy_x)**2 + 
                       (self.player_y + PLAYER_SIZE/2 - enemy_y)**2)**0.5
                if dist < PLAYER_SIZE/2 + obs['radius']:
                    self.game_over = True
                    reward = -50
                    done = True
        
        # Win condition
        if self.player_x >= self.goal_x:
            self.win = True
            # Calculate final score with bonuses
            coin_bonus = self.coins_collected * 5
            time_bonus = max(0, 500 - self.steps) * 0.1
            completion_bonus = 200
            
            # Perfect bonus
            coin_percentage = (self.coins_collected / self.total_coins) * 100
            if coin_percentage == 100:
                perfect_bonus = 100
            else:
                perfect_bonus = 0
            
            reward = completion_bonus + coin_bonus + time_bonus + perfect_bonus
            done = True
            
            # Update records
            if self.time_taken < self.best_time:
                self.best_time = self.time_taken
            if self.score > self.best_score:
                self.best_score = self.score
        
        # Small step penalty
        reward -= 0.02
        
        # Penalty for going backwards
        if self.player_x < old_x:
            reward -= 0.2
        
        # Timeout penalty
        if self.steps > MAX_STEPS:
            done = True
            reward = -30
        
        return self._get_state(), reward, done
    
    def render(self):
        """Render the game"""
        self.screen.fill(SKY_COLOR)
        
        # Draw clouds
        for i in range(5):
            cloud_x = (i * 300 - int(self.camera_x * 0.5)) % (SCREEN_WIDTH + 200)
            self._draw_cloud(cloud_x, 50 + i * 30)
        
        # Draw ground
        ground_rect = pygame.Rect(0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
        pygame.draw.rect(self.screen, GROUND_COLOR, ground_rect)
        
        for i in range(0, SCREEN_WIDTH, 20):
            grass_x = i - (int(self.camera_x) % 20)
            pygame.draw.line(self.screen, (50, 150, 50), 
                           (grass_x, GROUND_Y), (grass_x, GROUND_Y - 8), 2)
        
        # Draw coins
        for coin in self.coins:
            if not coin['collected']:
                screen_x = coin['x'] - self.camera_x
                if -50 < screen_x < SCREEN_WIDTH + 50:
                    self._draw_coin(screen_x, coin['y'])
        
        # Draw obstacles
        for obs in self.obstacles:
            screen_x = obs['x'] - self.camera_x
            
            if obs['type'] == 'pit':
                pit_rect = pygame.Rect(screen_x, GROUND_Y, obs['width'], SCREEN_HEIGHT - GROUND_Y)
                pygame.draw.rect(self.screen, PIT_COLOR, pit_rect)
                for i in range(0, obs['width'], 10):
                    pygame.draw.line(self.screen, (50, 50, 50),
                                   (screen_x + i, GROUND_Y),
                                   (screen_x + i + 5, GROUND_Y + 10), 2)
                    
            elif obs['type'] == 'block':
                self._draw_brick_block(screen_x, obs['y'], obs['width'], obs['height'])
                
            elif obs['type'] == 'spike':
                self._draw_spike(screen_x, obs['y'], obs['width'], obs['height'])
                
            elif obs['type'] == 'enemy':
                self._draw_enemy(screen_x, obs['y'], obs['radius'])
        
        # Draw goal - make it more visible
        goal_screen_x = self.goal_x - self.camera_x
        if -100 < goal_screen_x < SCREEN_WIDTH + 100:
            self._draw_flag(goal_screen_x, GROUND_Y - 80)
            # Add goal zone indicator
            goal_zone = pygame.Rect(goal_screen_x - 30, GROUND_Y - 100, 60, 100)
            pygame.draw.rect(self.screen, (255, 215, 0, 100), goal_zone, 3)
        
        # Draw player
        player_screen_x = self.player_x - self.camera_x
        self._draw_player(player_screen_x, self.player_y)
        
        # Draw UI
        font = pygame.font.Font(None, 32)
        
        # Score and coins
        coin_pct = (self.coins_collected * 100 // self.total_coins) if self.total_coins > 0 else 0
        score_text = font.render(f"Score: {self.score} | Coins: {self.coins_collected}/{self.total_coins} ({coin_pct}%)", 
                                True, (255, 255, 255))
        score_shadow = font.render(f"Score: {self.score} | Coins: {self.coins_collected}/{self.total_coins} ({coin_pct}%)", 
                                  True, (0, 0, 0))
        self.screen.blit(score_shadow, (12, 12))
        self.screen.blit(score_text, (10, 10))
        
        # Time
        best_time_str = f"{self.best_time:.1f}" if self.best_time != float('inf') else "--"
        time_text = font.render(f"Time: {self.time_taken:.1f}s | Best: {best_time_str}s", 
                               True, (255, 255, 255))
        time_shadow = font.render(f"Time: {self.time_taken:.1f}s | Best: {best_time_str}s", 
                                 True, (0, 0, 0))
        self.screen.blit(time_shadow, (12, 42))
        self.screen.blit(time_text, (10, 40))
        
        # Distance
        dist_text = font.render(f"Distance: {int(self.max_x)}/{int(self.goal_x)}", 
                               True, (255, 255, 255))
        dist_shadow = font.render(f"Distance: {int(self.max_x)}/{int(self.goal_x)}", 
                                 True, (0, 0, 0))
        self.screen.blit(dist_shadow, (12, 72))
        self.screen.blit(dist_text, (10, 70))
        
        if self.game_over:
            self._draw_game_over()
        elif self.win:
            self._draw_victory()
        
        pygame.display.flip()
    
    def _draw_coin(self, x, y):
        """Draw a coin with shine effect"""
        pygame.draw.circle(self.screen, COIN_COLOR, (int(x), int(y)), COIN_RADIUS)
        pygame.draw.circle(self.screen, (255, 240, 100), (int(x), int(y)), COIN_RADIUS - 3)
        pygame.draw.circle(self.screen, COIN_COLOR, (int(x), int(y)), 3)
        pygame.draw.circle(self.screen, (255, 255, 200), (int(x - 3), int(y - 3)), 2)
    
    def _draw_cloud(self, x, y):
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), 20)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x + 25), int(y)), 25)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x + 50), int(y)), 20)
    
    def _draw_brick_block(self, x, y, width, height):
        pygame.draw.rect(self.screen, BLOCK_COLOR, (x, y, width, height))
        pygame.draw.rect(self.screen, BLOCK_SHADOW, (x, y + height - 5, width, 5))
        for i in range(0, height, 10):
            pygame.draw.line(self.screen, BLOCK_SHADOW, (x, y + i), (x + width, y + i), 1)
        pygame.draw.line(self.screen, BLOCK_SHADOW, (x + width//2, y), (x + width//2, y + height), 1)
    
    def _draw_spike(self, x, y, width, height):
        num_spikes = max(1, width // 20)
        spike_width = width // num_spikes
        for i in range(num_spikes):
            spike_x = x + i * spike_width
            points = [
                (spike_x, y + height),
                (spike_x + spike_width // 2, y),
                (spike_x + spike_width, y + height)
            ]
            pygame.draw.polygon(self.screen, (80, 80, 80), points)
            pygame.draw.polygon(self.screen, (50, 50, 50), points, 2)
    
    def _draw_enemy(self, x, y, radius):
        pygame.draw.circle(self.screen, ENEMY_COLOR, (int(x), int(y)), radius)
        eye_offset = radius // 3
        pygame.draw.circle(self.screen, (255, 255, 255), 
                          (int(x - eye_offset), int(y - eye_offset)), radius // 4)
        pygame.draw.circle(self.screen, (255, 255, 255), 
                          (int(x + eye_offset), int(y - eye_offset)), radius // 4)
        pygame.draw.circle(self.screen, (0, 0, 0), 
                          (int(x - eye_offset), int(y - eye_offset)), radius // 6)
        pygame.draw.circle(self.screen, (0, 0, 0), 
                          (int(x + eye_offset), int(y - eye_offset)), radius // 6)
    
    def _draw_player(self, x, y):
        pygame.draw.rect(self.screen, PLAYER_COLOR, (x, y, PLAYER_SIZE, PLAYER_SIZE))
        pygame.draw.rect(self.screen, (200, 0, 0), (x, y, PLAYER_SIZE, 8))
        pygame.draw.rect(self.screen, (255, 200, 150), (x + 5, y + 8, PLAYER_SIZE - 10, 15))
        pygame.draw.circle(self.screen, (0, 0, 0), (int(x + 10), int(y + 15)), 2)
        pygame.draw.circle(self.screen, (0, 0, 0), (int(x + 20), int(y + 15)), 2)
        pygame.draw.rect(self.screen, (200, 0, 0), (x, y, PLAYER_SIZE, PLAYER_SIZE), 2)
    
    def _draw_flag(self, x, y):
        pygame.draw.rect(self.screen, (100, 50, 0), (x + 5, y, 4, 80))
        points = [(x + 9, y), (x + 45, y + 15), (x + 9, y + 30)]
        pygame.draw.polygon(self.screen, GOAL_COLOR, points)
        pygame.draw.polygon(self.screen, (200, 150, 0), points, 2)
    
    def _draw_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER!", True, (255, 50, 50))
        shadow = font.render("GAME OVER!", True, (0, 0, 0))
        self.screen.blit(shadow, (SCREEN_WIDTH//2 - 148, SCREEN_HEIGHT//2 - 2))
        self.screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
    
    def _draw_victory(self):
        font = pygame.font.Font(None, 72)
        
        if self.coins_collected == self.total_coins:
            text = font.render("PERFECT!", True, (255, 215, 0))
            shadow = font.render("PERFECT!", True, (0, 0, 0))
        else:
            text = font.render("GOAL REACHED!", True, (50, 255, 50))
            shadow = font.render("GOAL REACHED!", True, (0, 0, 0))
        
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH//2 + 2, SCREEN_HEIGHT//2 - 58))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text, text_rect)
        
        small_font = pygame.font.Font(None, 36)
        
        score_text = small_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        score_shadow = small_font.render(f"Final Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_shadow, (SCREEN_WIDTH//2 - 98, SCREEN_HEIGHT//2 + 2))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        
        coin_pct = (self.coins_collected * 100) // self.total_coins
        coins_text = small_font.render(f"Coins: {self.coins_collected}/{self.total_coins} ({coin_pct}%)", 
                                      True, (255, 215, 0))
        coins_shadow = small_font.render(f"Coins: {self.coins_collected}/{self.total_coins} ({coin_pct}%)", 
                                        True, (0, 0, 0))
        self.screen.blit(coins_shadow, (SCREEN_WIDTH//2 - 108, SCREEN_HEIGHT//2 + 42))
        self.screen.blit(coins_text, (SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2 + 40))
        
        time_text = small_font.render(f"Time: {self.time_taken:.1f}s", True, (150, 255, 150))
        time_shadow = small_font.render(f"Time: {self.time_taken:.1f}s", True, (0, 0, 0))
        self.screen.blit(time_shadow, (SCREEN_WIDTH//2 - 68, SCREEN_HEIGHT//2 + 82))
        self.screen.blit(time_text, (SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT//2 + 80))
        
        if self.time_taken == self.best_time and self.best_time != float('inf'):
            best_font = pygame.font.Font(None, 28)
            best_text = best_font.render("NEW RECORD!", True, (255, 100, 100))
            best_shadow = best_font.render("NEW RECORD!", True, (0, 0, 0))
            self.screen.blit(best_shadow, (SCREEN_WIDTH//2 - 72, SCREEN_HEIGHT//2 + 122))
            self.screen.blit(best_text, (SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT//2 + 120))
    
    def run_human(self):
        """Human play mode"""
        self.reset()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            keys = pygame.key.get_pressed()
            action = 0
            
            if keys[pygame.K_RIGHT] and keys[pygame.K_SPACE]:
                action = 4
            elif keys[pygame.K_LEFT] and keys[pygame.K_SPACE]:
                action = 5
            elif keys[pygame.K_LEFT]:
                action = 1
            elif keys[pygame.K_RIGHT]:
                action = 2
            elif keys[pygame.K_SPACE]:
                action = 3
            
            _, _, done = self.step(action)
            self.render()
            
            if done:
                pygame.time.wait(3000)
                self.reset()
            
            self.clock.tick(FPS)
    
    def run_ai(self, agent):
        """AI test mode with visualization"""
        self.reset()
        running = True
        episode = 0
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_r:
                        self.reset()
            
            state = self._get_state()
            action = agent.get_action(state, explore=False)
            _, _, done = self.step(action)
            self.render()
            
            if done:
                episode += 1
                result = 'WIN' if self.win else 'LOSE'
                coin_pct = (self.coins_collected * 100) // self.total_coins if self.total_coins > 0 else 0
                print(f"Episode {episode}: {result:4} | Time: {self.time_taken:6.1f}s | Score: {self.score:4} | Coins: {self.coins_collected}/{self.total_coins} ({coin_pct}%)")
                pygame.time.wait(2000)
                self.reset()
            
            self.clock.tick(FPS)