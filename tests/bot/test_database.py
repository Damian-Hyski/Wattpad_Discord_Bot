import pytest
from bot import Database


class TestDatabase:
    @pytest.fixture
    def database(self):
        db = Database(':memory:')
        yield db
        del db

    def test_create_users_table(self, database):
        database.create_users_table()
        tables = database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        assert ('users',) in tables

    def test_create_guilds_table(self, database):
        database.create_guilds_table()
        tables = database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        assert ('guilds',) in tables

    def test_create_relations_table(self, database):
        database.create_relations_table()
        tables = database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        assert ('relations',) in tables

    def test_add_user(self, database):
        database.create_users_table()
        database.add_user(1, 'John', 0, 0, 0)
        result = database.find_user(1)
        assert result == (1, 'John', 0, 0, 0)

    def test_add_guild(self, database):
        database.create_guilds_table()
        database.add_guild(1)
        result = database.check_guild_exists(1)
        assert result is True

    def test_add_relation(self, database):
        database.create_users_table()
        database.create_guilds_table()
        database.create_relations_table()
        database.add_user(1, 'John', 0, 0, 0)
        database.add_guild(1)
        database.add_relation(1, 1)
        result = database.get_guilds_in_user(1)
        assert result == [(1, None)]

    def test_set_notification_channel(self, database):
        database.create_guilds_table()
        database.add_guild(1)
        database.set_notification_channel(1, 100)
        result = database.cursor.execute("SELECT dc_notification_channel_id FROM guilds WHERE dc_guild_id = 1").fetchone()
        assert result == (100,)

    def test_set_last_message_date(self, database):
        database.create_users_table()
        database.add_user(1, 'John', 0, 0, 0)
        database.set_last_message_date(123456789, 1)
        result = database.cursor.execute("SELECT wp_last_message_date FROM users WHERE dc_user_id = 1").fetchone()
        assert result == (123456789,)

    def test_set_last_part_date(self, database):
        database.create_users_table()
        database.add_user(1, 'John', 0, 0, 0)
        database.set_last_part_date(987654321, 1)
        result = database.cursor.execute("SELECT wp_last_part_date FROM users WHERE dc_user_id = 1").fetchone()
        assert result == (987654321,)

    def test_set_number_of_stories(self, database):
        database.create_users_table()
        database.add_user(1, 'John', 0, 0, 0)
        database.set_number_of_stories(5, 1)
        result = database.cursor.execute("SELECT wp_number_of_stories FROM users WHERE dc_user_id = 1").fetchone()
        assert result == (5,)

    def test_check_user_exists(self, database):
        database.create_users_table()
        database.add_user(1, 'John', 0, 0, 0)
        result = database.check_user_exists(1)
        assert result is True

    def test_check_guild_exists(self, database):
        database.create_guilds_table()
        database.add_guild(1)
        result = database.check_guild_exists(1)
        assert result is True

    def test_find_user(self, database):
        database.create_users_table()
        database.add_user(1, 'John', 0, 0, 0)
        result = database.find_user(1)
        assert result == (1, 'John', 0, 0, 0)

    def test_find_all_users(self, database):
        database.create_users_table()
        database.add_user(1, 'John', 0, 0, 0)
        database.add_user(2, 'Jane', 0, 0, 0)
        result = database.find_all_users()
        assert result == [(1, 'John', 0, 0, 0), (2, 'Jane', 0, 0, 0)]

    def test_get_guilds_in_user(self, database):
        database.create_users_table()
        database.create_guilds_table()
        database.create_relations_table()
        database.add_user(1, 'John', 0, 0, 0)
        database.add_guild(1)
        database.add_relation(1, 1)
        result = database.get_guilds_in_user(1)
        assert result == [(1, None)]

    def test_get_users_in_guild(self, database):
        database.create_users_table()
        database.create_guilds_table()
        database.create_relations_table()
        database.add_user(1, 'John', 0, 0, 0)
        database.add_user(2, 'Jane', 0, 0, 0)
        database.add_guild(1)
        database.add_relation(1, 1)
        database.add_relation(2, 1)
        result = database.get_users_in_guild(1)
        assert result == [(1, 'John'), (2, 'Jane')]

    def test_remove_user(self, database):
        database.create_users_table()
        database.add_user(1, 'John', 0, 0, 0)
        database.remove_user(1)
        result = database.check_user_exists(1)
        assert result is False

    def test_remove_guild(self, database):
        database.create_guilds_table()
        database.add_guild(1)
        database.remove_guild(1)
        result = database.check_guild_exists(1)
        assert result is False

    def test_remove_relation(self, database):
        database.create_users_table()
        database.create_guilds_table()
        database.create_relations_table()
        database.add_user(1, 'John', 0, 0, 0)
        database.add_guild(1)
        database.add_relation(1, 1)
        database.remove_relation(1, 1)
        result = database.get_guilds_in_user(1)
        assert result == []
