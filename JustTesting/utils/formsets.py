from typing import Optional
from django import forms


class ModelAndInlineFormsetContainer:
    model = None
    model_fields = ()
    formset_model = None
    formset_model_fields = ()
    formset = None
    formset_model_foreignkey_name = ""

    def __init__(self, **kwargs):
        form = forms.modelform_factory(
            model=self.model, fields=self.model_fields
        )
        self.form = form(**kwargs)

        formset_factory = forms.inlineformset_factory(
            self.model,
            self.formset_model,
            formset=self.formset,
            fields=self.formset_model_fields,
            extra=2,
        )
        self.formset = formset_factory(
            queryset=self.formset_model.objects.none(), **kwargs
        )

    def is_valid(self):
        return self.form.is_valid() and self.formset.is_valid()

    def save(self, commit: bool = True):
        new_instance = self.model(**(self.form.cleaned_data))
        new_instance.save()
        for form in self.formset:
            d: Optional[dict] = {}
            for field in self.formset_model_fields:
                value = form.cleaned_data.get(field)
                if value is not None:
                    d[field] = value
                else:
                    d = None
                    break
            if d is not None:
                d[self.formset_model_foreignkey_name] = new_instance
                new_object = self.formset_model(**d)
                new_object.save()
