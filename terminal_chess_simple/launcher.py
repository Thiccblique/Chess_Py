#!/usr/bin/env python3
"""
Chess Game Launcher - Choose between Terminal and Pygame versions
"""

import sys
import os

def show_menu():
    """Display version selection menu"""
    print("=" * 50)
    print("🎮 CHESS GAME LAUNCHER 🎮")
    print("=" * 50)
    print()
    print("Choose your chess experience:")
    print()
    print("1. 📟 Terminal Chess (Text-based)")
    print("   ├─ Color-coded pieces (Red/Blue)")
    print("   ├─ Green move highlighting") 
    print("   ├─ Piece selection by letter")
    print("   └─ Works in any terminal")
    print()
    print("2. 🖼️  Pygame Chess (Original)")
    print("   ├─ Visual chess board")
    print("   ├─ Click to select and move")
    print("   ├─ Smooth highlighting")
    print("   └─ Professional appearance")
    print()
    print("3. 🏗️  Pygame Chess (Clean Architecture)")
    print("   ├─ Organized like Unity C#")
    print("   ├─ Separate systems and managers")
    print("   ├─ Easy to read and modify")
    print("   └─ Professional code structure")
    print()
    print("4. ❌ Exit")
    print()

def get_choice():
    """Get user's choice with validation"""
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return int(choice)
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            return 4

def launch_terminal_chess():
    """Launch the terminal version"""
    print("\n🚀 Launching Terminal Chess...")
    print("=" * 30)
    try:
        # Import and run the terminal version
        import main
        main.main()
    except ImportError:
        print("❌ Error: main.py not found!")
        input("Press Enter to return to menu...")
    except Exception as e:
        print(f"❌ Error launching terminal chess: {e}")
        input("Press Enter to return to menu...")

def launch_pygame_chess():
    """Launch the pygame version"""
    print("\n🚀 Launching Pygame Chess...")
    print("=" * 30)
    try:
        # Check if pygame is available
        import pygame
        
        # Import and run the pygame version
        from chess_pygame import chess_pygame_original
        chess_pygame_original.main()
        
    except ImportError as e:
        if 'pygame' in str(e):
            print("❌ Error: Pygame not installed!")
            print("To install pygame, run: pip install pygame")
        else:
            print(f"❌ Error: chess_pygame files not found!")
        input("Press Enter to return to menu...")
    except Exception as e:
        print(f"❌ Error launching pygame chess: {e}")
        input("Press Enter to return to menu...")

def launch_clean_architecture_chess():
    """Launch the clean architecture pygame version"""
    print("\n🚀 Launching Clean Architecture Chess...")
    print("=" * 40)
    try:
        # Check if pygame is available
        import pygame
        
        # Import and run the clean architecture version
        from chess_pygame import chess_game_runner
        chess_game_runner.main()
        
    except ImportError as e:
        if 'pygame' in str(e):
            print("❌ Error: Pygame not installed!")
            print("To install pygame, run: pip install pygame")
        else:
            print(f"❌ Error: Clean architecture files not found!")
            print("Make sure all chess_pygame/*.py files are present.")
        input("Press Enter to return to menu...")
    except Exception as e:
        print(f"❌ Error launching clean architecture chess: {e}")
        input("Press Enter to return to menu...")

def main():
    """Main launcher loop"""
    while True:
        # Clear screen (works on Windows and Unix)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        show_menu()
        choice = get_choice()
        
        if choice == 1:
            launch_terminal_chess()
        elif choice == 2:
            launch_pygame_chess()
        elif choice == 3:
            launch_clean_architecture_chess()
        elif choice == 4:
            print("\n👋 Thanks for playing chess!")
            sys.exit(0)

if __name__ == "__main__":
    main()