"""Module managing the message dialog"""
#      ubiquity
#      Copyright (C) 2023  INSA Rouen Normandie - CIP
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from tkinter import ttk
from tkinter.constants import EW
from .base import BaseDialog
from ...utils import ConsoleColor, gettext
_ = gettext.gettext


class MessageDialog(BaseDialog):
    """Class for the choice dialog"""
    def __init__(self, parent, title="", message="", color=ConsoleColor.RESET):
        self.message = message
        self.msg_type = color
        super().__init__(parent, title)

    def _event_setup(self):
        pass

    def _ui_setup(self):
        style = ttk.Style(self)
        type_message = ""
        if self.msg_type == ConsoleColor.SUCCESS:
            type_message = _("Success")
            style.configure("Success.TLabel", foreground="black", background="lightgreen")
        elif self.msg_type == ConsoleColor.WARNING:
            type_message = _("Warning")
            style.configure("Warning.TLabel", foreground="black", background="yellow")
        elif self.msg_type == ConsoleColor.ERROR:
            type_message = _("Error")
            style.configure("Error.TLabel", foreground="black", background="lightcoral")

        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.pack()
        self.resizable(False, False)

        if type_message:
            type_label = ttk.Label(mainframe, text=type_message + " !",
                                style=f"{self.msg_type.name.capitalize()}.TLabel")
            type_label.grid(column=0, row=0, sticky=EW)
        label = ttk.Label(mainframe, text=self.message)
        label.grid(column=1, row=1, sticky=EW)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.after(3000, self.dismiss)
