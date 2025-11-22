import pygame
import sys
from mario_env import MarioGame
from mario_agent import QLearningAgent
import json

def main():
    print("=" * 70)
    print("MARIO RL - EASY COIN COLLECTION ADVENTURE")
    print("=" * 70)
    print("\n Objective:")
    print("  • Collect as many coins as possible")
    print("  • Navigate through easy, well-spaced obstacles")
    print("  • Reach the goal and maximize your score!")
    print("\n Features:")
    print("  • Longer level with ~150 coins")
    print("  • Easy obstacles with good spacing")
    print("  • Player-friendly physics (better jump & speed)")
    print("  • More time to complete (1200 steps)")
    print("\n" + "=" * 70)
    print("\nSelect Mode:")
    print("1. Human Play Mode")
    print("2. AI Train Mode")
    print("3. AI Test Mode")
    print("=" * 70)
    
    mode = input("Enter mode (1/2/3): ").strip()
    
    pygame.init()
    game = MarioGame()
    
    if mode == "1":
        # Human play mode
        print("\n" + "="*70)
        print("HUMAN PLAY MODE")
        print("="*70)
        print("\n Controls:")
        print("  LEFT/RIGHT arrows: Move")
        print("  SPACE: Jump")
        print("  RIGHT+SPACE: Jump while moving right (recommended!)")
        print("  ESC: Quit")
        print("\n Tips:")
        print("  • Collect ALL coins for a PERFECT bonus!")
        print("  • Faster completion = Higher score!")
        print("  • Avoid obstacles to keep your run going")
        print("  • Your best time will be tracked")
        print("\n" + "="*70)
        input("Press ENTER to start...")
        game.run_human()
        
    elif mode == "2":
        # AI training mode
        episodes = int(input("\nEnter number of training episodes (default 3000): ") or "3000")
        
        agent = QLearningAgent()
        
        print(f"\n{'='*70}")
        print(f"TRAINING AI AGENT")
        print(f"{'='*70}")
        print(f"\n Training for {episodes} episodes...")
        print(" The AI will learn to:")
        print("  • Navigate obstacles efficiently")
        print("  • Collect coins strategically")
        print("  • Optimize completion time")
        print(f"\n{'='*70}\n")
        
        training_stats = agent.train(game, episodes)
        
        # Save training data
        agent.save_q_table("q_table.json")
        with open("training_stats.json", "w") as f:
            json.dump(training_stats, f, indent=2)
        
        print("\n" + "="*70)
        print(" TRAINING SUMMARY")
        print("="*70)
        agent.print_policy_sample(15)
        
        print(f"\n Files saved:")
        print(f"  • q_table.json - Trained Q-table")
        print(f"  • training_stats.json - Training statistics")
        print("="*70)
        
    elif mode == "3":
        # AI test mode
        try:
            agent = QLearningAgent()
            agent.load_q_table("q_table.json")
            
            print("\n" + "="*70)
            print("AI TEST MODE")
            print("="*70)
            print("\n Loaded trained model")
            print("\n Watch the AI play!")
            print(" Performance will be shown in console")
            print("\nControls:")
            print("  R: Reset")
            print("  ESC: Quit")
            print("\n" + "="*70)
            
            agent.print_policy_sample(5)
            print("\n" + "="*70)
            print("Starting AI playback...\n")
            
            game.run_ai(agent)
            
        except FileNotFoundError:
            print("\n Error: No trained model found!")
            print("Please run training mode first (option 2)")
            print("\nTo train: python main.py -> Select 2")
    else:
        print("Invalid mode selected!")
    
    pygame.quit()

if __name__ == "__main__":
    main()