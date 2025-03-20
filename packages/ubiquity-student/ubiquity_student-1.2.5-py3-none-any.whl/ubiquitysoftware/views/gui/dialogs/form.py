
"""Module managing the form dialog"""
#      ubiquity
#      Copyright (C) 2022  INSA Rouen Normandie - CIP
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

import os
from tkinter import ttk, filedialog, messagebox, PhotoImage
from tkinter.constants import W, EW
from ubiquitysoftware.tktooltip import ToolTip

from .base import BaseDialog
from .create_directory import CreateDirectory
from ...utils import LabelEnum, ErrorMessage, gettext

_ = gettext.gettext


class FormDialog(BaseDialog):
    """Class for the form dialog"""
    def __init__(self, parent):
        self.parent = parent
        self.parent.model.error.set('')
        super().__init__(parent, LabelEnum.NEW.value)


    def _event_setup(self):
        self.bind("<Return>", self.access)

    def _ui_setup(self):
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.pack()
        self.resizable(False, False)

        # Create Entries
        server_entry = ttk.Entry(mainframe, width=50, textvariable=self._model.server)
        server_entry.grid(column=2, row=1, sticky=EW)
        server_entry.focus()
        ToolTip(server_entry, msg=LabelEnum.TIP_SERVER_URL.value)

        student_key = ttk.Entry(mainframe, textvariable=self._model.student_key)
        student_key.grid(column=2, row=2, sticky=EW)
        ToolTip(student_key, msg=LabelEnum.TIP_PERSONAL_KEY.value)

        group_key = ttk.Entry(mainframe, textvariable=self._model.group_key)
        group_key.grid(column=2, row=3, sticky=EW)
        ToolTip(group_key, msg=LabelEnum.TIP_GROUP_KEY.value)

        # Create labels
        ttk.Label(mainframe, textvariable=self._model.error, foreground='#F00').grid(column=1, columnspan=3, row=0)
        ttk.Label(mainframe, text=LabelEnum.SERVER.value).grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text=LabelEnum.STUDENT_KEY.value).grid(column=1, row=2, sticky=W)
        ttk.Label(mainframe, text=LabelEnum.GROUP_KEY.value).grid(column=1, row=3, sticky=W)
        ttk.Label(mainframe, text=LabelEnum.DIRECTORY.value).grid(column=1, row=4, sticky=W)

        # Frame for Directory Selection
        directory_frame = ttk.LabelFrame(mainframe, text=LabelEnum.DIRECTORY.value)
        directory_frame.grid(column=1, row=4, columnspan=3, sticky=EW, padx=5, pady=5)

        self._model.directory.set(os.getcwd())
        directory = ttk.Entry(directory_frame, textvariable=self._model.directory, width=50)
        directory.grid(column=1, row=0, sticky=EW, padx=5, pady=5)
        ToolTip(directory, msg=LabelEnum.TIP_DESTINATION_DIRECTORY.value)

        # Create icons
        icon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        new_folder_icon = PhotoImage(file=os.path.join(icon_path, "images/search_icn.png")).subsample(20, 20)
        btn_search = ttk.Button(directory_frame, image=new_folder_icon, command=self.search)
        btn_search.grid(column=2, row=0, sticky=EW, padx=5)
        btn_search.image = new_folder_icon
        ToolTip(btn_search, msg=LabelEnum.TIP_SEARCH_DIRECTORY.value)

        new_folder_icon = PhotoImage(file=os.path.join(icon_path, "images/add_folder_icn.png")).subsample(20, 20)
        btn_create = ttk.Button(directory_frame, image=new_folder_icon, command=self.create_directory)
        btn_create.grid(column=3, row=0, sticky=EW, padx=5)
        btn_create.image = new_folder_icon
        ToolTip(btn_create, msg=LabelEnum.TIP_CREATE_DIRECTORY.value)

        # Create buttons
        btn_connection = ttk.Button(mainframe, text=LabelEnum.CONNECTION.value, command=self.access)
        btn_connection.grid(column=1, row=5, sticky=EW, columnspan=3, pady=20, padx=20)
        ToolTip(btn_connection, msg=LabelEnum.TIP_UPDATE_FILES.value)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def search(self):
        """Method searching a directory"""
        dir_name = filedialog.askdirectory(parent=self)
        if dir_name:
            self._model.directory.set(dir_name)

    def _is_valid(self):
        """Method verifying the form is valid

        :return: True if the values are valid, False if not
        """
        if '' in [self._model.server.get(), self._model.student_key.get(), self._model.group_key.get(),
                  self._model.directory.get()]:
            self._model.error.set(ErrorMessage.EMPTY_FIELD.value)
            return False
        return True

    def access(self, *_):
        """Method accessing and run if the values are valid"""
        self._model.error.set('')
        if self._is_valid():
            self.is_valid = self.parent.submit()
            if self.is_valid:
                self.dismiss()

    def create_directory(self):
        """Creates a new folder in the selected directory.  
        Prompts the user to enter a folder name and creates it within the current directory.  
        If successful, updates the directory path in the model.  
        Displays an error message if the folder cannot be created.
        """
        new_folder_name = CreateDirectory(self.parent, f"{LabelEnum.NEW.value} {LabelEnum.DIRECTORY.value}").result
        if new_folder_name:
            new_folder_path = os.path.join(self._model.directory.get(), new_folder_name)
            try:
                os.makedirs(new_folder_path)
                self._model.directory.set(new_folder_path)
            except Exception as e:
                messagebox.showerror(LabelEnum.ERROR, f"{LabelEnum.UNABLE_FOLDER.value} : {e}")
