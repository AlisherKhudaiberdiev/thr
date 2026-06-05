from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Software(db.Model):
    __tablename__ = 'software'
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(100), nullable=False, unique=True)
    category            = db.Column(db.String(50))   # Office, Media, Dev, Gaming, Design, Browser, Security
    icon                = db.Column(db.String(10), default='💻')
    windows_only        = db.Column(db.Boolean, default=False)
    migration_difficulty = db.Column(db.Integer, default=2)  # 1=легко 2=средне 3=сложно
    description         = db.Column(db.Text)
    search_count        = db.Column(db.Integer, default=0)
    alternatives        = db.relationship('Alternative', backref='software', lazy=True)

class Alternative(db.Model):
    __tablename__ = 'alternatives'
    id          = db.Column(db.Integer, primary_key=True)
    software_id = db.Column(db.Integer, db.ForeignKey('software.id'), nullable=False)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    rating      = db.Column(db.Float, default=0.0)
    website     = db.Column(db.String(255))
    is_free     = db.Column(db.Boolean, default=True)
    similarity  = db.Column(db.Integer, default=80)  # % схожести с оригиналом

class Distro(db.Model):
    __tablename__ = 'distros'
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False, unique=True)
    description  = db.Column(db.Text)
    based_on     = db.Column(db.String(100))
    category     = db.Column(db.String(50))
    desktop      = db.Column(db.String(100))
    difficulty   = db.Column(db.String(20))
    min_ram      = db.Column(db.Integer, default=2)   # минимум ГБ RAM
    rating       = db.Column(db.Float, default=0.0)
    website      = db.Column(db.String(255))
    tags         = db.Column(db.String(200))
    why_good     = db.Column(db.Text)  # почему хорош для мигрантов с Windows

class MigrationResult(db.Model):
    __tablename__ = 'migration_results'
    id                = db.Column(db.Integer, primary_key=True)
    experience        = db.Column(db.String(20))
    purpose           = db.Column(db.String(20))
    ram               = db.Column(db.String(10))
    software_count    = db.Column(db.Integer)
    recommended_distro = db.Column(db.String(100))
    difficulty        = db.Column(db.String(20))
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)
