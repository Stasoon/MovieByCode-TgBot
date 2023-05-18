from .models import Movie


def add_movie_and_get_code(description: str, photo_file_id: str = None) -> int:
    new_movie = Movie(description=description, photo_file_id=photo_file_id)
    new_movie.save()
    return new_movie.id


def get_movie_desc_by_code_or_none(code: int) -> tuple[str, str] | None:
    movie = Movie.get_or_none(Movie.id == code)
    return (movie.description, movie.photo_file_id) if movie else None


def get_all_movies() -> tuple[tuple[any, any]]:
    return tuple((movie.id, movie.description) for movie in Movie.select())


def delete_movie_by_code(code: int) -> bool:
    movie_to_delete = Movie.get_or_none(Movie.id == code)
    if movie_to_delete:
        movie_to_delete.delete_instance()
        return True
    else:
        return False
