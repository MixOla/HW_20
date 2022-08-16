import pytest
from unittest.mock import MagicMock

# создаем фикстуру
from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    m_1 = Movie(id=1, title='Аманат',
                description='Фильм повествует о любви сына Шамиля Джамалутдина и Лизы Олениной на фоне драматических событий военной истории России первой половины XIX века',
                trailer="hjfgjkk",
                year=2022,
                rating=5,
                genre_id=3,
                director_id=3)
    m_2 = Movie(id=2, title='Винни пух',
                description='Мультфильм о приключениях Винни Пуха и его друзей',
                trailer = "hjgjhjkk",
                year=1969,
                rating=5,
                genre_id=2,
                director_id=2)
    m_3 = Movie(id=3, title='Смерш',
                description='История противостояния секретной разведслужбы СССР и Третьего Рейха в годы Великой Отечественной войны',
                trailer = "h45jgjkk",
                year=2019,
                rating=5,
                genre_id=1,
                director_id=1)

    # вызываем методы
    movie_dao.get_one = MagicMock(return_value=m_1)
    movie_dao.get_all = MagicMock(return_value=[m_1, m_2, m_3])
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_d ={
            "id": 1,
            "title": "В августе 44",
            "description": "fhbjbblb;",
            "trailer": "ghgjgk",
            "year": 2019,
            "rating": 5,
            "genre_id": 1,
            "director_id": 1
        }

        movie = self.movie_service.create(movie_d)
        assert movie.id is not None

    parametres = (
                (
                    {
                        'id': 1,
                        'title': 'Noname'
                    },
                    {
                        'id': 1,
                        'title': 'TestName'
                    }
                ),
            )

    @pytest.mark.parametrize('movie_original, movie_new', parametres)
    def test_update(self, movie_original, movie_new):
        self.movie_service.update(movie_new)
        self.movie_service.dao.update.assert_called_once_with(movie_new)


    def test_delete(self):
        self.movie_service.delete(1)
        self.movie_service.dao.delete.assert_called_once_with(1)
