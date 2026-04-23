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

---

## 🛠️ Installation

Stelle sicher, dass du Python installiert hast. Du benötigst außerdem die `pygame` Bibliothek.

1. **Repository klonen oder herunterladen.**
2. **Abhängigkeiten installieren:**
   ```bash
   pip install pygame
   ```
3. **Spiel starten:**
   ```bash
   python main.py
   ```

---

## ⌨️ Steuerung

- **W, A, S, D:** LKW bewegen
- **Maus:** Menüs bedienen und Einstellungen anpassen

---

## 📂 Projektstruktur

- `main.py`: Die Hauptklasse, welche den Spielverlauf und die Menüs steuert.
- `fahrzeug.py`: Logik für den LKW (Bewegung, Kraftstoff, Ladung).
- `hubschrauber.py`: Die KI des gegnerischen Hubschraubers.
- `gebaeude.py`: Definitionen für Tankstelle, Lager und Endpunkt.
- `constants.py`: Farben und Spielzustände.
- `config.json`: Speichert deine aktuellen Einstellungen.

---

Viel Erfolg beim Transportieren! Pass auf deinen Rücken (und dein Dach) auf! 🚛💨