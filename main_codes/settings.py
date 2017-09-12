class Config(object):
    """Base configuration."""
    SECRET_KEY = 'hard to guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/models?charset=utf8'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


