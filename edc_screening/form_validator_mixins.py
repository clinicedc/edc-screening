from __future__ import annotations

from typing import TYPE_CHECKING, Type

from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .utils import get_subject_screening_model

if TYPE_CHECKING:
    from .model_mixins import ScreeningModelMixin


class SubjectScreeningFormValidatorMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._subject_screening = None
        self.screening_identifier = self.cleaned_data.get("screening_identifier")

    @property
    def subject_screening_model(self) -> str:
        return get_subject_screening_model()

    @property
    def subject_screening_model_cls(self) -> Type[ScreeningModelMixin]:
        return django_apps.get_model(self.subject_screening_model)

    @property
    def subject_screening(self) -> ScreeningModelMixin:
        if not self._subject_screening:
            try:
                self._subject_screening = self.subject_screening_model_cls.objects.get(
                    screening_identifier=self.screening_identifier
                )
            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    'Complete the "Subject Screening" form before proceeding.',
                    code="missing_subject_screening",
                )
        return self._subject_screening
