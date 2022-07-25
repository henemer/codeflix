from abc import ABC
import abc
from dataclasses import field, dataclass
from pydoc import pager
from typing import Any, Generic, List, Optional, TypeVar
from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import NotFoundException

from __seedwork.domain.value_objects import UniqueEntityId

ET = TypeVar('ET', bound=Entity)


class RepositoryInterface(Generic[ET], ABC):

    @abc.abstractmethod
    def insert(self, entity) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all(self) -> List[ET]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, entity) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, entity_id: str | UniqueEntityId) -> None:
        raise NotImplementedError()


Input = TypeVar('Input')
Output = TypeVar('Output')


class SearchableRepositoryInterface(Generic[ET, Input, Output], RepositoryInterface[ET], ABC):

    @abc.abstractmethod
    def search(self, input_params: Input) -> Output:
        raise NotImplementedError()


Filter = TypeVar('Filter', str, Any)

@dataclass(slots=True, kw_only=True)
class SearchParams:
    page: Optional[int] = 1
    per_page: Optional[int] = 15
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None

    def __post_init__(self):
        self._normalize_page() 
        self._normalize_per_page()
        self._normalize_sort()
        self._normalize_sort_dir()
        self._normalize_filter()

    def _normalize_page(self):
        pass

    def _normalize_per_page(self):
        pass

    def _normalize_sort(self):
        pass

    def _normalize_sort_dir(self):
        pass

    def _normalize_filter(self):
        pass


@dataclass(slots=True)
class InMemoryRepository(RepositoryInterface[ET], ABC):
    items: List[ET] = field(default_factory=lambda: [])

    def insert(self, entity) -> None:
        self.items.append(entity)

    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        id_str = str(entity_id)
        return self._get(id_str)

    def find_all(self) -> List[ET]:
        return self.items

    def update(self, entity) -> None:
        entity_found = self._get(entity.id)
        index = self.items.index(entity_found)
        self.items[index] = entity

    def delete(self, entity_id: str | UniqueEntityId) -> None:
        id_str = str(entity_id)
        entity_found = self._get(id_str)
        self.items.remove(entity_found)

    def _get(self, entity_id: str) -> ET:
        entity = next(filter(lambda i: i.id == entity_id, self.items), None)
        if not entity:
            raise NotFoundException(f"Entity not found using ID '{entity_id}'")
        return entity
