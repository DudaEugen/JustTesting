class MultiTableInheritanceBaseManagerMixin:
    """
    Mixin for manager of base class for multi table inheritance.
    (Depth of inheritance is 1)

    Methods select_related_all and select_related_filter return
    list of derivative instances.
    """

    def select_related_all(self) -> list:
        base_instances = self._select_related().all()
        return self._cast_to_derivative(base_instances)

    def select_related_filter(self, **kwargs) -> list:
        base_instances = self.select_related().filter(**kwargs)
        return self._cast_to_derivative(base_instances)

    def select_related_get(self, **kwargs):
        base_instance = self.select_related().get(**kwargs)
        return self._cast_to_derivative(base_instance)

    def _cast_to_derivative(self, base_instances):
        from django.db.models import QuerySet

        instances = base_instances if isinstance(base_instances, QuerySet) \
            else [base_instances]
        result = []
        for instance in instances:
            for cl in self.model.__subclasses__():
                try:
                    result.append(eval(f"instance.{cl.__name__.lower()}"))
                    break
                except cl.DoesNotExist:
                    pass
        if not isinstance(base_instances, QuerySet):
            return result[0]
        return result

    def _select_related(self):
        print()
        return self.select_related(
            *tuple(cl.__name__.lower() for cl in self.model.__subclasses__())
        )
