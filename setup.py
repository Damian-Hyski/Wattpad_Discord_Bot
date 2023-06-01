import subprocess
from bot import Database


def install_dependencies():
    subprocess.run(["pip", "install", "-r", "requirements.txt"])


def install_database():
    database = Database('data/wattpad_database.db')
    database.create_users_table()
    database.create_guilds_table()
    database.create_relations_table()


if __name__ == "__main__":
    install_dependencies()
    install_database()
