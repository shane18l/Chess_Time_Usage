# ♟️ Chess Time Management Dashboard

This project explores how factors like time spent, game phase, piece moved in a chess game relates to move quality, using data collected from my own games. [Profile](https://www.chess.com/member/OkayKev)

## 🔍 Key Questions Explored
- Does spending more time on a move result in higher move quality?
- How does time management vary across game phases (opening, middlegame, endgame)?
- What pieces do I blunder most with?

## 📊 Dashboard Preview

![Dashboard Screenshot](images/dashboard.png)

[🔗 View the Interactive Dashboard on Tableau Public](https://public.tableau.com/views/ChessAnalysis_17467234829240/ChessAnalysis?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## 📁 Tools Used
- **Python **: Data cleaning, Extracting PGN data, Stockfish analysis
- **Excel**: Pivot tables, and preliminary analysis (initial visualizations)
- **Tableau**: Interactive dashboard creation and visual exploration

## 🧠 Features
- Interactive filters for game phase, time remaining
- Scatter plot: Time spent vs move quality
- Charts showing time trends and quality breakdowns

## 📌 Next Steps
- Analyze time-quality patterns based on opponent strength
- Incorporate opening names and material balance as context
- Compare games played with vs without a time increment

---

## 📝 Data Source
PGN data from personal games, converted to structured format, then exported to Excel/Tableau.

## 📂 Data
You can explore the cleaned game data and pivot analysis in [`excel_files/chess_analysis.xlsx`](data/chess_analysis.xlsx).

## 🛠️ How to Recreate This Project
To analyse your own account:

1. **Download Your Own Chess Games**  
   - Go to [lichess.org](https://lichess.org) or [chess.com](https://www.chess.com)  
   - Export your games as PGN files


2. **Replace Sample Games**  
   - Replace the files in 'match_histories/' with your own PGN files

3. **Download Stockfish Engine**  
   - [Download from the official site](https://stockfishchess.org/download/)  
   - Set the `engine_path` in `main.py` to your local `stockfish.exe` file

4. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt

5. **Optional** Add columns, extract more/less information from the chess games

6. **Run the script!** 
    ```bash
    python main.py

This generates a csv file, ready to be exported to Excel/Tableau!
