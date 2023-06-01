import sqlite3


class Database:
    def __init__(self, database: str):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def create_users_table(self):
        query = """
        CREATE TABLE users (
            dc_user_id INTEGER PRIMARY KEY, 
            wp_name TEXT,
            wp_last_message_date INTEGER DEFAULT (0),
            wp_number_of_stories INTEGER DEFAULT (0),
            wp_last_part_date INTEGER DEFAULT (0)
        )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def create_guilds_table(self):
        query = """
        CREATE TABLE guilds (
            dc_guild_id INTEGER PRIMARY KEY,
            dc_notification_channel_id INTEGER
        )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def create_relations_table(self):
        query = """
        CREATE TABLE relations (
            dc_user_id INTEGER,
            dc_guild_id INTEGER,
            FOREIGN KEY (dc_user_id) REFERENCES users (dc_user_id)
            FOREIGN KEY (dc_guild_id) REFERENCES guilds (dc_guild_id)
            PRIMARY KEY (dc_user_id, dc_guild_id)
            )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def add_user(self, dc_user_id: int, wp_name: str, wp_last_message_date: int, wp_number_of_stories: int,
                 wp_last_part_date: int):
        query = """
        INSERT INTO users (
        dc_user_id, wp_name, wp_last_message_date, wp_number_of_stories, wp_last_part_date
        ) VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (dc_user_id, wp_name, wp_last_message_date, wp_number_of_stories, wp_last_part_date))
        self.connection.commit()

    def add_guild(self, dc_guild_id):
        query = 'INSERT INTO guilds (dc_guild_id) VALUES (?)'
        self.cursor.execute(query, (dc_guild_id,))
        self.connection.commit()

    def add_relation(self, dc_user_id, dc_guild_id):
        query = 'INSERT INTO relations (dc_user_id, dc_guild_id) VALUES (?, ?)'
        self.cursor.execute(query, (dc_user_id, dc_guild_id))
        self.connection.commit()

    def set_notification_channel(self, dc_guild_id, dc_channel_id):
        query = 'UPDATE guilds SET dc_notification_channel_id = ? WHERE dc_guild_id = ?'
        self.cursor.execute(query, (dc_channel_id, dc_guild_id))
        self.connection.commit()

    def set_last_message_date(self, wp_last_message_date, dc_user_id):
        query = 'UPDATE users SET wp_last_message_date = ? WHERE dc_user_id = ?'
        self.cursor.execute(query, (wp_last_message_date, dc_user_id))
        self.connection.commit()

    def set_last_part_date(self, wp_last_part_date, dc_user_id):
        query = 'UPDATE users SET wp_last_part_date = ? WHERE dc_user_id = ?'
        self.cursor.execute(query, (wp_last_part_date, dc_user_id))
        self.connection.commit()

    def set_number_of_stories(self, wp_number_of_stories, dc_user_id):
        query = 'UPDATE users SET wp_number_of_stories = ? WHERE dc_user_id = ?'
        self.cursor.execute(query, (wp_number_of_stories, dc_user_id))
        self.connection.commit()

    def check_user_exists(self, dc_user_id: int) -> bool:
        query = 'SELECT COUNT(*) FROM users WHERE dc_user_id = ?'
        self.cursor.execute(query, (dc_user_id,))
        result = self.cursor.fetchone()[0]

        return result > 0

    def check_guild_exists(self, dc_guild_id: int) -> bool:
        query = 'SELECT COUNT(*) FROM guilds WHERE dc_guild_id = ?'
        self.cursor.execute(query, (dc_guild_id,))
        result = self.cursor.fetchone()[0]

        return result > 0

    def find_user(self, dc_user_id) -> tuple:
        query = 'SELECT * FROM users WHERE dc_user_id = ?'
        self.cursor.execute(query, (dc_user_id,))
        result = self.cursor.fetchone()

        return result

    def find_all_users(self):
        query = 'SELECT * FROM users'
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result

    def get_guilds_in_user(self, dc_user_id):
        query = """
        SELECT guilds.* FROM guilds
        INNER JOIN relations ON guilds.dc_guild_id = relations.dc_guild_id
        INNER JOIN users ON users.dc_user_id = relations.dc_user_id
        WHERE users.dc_user_id = ?
        """
        self.cursor.execute(query, (dc_user_id,))
        result = self.cursor.fetchall()

        return result

    def get_users_in_guild(self, dc_guild_id):
        query = """
        SELECT users.dc_user_id, users.wp_name FROM users
        INNER JOIN relations ON users.dc_user_id = relations.dc_user_id
        INNER JOIN guilds ON guilds.dc_guild_id = relations.dc_guild_id
        WHERE guilds.dc_guild_id = ?
        """
        self.cursor.execute(query, (dc_guild_id,))
        result = self.cursor.fetchall()

        return result

    def remove_user(self, dc_user_id):
        query = 'DELETE FROM users WHERE dc_user_id = ?'
        self.cursor.execute(query, (dc_user_id,))
        self.connection.commit()

    def remove_guild(self, dc_guild_id: int):
        query = 'DELETE FROM guilds WHERE dc_guild_id = ?'
        self.cursor.execute(query, (dc_guild_id,))
        self.connection.commit()

    def remove_relation(self, dc_user_id, dc_guild_id):
        query = 'DELETE FROM relations WHERE dc_user_id = ? AND dc_guild_id = ?'
        self.cursor.execute(query, (dc_user_id, dc_guild_id))
        self.connection.commit()
