# 🎮 Tic-Tac-Toe AI

A Python-based Tic-Tac-Toe game featuring an AI opponent with multiple algorithms and heuristics.

---

## 🧠 Description

This project implements a 3x3 Tic-Tac-Toe game using **Python** and **Tkinter** for the GUI. The AI player can utilize various algorithms and heuristics, including:

- ♟️ Minimax
- ✂️ Minimax with Alpha-Beta Pruning
- 🔄 Minimax with Symmetry Pruning
- 🛡️ Heuristic Winning and Blocking
- ⚡ Heuristic with Fork Detection
- 🎯 Minimax with Winning and Blocking
- 🔍 Minimax with Fork Detection
- 🧭 Heuristic Positional Mobility

---

## 🚀 Features

- 🤖 Play against an AI with selectable algorithms
- ⏱️ Real-time move evaluation and turn switching
- ♻️ Option to start a new game
- 🏆 Display of game status and winner declaration

---

## 🛠️ Installation

1. Ensure you have **Python 3.x** installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tic-tac-toe-ai.git
   ```
3. Navigate to the project directory:
   ```bash
   cd tic-tac-toe-ai
   ```
4. Install the required library:
   ```bash
   pip install tk
   ```
5. Run the game:
   ```bash
   python Final_Tic_Tac_Toe.py
   ```

---

## 🎮 Usage

- Select an AI algorithm from the dropdown menu.
- Click on a square to place your mark (❌).
- The AI (⭕) will respond after your move.
- The game ends when someone wins or it's a tie.
- Click **"New Game"** to restart.

---

## 📚 Algorithms and Heuristics

| Algorithm/Heuristic   | Description                                            |
| --------------------- | ------------------------------------------------------ |
| `Minimax`             | Basic optimal decision tree algorithm.                 |
| `Alpha-Beta Pruning`  | Speeds up minimax by eliminating unnecessary branches. |
| `Symmetry Pruning`    | Reduces computation by recognizing symmetric states.   |
| `Winning & Blocking`  | Scores positions to win or block opponent.             |
| `Fork Detection`      | Detects two-way winning positions.                     |
| `Minimax + Winning`   | Minimax combined with heuristic for winning/blocking.  |
| `Minimax + Forks`     | Uses fork detection within minimax.                    |
| `Positional Mobility` | Prioritizes center and corner control.                 |

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests.
Suggestions and improvements are always welcome! 💡

---

## 👥 Team Members

- 👑 Youssef Said _(Leader)_
- Abdallah Adel
- Youssef Magdy
- Youssef Sadat
- Marwan Tamer

---

## 📄 License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

For any questions or feedback, please open an issue or contact the maintainer.
