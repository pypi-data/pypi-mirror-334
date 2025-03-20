"""Module managing the create directory dialog"""
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
from ubiquitysoftware.tktooltip import ToolTip

from .base import BaseDialog
from ...utils import LabelEnum


class CreateDirectory(BaseDialog):
    """Class for the creat directory dialog"""
    def __init__(self, parent, title=""):
        self.result = None
        self.entry = None
        super().__init__(parent, title)

    def _event_setup(self):
        pass

    def _ui_setup(self):
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.pack()
        self.resizable(False, False)

        self.entry = ttk.Entry(mainframe)
        self.entry.grid(column=0, row=0, columnspan=3, sticky=EW)
        self.entry.focus_set()
        ToolTip(self.entry, msg=LabelEnum.TIP_NEW_FOLDER.value)

        ttk.Button(mainframe, text=LabelEnum.OK.value, command=self.confirm).grid(column=0, row=1, sticky=EW)
        ttk.Button(mainframe, text=LabelEnum.CANCEL.value, command=self.cancel).grid(column=1, row=1, sticky=EW)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def confirm(self):
        """Method to choice yes and quit the dialog"""
        self.result = self.entry.get().strip()
        self.dismiss()

    def cancel(self):
        """Method to choice no and quit the dialog"""
        self.dismiss()
