"""
File containing the main functionality of the package.
"""

from functools import update_wrapper
from collections.abc import Callable
from typing import ParamSpec, Type, TypeVar, Generic
from .decorator_protocol import DecoratorProtocol, DecoratorOutput

FunctionOutput = TypeVar("FunctionOutput")
FunctionParams = ParamSpec("FunctionParams")
DecoratorParams = ParamSpec("DecoratorParams")


class MetaDecorator(Generic[FunctionOutput], type):
    """
    Helps standardize the decorators and parametrize the decorator function.
    """

    def __new__(  # numpydoc ignore=PR02
        cls: Type["MetaDecorator[FunctionOutput]"],
        name: str,
        bases: tuple,  # type: ignore
        class_dict: dict,  # type: ignore
        decorator_function: Callable[[tuple, dict, tuple, dict], DecoratorOutput],  # type: ignore
    ) -> "MetaDecorator[FunctionOutput]":
        """
        Create the decorator from the decorator function.

        Parameters
        ----------
        cls : Type[type]
            The class type.
        name : str
            The name of the class.
        bases : tuple
            The bases of the class.
        class_dict : dict
            The class dictionary attribute.
        decorator_function : Callable[[list, dict, list, dict], DecoratorOutput]
            The decorator function. It must take the following arguments:
                - decorated_function: Callable[FunctionParams, FunctionOutput]
                - function_args: tuple
                - function_kwargs: dict
                - decorator_args: tuple
                - decorator_kwargs: dict

        Returns
        -------
        MetaDecorator
            The decorator.
        """
        # customize the creation of new classes here...
        class_dict["__init__"] = (
            lambda decorator_instance, *args, **kwargs: MetaDecorator._decorator_init(
                decorator_instance, *args, **kwargs
            )
        )
        class_dict["__call__"] = (
            lambda decorator_instance, *args, **kwargs: MetaDecorator._decorator_call(
                decorator_instance, *args, **kwargs
            )
        )
        class_dict["decorator_function"] = (
            lambda decorator_instance, *args, **kwargs: decorator_function(
                *args, **kwargs
            )
        )
        return super().__new__(cls, name, bases, class_dict)

    @staticmethod
    def _decorator_init(
        decorator_instance: DecoratorProtocol[DecoratorOutput],
        *args: DecoratorParams.args,  # type: ignore
        **kwargs: DecoratorParams.kwargs,  # type: ignore
    ) -> None:
        """
        Define the init method of the decorator that  will be created.

        Parameters
        ----------
        decorator_instance : DecoratorProtocol[DecoratorOutput]
            The decorator instance.
        *args : DecoratorParams.args
            The decorator arguments.
        **kwargs : DecoratorParams.kwargs
            The decorator keyword arguments.
        """
        update_wrapper(decorator_instance, decorator_instance.decorator_function)
        decorator_instance.decorator_args = args
        decorator_instance.decorator_kwargs = kwargs

    @staticmethod
    def _decorator_call(  # numpydoc ignore=PR04
        decorator_instance: DecoratorProtocol[DecoratorOutput],
        decorated_function: Callable[FunctionParams, FunctionOutput],
    ) -> Callable[FunctionParams, DecoratorOutput]:
        """
        Return the decorator.

        Parameters
        ----------
        decorator_instance : DecoratorProtocol[DecoratorOutput]
            The decorator instance.
        decorated_function : Callable[FunctionParams, FunctionOutput]
            The decorated function.

        Returns
        -------
        Callable[FunctionParams, DecoratorOutput]
            The decorated function with the modified behavior.
        """
        return lambda *args, **kwargs: decorator_instance.decorator_function(
            decorated_function,
            function_args=args,
            function_kwargs=kwargs,
            decorator_args=decorator_instance.decorator_args,
            decorator_kwargs=decorator_instance.decorator_kwargs,
        )


def to_decorator(  # numpydoc ignore=PR04
    decorator_function: Callable[[tuple, dict, tuple, dict], DecoratorOutput],  # type: ignore
) -> Type[DecoratorProtocol[DecoratorOutput]]:
    """
    Create a decorator class that will use the decorator function.

    Parameters
    ----------
    decorator_function : Callable[[list, dict, list, dict], DecoratorOutput]
        The decorator function. It must take the following arguments:
            - decorated_function: Callable[FunctionParams, FunctionOutput]
            - function_args: tuple
            - function_kwargs: dict
            - decorator_args: tuple
            - decorator_kwargs: dict

    Returns
    -------
    Type[DecoratorProtocol[DecoratorOutput]]
        The decorator class that will use the decorator function.
    """

    class Decorator(
        metaclass=MetaDecorator[DecoratorOutput],  # type: ignore
        decorator_function=decorator_function,
    ):
        """
        Defines a decorator class that will use the decorator function.
        """

        pass

    return Decorator  # type: ignore
