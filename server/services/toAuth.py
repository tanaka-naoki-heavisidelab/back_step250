from passlib.context import CryptContext

# Dependの引数にするには関数型で渡す。インスタンスはエラーになる。
def get_pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")