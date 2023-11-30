class Config(object):
    DEBUG = False
    TESTING = False
    DUENO_ID = None
    SQLALCHEMY_DATABASE_URI = "sqlite:///mascotas.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_SECRET_KEY = '5e3d937f09a95865e69e2b91920bf642929bb1edbc45f2fbe38eb57fc037aa56'

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mascotas:mascotas@localhost/mascotas'
    SECRET_KEY = '5e3d937f09a95865e69e2b91920bf642929bb1edbc45f2fbe38eb57fc037aa56'

class DevelpmentConfig(Config):
    DEBUG = True
    SECRET_KEY = '5e3d937f09a95865e69e2b91920bf642929bb1edbc45f2fbe38eb57fc037aa56'
    # SECRET_KEY = '5e3d937f09a95865e69e2b91920bf642929bb1edbc45f2fbe38eb57fc037aa56'
