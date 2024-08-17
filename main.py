from app import create_app
from configuration import HOST, PORT

if __name__ == "main":
    app = create_app()
    app.run(host=HOST, port=PORT)
