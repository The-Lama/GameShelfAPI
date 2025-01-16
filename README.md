# GameShelfAPI
GameShelfAPI is a microservice-based project that provides information and recommendations for board games. It consists of multiple Flask-based services handling user preferences, game information, and personalized recommendations. Initially designed for local deployment, GameShelfAPI is built to scale with future cloud integration on Microsoft Azure.


## Download the Data

The data for this project is from the [Board Games Database on Kaggle](https://www.kaggle.com/datasets/threnjen/board-games-database-from-boardgamegeek).
To download the data, ensure you have the Kaggle CLI installed and authenticated, then run:
```bash
kaggle datasets download threnjen/board-games-database-from-boardgamegeek -p data --unzip
```
The /data directory is used to store the board game dataset. Since the data files are not included in the repository, a placeholder file .gitkeep is used to ensure the folder exists in the project structure.
You can also use other ways to download the data to the /data directory.