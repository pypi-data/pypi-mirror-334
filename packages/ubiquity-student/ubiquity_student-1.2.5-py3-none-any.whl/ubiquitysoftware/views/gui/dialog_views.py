"""Module managing the dialogs windows"""
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

from .dialogs import ConfirmDialog, MessageDialog
from ..utils import LabelEnum, ConsoleColor


def ask_for_download(parent, message: str) -> ConfirmDialog:
    """
    Display a confirmation dialog to ask the user if they want to download the file.

    Args:
        message (str): Message asking for confirmation to download the file.

    Returns:
        DownloadDialog: Instance of the confirmation dialog box.
    """
    return ConfirmDialog(parent, title=LabelEnum.DOWNLOAD.value, message=message)

def information_message(parent, message: str, color: ConsoleColor=ConsoleColor.RESET) -> None:
    """
    Display an information message

    Args:
        message (str): information message
        color (ConsoleColor): color message
    """
    MessageDialog(parent, title=LabelEnum.INFORMATION_DISPLAY.value, message=message, color=color)
