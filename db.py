import sqlite3
from os import path


class Database:
    def __init__( self, db_path=None ):
        if db_path == None:
            self._db_path = path.join( path.curdir, 'db', 'app.db' )
        else:
            self._db_path = db_path
        self._setup_database()

    def _generate_connection( self ):
        return sqlite3.connect( self._db_path )

    def _setup_database( self ):
        connection = self._generate_connection()
        cursor = connection.cursor()


        cursor.executescript( '''
            PRAGMA foreign_keys = ON;
            
            CREATE TABLE IF NOT EXISTS Users
              ( id INTEGER NOT NULL PRIMARY KEY
              , username TEXT
              , password_hash TEXT
              , email TEXT
              );
            
            CREATE TABLE IF NOT EXISTS Conversations
              ( id INTEGER NOT NULL PRIMARY KEY
              , name TEXT
              );
            
            CREATE TABLE IF NOT EXISTS Conversation_Members
              ( conversation_id INTEGER NOT NULL FOREIGN KEY
                  REFERENCES Conversations(id)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
              , member_id INTEGER FOREIGN KEY
                  REFERENCES Users(id)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
              );
            
            CREATE TABLE IF NOT EXISTS Messages
              ( id INTEGER NOT NULL PRIMARY KEY
              , sent DATETIME
              , edited BOOLEAN
              , contents TEXT
              , conversation_id INTEGER NOT NULL FOREIGN KEY
                  REFERENCES Conversations(id)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
              , sender_id INTEGER FOREIGN KEY
                  REFERENCES Users(id)
                    ON DELETE SET NULL
                    ON UPDATE NO ACTION
              );''' )
        connection.commit()
        connection.close()


