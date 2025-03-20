"""
Copyright (C) 2022-2025 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import functools
import typing as t
from functools import update_wrapper

import click
import typing_extensions as te
from click import get_current_context

from ..core.context import StellaNowContext
from ..services.service import StellaNowService

P = te.ParamSpec("P")
R = t.TypeVar("R")
T = t.TypeVar("T", bound=StellaNowService)
_AnyCallable = t.Callable[..., t.Any]


def option_with_config_lookup(
    param_name: str, service_class: t.Optional[t.Type[T]] = None, **option_kwargs
) -> t.Callable[[_AnyCallable], _AnyCallable]:
    def decorator(f):
        original_callback = option_kwargs.pop("callback", None)

        def callback(ctx, param, value):
            lookup_name = service_class if service_class else ctx.info_name
            stella_ctx: t.Optional[StellaNowContext] = ctx.find_object(StellaNowContext)

            if stella_ctx is None:
                raise click.ClickException(
                    f"{StellaNowContext.__class__.__name__} not found in the current Click context."
                )

            if value is None or ctx.get_parameter_source(param.name) == click.core.ParameterSource.DEFAULT:
                config_value = stella_ctx.get_config_value(lookup_name, param_name.replace("-", ""))
                value = config_value if config_value is not None else value

            if original_callback is not None:
                return original_callback(ctx, param, value)
            return value

        option_kwargs["callback"] = callback

        def default_value():
            ctx = click.get_current_context()
            lookup_service = service_class.service_name() if service_class else ctx.info_name
            stella_ctx: t.Optional[StellaNowContext] = ctx.find_object(StellaNowContext)

            if stella_ctx is None:
                raise click.ClickException(
                    f"{StellaNowContext.__class__.__name__} not found in the current Click context."
                )

            config_value = stella_ctx.get_config_value(lookup_service, param_name.replace("-", ""))
            if config_value is None:
                ctx.fail(f"Missing value for '{param_name}', provide configuration for Service: {lookup_service}")
            return config_value

        option_kwargs["default"] = functools.partial(default_value)
        option_kwargs["show_default"] = False

        return click.option(param_name, **option_kwargs)(f)

    return decorator


def prompt(param_name: str, **option_kwargs) -> t.Callable[[_AnyCallable], _AnyCallable]:
    """
    Creates a Click option decorator that automatically fetches its default value
    from the configuration, using a service name from ctx.obj.
    Additional keyword arguments are passed through to click.option().
    """

    def default_value():
        ctx = click.get_current_context()
        return ctx.obj.get_config_value(ctx.info_name, param_name.replace("-", ""))

    option_kwargs.setdefault("prompt", True)
    option_kwargs.setdefault("hidden", True)

    return click.option(param_name, default=default_value, **option_kwargs)


def make_stella_context_pass_decorator(
    object_type: t.Type[T],
) -> t.Callable[["t.Callable[te.Concatenate[T, P], R]"], "t.Callable[P, R]"]:
    def decorator(f: "t.Callable[te.Concatenate[T, P], R]") -> "t.Callable[P, R]":
        def new_func(*args: "P.args", **kwargs: "P.kwargs") -> "R":
            ctx = get_current_context()

            from ..core.context import StellaNowContext

            stella_ctx: t.Optional[StellaNowContext] = ctx.find_object(StellaNowContext)
            if stella_ctx is None:
                raise click.ClickException(
                    f"{StellaNowContext.__class__.__name__} not found in the current Click context."
                )

            obj: t.Optional[T]
            obj = stella_ctx.get_service(object_type)

            if obj is None:
                raise RuntimeError(
                    "Managed to invoke callback without a context"
                    f" object of type {object_type.__name__!r}"
                    " existing."
                )

            return ctx.invoke(f, obj, *args, **kwargs)

        return update_wrapper(new_func, f)

    return decorator  # type: ignore[return-value]
