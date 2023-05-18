from datetime import datetime
from peewee import Model, SqliteDatabase, IntegerField, DateField, TextField, CharField


db = SqliteDatabase('database.db')


class _BaseModel(Model):
    class Meta:
        database = db


class User(_BaseModel):
    class Meta:
        db_table = 'users'

    name = TextField(null=False, default='Пользователь')
    telegram_id = IntegerField(unique=True, null=False)
    registration_date = DateField(default=datetime.today())


class Movie(_BaseModel):
    class Meta:
        db_table = 'movies'

    description = TextField()
    photo_file_id = CharField(default=None, null=True)


def register_models() -> None:
    for model in _BaseModel.__subclasses__():
        model.create_table()
