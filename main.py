from app.main import create_app
from app.core.config import Config

# Build Flask application instance
app = create_app()

if __name__ == "__main__":
    # Serve app on configured local port parameters
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
