from .models import User


# region SQL Get

def get_user_by_telegram_id_or_none(telegram_id: int) -> User | None:
    return User.get_or_none(User.telegram_id == telegram_id)


def get_user_ids_to_mailing() -> tuple:
    return tuple(user.telegram_id for user in User.select())


def get_users_count() -> int:
    return len(User.select())


# endregion


# region SQL Create

def create_user(telegram_id: int, name: str) -> None:
    if not get_user_by_telegram_id_or_none(telegram_id):
        User.create(name=name, telegram_id=telegram_id)


# endregion
