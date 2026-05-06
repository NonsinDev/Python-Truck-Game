# 🚛 Cargo Clash: Sky Heist 🚁

**Cargo Clash: Sky Heist** ist ein spannendes Top-Down Transport-Spiel, entwickelt mit Python und Pygame. Du steuerst einen LKW, lieferst wertvolle Fracht ab und musst dich vor einem diebischen Hubschrauber in Acht nehmen, der versucht, deine Ladung direkt von der Ladefläche zu stehlen!

---

## 🎮 Gameplay

In **Cargo Clash: Sky Heist** ist dein Ziel, eine bestimmte Menge an Fracht vom **Lager** zum **Endpunkt** zu transportieren. Aber Vorsicht:
- **Tanken:** Dein LKW verbraucht Benzin. Halte rechtzeitig an der **Tankstelle** an!
- **Der Bandit am Himmel:** Ein Hubschrauber verfolgt dich und stiehlt deine Ladung, wenn er dich einholt.
- **Strategie:** Wähle deinen Modus und passe die Spieleinstellungen an, um die perfekte Herausforderung zu finden.

---

## ✨ Features

- **Drei Schwierigkeitsgrade:** Leicht, Normal und Schwer.
- **Custom-Modus:** Passe Geschwindigkeit, Benzinverbrauch und Hubschrauber-Aggressivität individuell an.
- **Dynamisches HUD:** Behalte deine Punkte, Ladung und den Benzinstand immer im Blick.
- **Herausfordernde KI:** Der Hubschrauber agiert je nach Schwierigkeitsgrad aggressiver.
- **Sieg & Niederlage:** Erreiche das Zielgewicht, um zu gewinnen, aber lass nicht zu, dass der Hubschrauber zu viel stiehlt!
- **Zufälliges Kartenlayout:** Jede Runde platziert die Gebäude auf neuen Positionen im Straßennetz.
- **Straßennetz:** Gebäude werden an Knotenpunkten eines festen Rasters verbunden – mit automatisch gezeichneten Straßen.
- **Pause-Menü:** ESC pausiert das Spiel und bietet Optionen zum Weiterspielen, Neustarten oder zum Hauptmenü zurückzukehren.

---

## 🛠️ Installation

> **Hinweis:** Das Spiel nutzt `pygame-ce` (Community Edition) als Abhängigkeit.

```
pip install pygame-ce
```

---

## ⌨️ Steuerung

- **W, A, S, D:** LKW bewegen
- **ESC:** Spiel pausieren / Pause-Menü öffnen
- **Maus:** Menüs bedienen und Einstellungen anpassen

---

## 📂 Projektstruktur

- `main.py`: Hauptklasse – Spielverlauf, Menüs, Pause und Kartengenerierung.
- `game/truck.py`: Logik für den LKW (Bewegung, Kraftstoff, Ladung).
- `game/helicopter.py`: KI des gegnerischen Hubschraubers.
- `game/building.py`: Definitionen für Tankstelle, Lager und Endpunkt.
- `game/button.py`: Wiederverwendbare Button-Komponente.
- `game/constants.py`: Farben und Spielzustände.
- `config.json`: Speichert deine aktuellen Einstellungen.
- `default_config.json`: Standardwerte für alle Spielmodi.

---

Viel Erfolg beim Transportieren! Pass auf deinen Rücken (und dein Dach) auf! 🚛💨
