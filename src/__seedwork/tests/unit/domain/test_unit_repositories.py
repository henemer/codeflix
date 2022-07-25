# pylint:disable=unexpected-keyword-arg
from dataclasses import dataclass
import unittest
from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import NotFoundException

from __seedwork.domain.repositories import InMemoryRepository, RepositoryInterface
from __seedwork.domain.value_objects import UniqueEntityId


class TestRepositoryInterface(unittest.TestCase):
    def test_throw_error_when_method_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            RepositoryInterface()
        self.assertEqual(assert_error.exception.args[0],
                         "Can't instantiate abstract class RepositoryInterface with abstract methods delete, find_all, " +
                         "find_by_id, insert, update")


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: float


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


class TestInMemoryRepository(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()

    def test_items_prop_is_empty_on_init(self):
        self.assertEqual(self.repo.items, [])

    def test_insert(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)
        self.assertEqual(self.repo.items[0], entity)

    def test_throw_exception_not_found_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('fake id')
        
        self.assertEqual(assert_error.exception.args[0],
                         "Entity not found using ID 'fake id'")

        unique_entity_id = UniqueEntityId('c1f40ced-dfdf-4997-a1ae-84857c6101fd')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        
        self.assertEqual(assert_error.exception.args[0],
                         "Entity not found using ID 'c1f40ced-dfdf-4997-a1ae-84857c6101fd'")
    
    def test_find_by_id(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)
     
        entity_found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity_found, entity)

        entity_found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(entity_found, entity)

    def test_find_all(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)

        items = self.repo.find_all()
        self.assertListEqual(items, [entity])


    def test_throw_exception_not_found_in_update(self):
        entity = StubEntity(name='test', price=5)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(entity.id)
        
        self.assertEqual(assert_error.exception.args[0],
                        f"Entity not found using ID '{entity.id}'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(entity.unique_entity_id)
        
        self.assertEqual(assert_error.exception.args[0],
                         f"Entity not found using ID '{entity.id}'")

    def test_update(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)
        entity_updated = StubEntity(unique_entity_id=entity.unique_entity_id, name='updated', price=1)
        self.repo.update(entity_updated)

        self.assertEqual(entity_updated, self.repo.items[0])


    def test_throw_exception_not_found_in_delete(self):
        entity = StubEntity(name='test', price=5)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.id)
        
        self.assertEqual(assert_error.exception.args[0],
                         f"Entity not found using ID '{entity.id}'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(entity.unique_entity_id)
        
        self.assertEqual(assert_error.exception.args[0],
                         f"Entity not found using ID '{entity.id}'")

    def test_delete(self):
        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)
        self.repo.delete(entity.id)
        self.assertListEqual(self.repo.items, [])

        entity = StubEntity(name='test', price=5)
        self.repo.insert(entity)
        self.repo.delete(entity.unique_entity_id)
        self.assertListEqual(self.repo.items, [])
