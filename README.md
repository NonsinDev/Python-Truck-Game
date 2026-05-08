# 🚛 Cargo Clash: Sky Heist 🚁

**Cargo Clash: Sky Heist** is an top-down transport game built with Python and Pygame. You drive a truck, deliver valuable cargo, and must watch out for a thieving helicopter that tries to steal your load right off the truck!

---

## 🎮 Gameplay

Your goal in **Cargo Clash: Sky Heist** is to transport a set amount of cargo from the **Warehouse** to the **Delivery Point**. Watch out:
- **Refuel:** Your truck consumes fuel. Stop at the **Gas Station** before you run out!
- **The Sky Bandit:** A helicopter hunts you down and steals your cargo when it catches up.
- **Strategy:** Choose a game mode and tweak the settings to find the right challenge.

---

## ✨ Features

- **Three difficulty levels:** Easy, Normal, and Hard.
- **Custom mode:** Adjust speed, fuel consumption, and helicopter aggression individually.
- **Dynamic HUD:** Always keep track of your score, cargo, and fuel level.
- **Challenging AI:** The helicopter becomes more aggressive on higher difficulties.
- **Win & Lose conditions:** Reach the target score to win, but don't let the helicopter steal too much!
- **Random map layout:** Each round places buildings at new positions on the road network.
- **Road network:** Buildings are connected at fixed grid nodes with automatically drawn roads.
- **Pause menu:** ESC pauses the game with options to continue, reset, or return to the main menu.

---

## 🛠️ Installation

> **Note:** This game uses `pygame-ce` (Community Edition). PNG image loading is built in via SDL2 — no extra dependencies needed.

```
pip install pygame-ce
```

---

## ⌨️ Controls

- **W / S:** Drive forward / reverse
- **A / D:** Steer left / right
- **ESC:** Pause / open pause menu
- **Mouse:** Navigate menus and adjust settings
- **Ctrl + Start Game:** Enable debug mode (shows speed, position, helicopter state)

---

## 📂 Project Structure

- `main.py`: Main class — game loop, states, events, and collision logic.
- `default_config.json`: Default values for all game modes (Easy, Normal, Hard).
- `assets/`: Images used in the main menu (background, logo, truck).
- `game/constants.py`: Colors and game state constants.
- `game/button.py`: Reusable button component.
- `game/building.py`: Drawing and collision for buildings.
- `game/map.py`: Map generation with random building placement and road network.
- `game/truck.py`: Truck logic (movement, fuel, cargo).
- `game/helicopter.py`: Enemy helicopter AI.
- `game/renderer.py`: Drawing logic for the game screen, pause screen, and end screens.
- `game/menu/renderer.py`: Drawing logic for the main menu and settings screen.

---

