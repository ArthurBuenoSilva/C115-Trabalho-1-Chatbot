import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration:
    SECRET_KEY = "37ce401419a7b05582cd19ee14ad958c5b05be9dcd00dac020ed495f254f0c70"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False