from flask import Flask

from services.game_service.routes import game_routes

app = Flask(__name__)
app.register_blueprint(game_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
