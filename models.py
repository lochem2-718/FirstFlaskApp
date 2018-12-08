from werkzeug.security import gen_salt, generate_password_hash, check_password_hash

class User():
    def __init__( self, username : str, password : str ):
        self.username = username
        self.password_hash = generate_password_hash( password )

    def check_password( self, plain_password : str ) -> bool:
        return check_password_hash( self.password_hash, plain_password )


