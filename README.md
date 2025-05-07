# Cosmic Clash - Space Shooter Game

Cosmic Clash is a 2D space shooter game built with **Pygame**. The game allows players to control a spaceship, dodge alien enemies, and collect goodies like gold and shields to score points and protect themselves. Players can shoot lasers to eliminate aliens and aim for the high score leaderboard.

## Features

- **Spaceship Movement**: The player moves the spaceship by dragging the mouse.
- **Shooting**: Press the spacebar to shoot lasers at aliens.
- **Enemies (Aliens)**: Aliens move down the screen, and the player must dodge or destroy them for points.
- **Goodies**: Collect gold to earn points and a special laser when you collect 10 gold and shields for protection.
- **High Scores**: Track and display top 10 high scores.
- **Game States**: 
  - **Splash Screen**: Introduction and game instructions.
  - **Gameplay**: The core gameplay where players shoot lasers and dodge enemies.
  - **High Scores**: View and reset the high score leaderboard.

## Game Design

### Structure
- **Scene Management**: The game is divided into scenes (Splash, Play, High Scores) handled by the `pyghelpers.SceneMgr`.
- **Player Interaction**: The player interacts with the game via the mouse to move the spaceship and the keyboard to shoot lasers.
- **Game Logic**: 
  - The player earns points by dodging aliens and shooting them with lasers.
  - Collecting gold provides points, while collecting shields offers temporary invincibility.
- **High Score System**: 
  - The `HighScoresData` class manages the top 10 scores, stored in a JSON file (`HighScores.json`).
  - Scores are added to the leaderboard when the player achieves a new high score.

### Files and Implementation
- **Constants.py**: Defines constants for game dimensions, colors, point values, and scene keys.
- **HighScores.json**: Stores the top 10 high scores in a JSON format.
- **HighScoresData.py**: Manages high score data, including adding new scores and saving/loading from `HighScores.json`.
- **Main_Dodger.py**: The main game loop, which initializes and runs the scenes.
- **Player.py**: Handles the player's spaceship, including movement and shooting mechanics.
- **SceneHighScores.py**: Displays the high score leaderboard and allows players to reset or view high scores.
- **SceneSplash.py**: The introductory scene with game instructions and buttons to start the game or view high scores.
- **ScenePlay.py**: The core game scene where the player interacts with the game, dodging and shooting enemies.

## Running the Game

### Prerequisites
Make sure you have **Python 3** and **Pygame** installed.

1. Install **Pygame** if you don't have it:

2. Clone or download the repository.

3. Run the game with the following command:


### Controls
- **Move**: Use the mouse to move the spaceship.
- **Shoot**: Press the **spacebar** to fire lasers.
- **Pause/Exit**: Use the quit button in the menu to exit the game.

### High Scores
- The game tracks the top 10 high scores. Players are prompted to enter their name if they achieve a new high score.

## Design Choices

- **Modular Design**: The game is divided into different scenes (Splash, Play, High Scores), each handled by its own class. This modular approach makes it easier to manage different parts of the game.
- **Game Objects**: The game uses objects like the `Player`, `Baddie`, and `Goodie` to manage their respective behaviors and interactions. These objects are updated and drawn each frame.
- **High Score Management**: The high scores are stored in a JSON file and managed via the `HighScoresData` class. This class handles adding new scores, saving, and loading the leaderboard.
- **Graphics and Sound**: The game uses images for the spaceship, enemies, and goodies, as well as background music and sound effects for actions like shooting and game over.

## Credits

- **Pygame**: A library used to create the game.
- **pygwidgets** and **pyghelpers**: Libraries for managing game UI elements and scenes.
- **Graphics and Sound**: Custom images and sound effects used for the game visuals and interactions.

---

Enjoy playing **Cosmic Clash** and aim for the highest score!

If you would like to see the original game that I used as my base: see the **Original Dodger** file to compare!
