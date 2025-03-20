"""
Define the `DecoratorProtocol` class that describes the methods of a decorator.
"""

from typing import Protocol, TypeVar, ParamSpec, Callable, Any, Generic

FunctionOutput = Any  # for readability
DecoratorOutput = TypeVar("DecoratorOutput")
DecoratedFunctionParams = ParamSpec("DecoratedFunctionParams")
DecoratorParams = ParamSpec("DecoratorParams")


class DecoratorProtocol(  # type: ignore # numpydoc ignore=PR01
    Generic[DecoratorOutput],
    Protocol,
):
    """
    Protocol that describes the methods of a decorator.

    Notes
    -----
    DecoratorOutput : TypeVar
        The output of the decorator.
    DecoratedFunctionParams : ParamSpec
        The parameters of the decorated function.
    DecoratorParams : ParamSpec
        The parameters of the decorator.
    """

    decorator_args: tuple  # type: ignore
    decorator_kwargs: dict  # type: ignore

    def __init__(
        self,
        *args: DecoratorParams.args,  # type: ignore
        **kwargs: DecoratorParams.kwargs,  # type: ignore
    ) -> None:
        """
        Initialize the decorator.

        Parameters
        ----------
        *args : DecoratorParams.args
            The arguments of the decorator.
        **kwargs : DecoratorParams.kwargs
            The keyword arguments of the decorator.
        """
        ...

    def __call__(
        self,
        *args: DecoratedFunctionParams.args,
        **kwargs: DecoratedFunctionParams.kwargs,
    ) -> Callable[DecoratedFunctionParams, DecoratorOutput]:
        """
        Call the decorator.

        Parameters
        ----------
        *args : DecoratedFunctionParams.args
            The arguments of the decorated function.
        **kwargs : DecoratedFunctionParams.kwargs
            The keyword arguments of the decorated function.

        Returns
        -------
        Callable[DecoratedFunctionParams, DecoratorOutput]
            The modified decorated function.
        """
        ...

    def decorator_function(
        self,
        decorated_function: Callable[DecoratedFunctionParams, FunctionOutput],
        function_args: tuple,  # type: ignore
        function_kwargs: dict,  # type: ignore
        decorator_args: tuple,  # type: ignore
        decorator_kwargs: dict,  # type: ignore
    ) -> DecoratorOutput:
        """
        Code your decorator here.

        Parameters
        ----------
        decorated_function : Callable[DecoratedFunctionParams, FunctionOutput]
            The function to be decorated.
        function_args : list
            The arguments of the decorated function.
        function_kwargs : dict
            The keyword arguments of the decorated function.
        decorator_args : list
            The arguments of the decorator.
        decorator_kwargs : dict
            The keyword arguments of the decorator.

        Returns
        -------
        DecoratorOutput
            The output of the decorator.
        """
        ...
