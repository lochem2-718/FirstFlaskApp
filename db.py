from sqlite3 import connect, Connection, Cursor, PARSE_COLNAMES, PARSE_DECLTYPES
from os import path
from models import User, user_from_db_tuple
from typing import Optional


class Database:
    def __init__(self):
        self._db_path = path.join( path.curdir, 'db', 'app.db' )
        self._setup_database()

    def _generate_connection_and_cursor( self ) -> ( Connection, Cursor ):
        conn = connect( self._db_path, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES )
        cursor = conn.cursor()
        return conn, cursor

    def _setup_database(self) -> None:
        ( connection, cursor ) = self._generate_connection_and_cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.executescript( '''
            CREATE TABLE IF NOT EXISTS Users
              ( id INTEGER NOT NULL PRIMARY KEY
              , username TEXT
              , email TEXT
              , password_hash TEXT
              );
            
            CREATE INDEX IF NOT EXISTS User_username_Index 
              ON Users (username);
            
            CREATE TABLE IF NOT EXISTS Conversations
              ( id INTEGER NOT NULL PRIMARY KEY
              , name TEXT
              );
            
            CREATE TABLE IF NOT EXISTS Conversation_Members
              ( conversation_id INTEGER NOT NULL
              , member_id INTEGER 
              , FOREIGN KEY( member_id )
                  REFERENCES Users( id )
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
              , FOREIGN KEY( conversation_id )
                  REFERENCES Conversations( id )
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
              );
            
            CREATE TABLE IF NOT EXISTS Messages
              ( id INTEGER NOT NULL PRIMARY KEY
              , sent DATETIME
              , edited BOOLEAN
              , contents TEXT
              , conversation_id INTEGER NOT NULL 
              , sender_id INTEGER
              , FOREIGN KEY( conversation_id )
                  REFERENCES Conversations( id )
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
              , FOREIGN KEY( sender_id )
                  REFERENCES Users( id )
                    ON DELETE SET NULL
                    ON UPDATE NO ACTION
              );''' )
        connection.commit()
        connection.close()

    # User CRUD

    def create_user( self, user: User ) -> int:
        ( connection, cursor ) = self._generate_connection_and_cursor()
        cursor.execute(
            '''INSERT INTO Users ( username, password_hash, email ) VALUES ( ?, ?, ? )''',
            ( user.username, user.password_hash, user.email )
        )
        user_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return user_id

    def read_user( self, username: str ) -> Optional[ User ]:
        ( connection, cursor ) = self._generate_connection_and_cursor()
        cursor.execute(
            'SELECT * FROM Users WHERE username = ?',
            ( username, )
        )
        user_tuple = cursor.fetchone()
        connection.commit()
        connection.close()
        return user_from_db_tuple( user_tuple ) if user_tuple is not None else None

    def update_user_username( self, old_username: str, new_ussername: str) -> None:
        ( connection, cursor ) = self._generate_connection_and_cursor()
        cursor.execute(
            '''UPDATE Users
                SET username = ?
                WHERE username = ?''',
            ( new_ussername, old_username )
        )
        connection.commit()
        connection.close()

    def update_user_email(self, username: str, new_email: str ) -> None:
        ( connection, cursor ) = self._generate_connection_and_cursor()
        cursor.execute(
            '''UPDATE Users
                SET email = ?
                WHERE username = ?''',
            ( new_email, username )
        )
        connection.commit()
        connection.close()

    def update_user_password_hash(self, username: str, new_password_hash: str ) -> None:
        ( connection, cursor ) = self._generate_connection_and_cursor()
        cursor.execute(
            '''UPDATE Users
                SET password_hash = ?
                WHERE username = ?''',
            ( new_password_hash, username )
        )
        connection.commit()
        connection.close()

    def delete_user( self, username: str) -> Optional[ User ]:
        deleted_user_tuple = self.read_user( username )

        ( connection, cursor ) = self._generate_connection_and_cursor()
        cursor.execute(
            'DELETE FROM Users WHERE username = ?',
            ( username, )
        )

        connection.commit()
        connection.close()
        return user_from_db_tuple( deleted_user_tuple ) if deleted_user_tuple is not None else None

