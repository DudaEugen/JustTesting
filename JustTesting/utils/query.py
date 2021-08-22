from django.db.models.query import QuerySet
from django.db.models.manager import Manager
from typing import Optional


class InheritanceQyerySetWrapper:
    """
    Wrapping QuerySet instance.
    Depth of inheritance is 1.

    Using select_related on all derivative classes and 
    define type of instance before returning 
    (return derivative class instance instead of base class instance if exist)
    """

    def __init__(self, queryset: Optional[QuerySet] = None,
                 model=None, query=None, using=None, hints=None):
        self._iter = None
        self._query_set = queryset if queryset is not None else\
            QuerySet(model, query, using, hints)
        if not self._query_set.query.select_related:
            self._query_set.select_related(
                *tuple(cl.__name__.lower() for cl in self._query_set.model.__subclasses__())
            )

    def _cast_to_derivative(self, base_instance):
        for cl in self._query_set.model.__subclasses__():
            try:
                return eval(f"base_instance.{cl.__name__.lower()}")
            except cl.DoesNotExist:
                pass
        return base_instance

    def first(self):
        return self._cast_to_derivative(self._query_set.first())

    def last(self):
        return self._cast_to_derivative(self._query_set.last())

    def all(self):
        return InheritanceQyerySetWrapper(self._query_set.all())

    def filter(self, *args, **kwargs):
        return InheritanceQyerySetWrapper(self._query_set.filter(*args, **kwargs))

    def get(self, *args, **kwargs):
        return self._cast_to_derivative(self._query_set.get(*args, **kwargs))

    def order_by(self, *field_names):
        return InheritanceQyerySetWrapper(self._query_set.order_by(*field_names))

    def __iter__(self):
        self._iter = iter(self._query_set)
        return self

    def __next__(self):
        return self._cast_to_derivative(next(self._iter))

    def __getitem__(self, k):
        return self._cast_to_derivative(self._query_set[k])

    def __bool__(self):
        return self._query_set.__bool__()

    def __len__(self):
        return len(self._query_set)

    def __repr__(self):
        instances = []
        for base_instance in self:
            instances.append(self._cast_to_derivative(base_instance))
        return f"<{self.__class__.__name__}: {instances}>"


class InheritanceManager(Manager):
    """
    Manager of base class for multi table inheritance.
    (Depth of inheritance is 1)

    Method select_derivatives return InheritanceQyerySetWrapper 
    that returning derivative instances if those exists.
    """

    def select_derivatives(self) -> InheritanceQyerySetWrapper:
        return InheritanceQyerySetWrapper(model=self.model)
