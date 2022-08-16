import pytest
from unittest.mock import MagicMock

# создаем фикстуру
from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)

    d_1 = Director(id=1, name='Маршалл')
    d_2 = Director(id=2, name='Доктер')
    d_3 = Director(id=3, name='Бержерон')

    # вызываем методы
    director_dao.get_one = MagicMock(return_value=d_1)
    director_dao.get_all = MagicMock(return_value=[d_1, d_2, d_3])
    director_dao.create = MagicMock(return_value=d_1)
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao

class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_d = {"name": "Фляйшер"}
        director = self.director_service.create(director_d)
        assert director.id is not None

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

    @pytest.mark.parametrize('director_original, director_new', parametres)
    def test_update(self, director_original, director_new):
        self.director_service.update(director_new)
        self.director_service.dao.update.assert_called_once_with(director_new)


    def test_delete(self):
        self.director_service.delete(1)
        self.director_service.dao.delete.assert_called_once_with(1)
