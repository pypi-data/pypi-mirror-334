from functools import cached_property
from typing import Literal

from pydantic import BaseModel

from fitrequest.utils import is_basemodel_subclass

#: Global dictionnary used to map ``json/yaml`` declared models to actual python models.
environment_models = {}


class AttrSignature(BaseModel):
    """Represents the signature of the attribute."""

    name: str
    annotation: str
    attr_type: Literal['arg', 'kwarg']
    default_value: str | None = None

    @cached_property
    def signature(self) -> str:
        """Dumps flattened signature of the attribute."""
        if self.attr_type == 'arg':
            return f'{self.name}: {self.annotation}'
        return f'{self.name}: {self.annotation} = {self.default_value}'


class FlattenedModelSignature(BaseModel):
    """
    Represents flattened model signatures, simplifying nested Pydantic models into straightforward method signatures.

    This class flattens model structures to create simple signatures that are easy to handle with command-line tools.
    However, it has limitations: it does not support complex signatures
    involving unions (``Model | dict | None``) or lists (``list[Model]``).
    """

    model: type[BaseModel]

    def nested_signatures(self, prefix: str) -> list[AttrSignature]:
        """
        Update the names of attributes by appending the specified `prefix`,
        indicating this model represents a nested structure within another model.
        """
        for attr_sign in self.attr_signatures:
            attr_sign.name = f'{prefix}_{attr_sign.name}'
        return self.attr_signatures

    @cached_property
    def varnames(self) -> set[str]:
        """Return the names of all flattened attributes."""
        return {attr.name for attr in self.attr_signatures}

    @cached_property
    def attr_signatures(self) -> list[AttrSignature]:
        """
        Creates a flattened representation of the model's attributes suitable for fitrequest method signatures.
        The returned list is ordered with positional arguments (args) first, followed by keyword arguments (kwargs),
        following Python method signature conventions.
        """

        attr_signatures = []

        for field, info in self.model.model_fields.items():
            # Get nested pydantic model signature (reccursive)
            if is_basemodel_subclass(info.annotation):
                nested_model = FlattenedModelSignature(model=info.annotation)
                attr_signatures.extend(nested_model.nested_signatures(field))
                continue

            # Get orther types signature
            if 'class' in (field_type := str(info.annotation)):
                field_type = info.annotation.__qualname__

            if not info.is_required():
                default_value = info.get_default(call_default_factory=True)
                attr_signatures.append(
                    AttrSignature(
                        name=field,
                        annotation=field_type,
                        attr_type='kwarg',
                        default_value=repr(default_value),
                    )
                )
            else:
                attr_signatures.append(AttrSignature(name=field, annotation=field_type, attr_type='arg'))

        # Sort all positional parameters first followed by keyword parameters.
        args_signatures = filter(lambda x: x.attr_type == 'arg', attr_signatures)
        kwargs_signatures = filter(lambda x: x.attr_type == 'kwarg', attr_signatures)
        return [*sorted(args_signatures, key=lambda x: x.name), *sorted(kwargs_signatures, key=lambda x: x.name)]

    @cached_property
    def signature(self) -> list[str]:
        """Returns a flattened list of signatures for all attributes of the model."""
        return [attr_sign.signature for attr_sign in self.attr_signatures]
