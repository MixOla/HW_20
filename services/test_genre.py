import pytest
from unittest.mock import MagicMock

# создаем фикстуру
from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)

    g_1 = Genre(id=1, name='Фантастика')
    g_2 = Genre(id=2, name='Мультфильм')
    g_3 = Genre(id=3, name='Мюзикл')

    # вызываем методы
    genre_dao.get_one = MagicMock(return_value=g_1)
    genre_dao.get_all = MagicMock(return_value=[g_1, g_2, g_3])
    genre_dao.create = MagicMock(return_value=Genre(id=4))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao

class TestDirectorService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        directors = self.genre_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        genre_d = {"name": "Боевик"}
        genre = self.genre_service.create(genre_d)
        assert genre.id is not None

