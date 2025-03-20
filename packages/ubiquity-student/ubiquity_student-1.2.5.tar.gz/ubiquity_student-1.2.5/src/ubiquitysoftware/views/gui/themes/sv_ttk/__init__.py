"""Module for the sv_ttk theme"""
from pathlib import Path

inited = False
root = None


def init(func):
    """
    Decorator to initialize the Tkinter theme before executing the decorated function.

    This ensures that the theme is loaded only once and Tkinter is initialized before 
    applying the theme. If the theme has already been initialized, the decorated function 
    is simply executed.

    Args:
        func (callable): The function to decorate.

    Returns:
        callable: The wrapped function with initialization.
    """
    def wrapper(*args, **kwargs):
        global inited
        global root

        if not inited:
            from tkinter import _default_root

            path = (Path(__file__).parent / "sun-valley.tcl").resolve()

            try:
                _default_root.tk.call("source", str(path))
            except AttributeError:
                raise RuntimeError(
                    "can't set theme. Tk is not initialized. "
                    + "Please first create a tkinter.Tk instance, then set the theme."
                ) from None
            else:
                inited = True
                root = _default_root

        return func(*args, **kwargs)

    return wrapper


@init
def set_theme(theme):
    """
    Sets the theme for the Tkinter application.

    This function applies either a "dark" or "light" theme to the Tkinter root widget. 
    If an invalid theme is provided, a RuntimeError is raised.

    Args:
        theme (str): The name of the theme to apply. Should be either "dark" or "light".

    Raises:
        RuntimeError: If an invalid theme name is provided.
    """
    if theme not in {"dark", "light"}:
        raise RuntimeError(f"not a valid theme name: {theme}")

    root.tk.call("set_theme", theme)


@init
def get_theme():
    """
    Retrieves the current theme being used in the Tkinter application.

    This function checks which theme is currently applied (either "dark" or "light") 
    and returns the corresponding value. If the theme is not recognized, it returns the 
    raw theme name.

    Returns:
        str: The current theme, either "dark" or "light", or the raw theme name if unrecognized.
    """
    theme = root.tk.call("ttk::style", "theme", "use")

    try:
        return {"sun-valley-dark": "dark", "sun-valley-light": "light"}[theme]
    except KeyError:
        return theme


@init
def toggle_theme():
    """
    Toggles between the "dark" and "light" themes in the Tkinter application.

    This function checks the current theme and switches it to the opposite one: 
    from "dark" to "light" or from "light" to "dark".

    If the current theme is "dark", it will apply the light theme, and vice versa.
    """
    if get_theme() == "dark":
        use_light_theme()
    else:
        use_dark_theme()


use_dark_theme = lambda: set_theme("dark")
use_light_theme = lambda: set_theme("light")
