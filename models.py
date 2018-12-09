from werkzeug.security import gen_salt, generate_password_hash, check_password_hash
from typing import Optional


class User:
    def __init__( self, username: str, email: str, password: Optional[str], id: Optional[int] = None ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = None if password is None else generate_password_hash( password )

    def check_password( self, plain_password ):
        return check_password_hash( self.password_hash, plain_password )


def user_from_db_tuple( db_tuple: ( int, str, str, str ) ) -> User:
    user = User( id=db_tuple[0], username=db_tuple[1], email=db_tuple[2], password=None )
    user.password_hash = db_tuple[3]
    return user

