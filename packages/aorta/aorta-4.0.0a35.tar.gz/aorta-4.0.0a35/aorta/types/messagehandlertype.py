# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
import types
import typing
from typing import Any

from .command import Command
from .event import Event



class MessageHandlerType(type):
    __module__: str = 'aorta.types'
    handles: type[Command | Event]
    parameter_name: str

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: Any
    ) -> 'MessageHandlerType':
        # Do some checks to ensure that handlers are properly implemented.
        is_abstract = namespace.pop('__abstract__', False)
        new_class = super().__new__(cls, name, bases, {**namespace, 'handles': []})
        if is_abstract:
            return new_class
        
        # Ensure that the handle() method accepts the message as the first
        # parameter.
        sig = inspect.signature(new_class.handle) # type: ignore
        parameters = list(sig.parameters.values())
        if len(parameters) < 2:
            raise TypeError(
                f"Invalid number of arguments for {name}.handle(). "
                f"Ensure that the parameters accepted by this method are at "
                f"least {name}.handle(self, {cls.parameter_name}: "
                f"{cls.handles.__name__})."
            )

        arg = parameters[1]
        if arg.name != cls.parameter_name:
            raise TypeError(
                f'The first positional argument to {name}.handle() '
                f'must be named `{cls.parameter_name}`, got `{arg.name}`.'
            )

        args: set[type] = set()
        handles: set[type[Command | Event]] = set()
        for b in getattr(new_class, '__orig_bases__', []):
            args.update(typing.get_args(b))
        for t in args:
            if typing.get_origin(t) in (typing.Union, types.UnionType):
                handles.update(typing.get_args(t))
                continue
            if not inspect.isclass(t) or not issubclass(t, (Command, Event)):
                continue
            handles.add(t)

        new_class.handles = list(handles) # type: ignore
        return new_class