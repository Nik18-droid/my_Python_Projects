#!/usr/bin/env python3
"""
PING PONG GAMES DEMONSTRATION
============================

This script demonstrates both versions of the Ping Pong game:
1. Advanced version with pygame (full graphics)
2. Simple version for beginners (text-based)
"""

import os
import sys


def show_menu():
    """Display the main menu"""
    print("=" * 60)
    print("           PING PONG GAMES COLLECTION")
    print("=" * 60)
    print()
    print("Choose which version to play:")
    print()
    print("1. 🎮 ADVANCED PING PONG (pygame)")
    print("   - Full graphics and animations")
    print("   - Sound effects support")
    print("   - Multiple difficulty levels")
    print("   - Professional game feel")
    print("   - Requires: pygame library")
    print()
    print("2. 📚 SIMPLE PING PONG (beginner-friendly)")
    print("   - Text-based graphics")
    print("   - Educational comments")
    print("   - Fundamental concepts")
    print("   - Runs in terminal")
    print("   - No external dependencies")
    print()
    print("3. 📖 View Beginner's Guide")
    print("4. ❌ Exit")
    print()


def check_pygame():
    """Check if pygame is installed"""
    try:
        import pygame
        return True
    except ImportError:
        return False


def run_advanced_game():
    """Run the advanced pygame version"""
    if not check_pygame():
        print("❌ pygame is not installed!")
        print("To install pygame, run: pip install pygame")
        print("Then try again.")
        return

    print("🎮 Starting Advanced Ping Pong Game...")
    print("Close the game window to return to this menu.")
    print()

    try:
        os.system("python ping_pong_python.py")
    except Exception as e:
        print(f"Error running advanced game: {e}")


def run_simple_game():
    """Run the simple beginner version"""
    print("📚 Starting Simple Ping Pong Game...")
    print("This version runs in the terminal.")
    print("Press Ctrl+C to return to this menu.")
    print()

    try:
        os.system("python simple_ping_pong.py")
    except Exception as e:
        print(f"Error running simple game: {e}")


def show_guide():
    """Display information about the beginner's guide"""
    print("📖 BEGINNER'S GUIDE")
    print("=" * 40)
    print()
    print("The beginner's guide is available in 'BEGINNER_GUIDE.md'")
    print("It explains all the fundamental Python concepts used in the simple game:")
    print()
    print("• Variables and Data Types")
    print("• Functions and Classes")
    print("• Loops and Conditionals")
    print("• Object-Oriented Programming")
    print("• Game Programming Basics")
    print()
    print("Open 'BEGINNER_GUIDE.md' in your text editor to read the full guide.")
    print()


def main():
    """Main program loop"""
    while True:
        show_menu()

        try:
            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                run_advanced_game()
            elif choice == "2":
                run_simple_game()
            elif choice == "3":
                show_guide()
            elif choice == "4":
                print("Thanks for trying the Ping Pong games! 🏓")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

            if choice in ["1", "2", "3"]:
                input("\nPress Enter to return to the main menu...")

        except KeyboardInterrupt:
            print("\n\nExiting... Thanks for playing! 🏓")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
