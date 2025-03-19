"""Custom tkinter messagebox."""
import tkinter as tk
from tkinter import ttk
from tkinter import font
from pathlib import Path
from PIL import ImageTk, Image

from psiutils.constants import PAD

import text

icons = {
    'info': 'icon-info.png',
    'error': 'icon-error.png',
}

icon_text = {
    'info': 'Info:',
    'error': 'Error!!!',
}


class MessageBox():
    def __init__(
            self,
            title: str = '',
            message: str = '',
            parent: tk.Tk = None,
            icon: str = 'info',
            ) -> None:
        self.root = tk.Toplevel(parent)
        self.title = title
        self.parent = parent
        self.icon = icon

        # tk variables
        self.message_text = tk.StringVar(value=message)

        # self.show()

    def show(self) -> None:
        root = self.root
        root.transient(self.parent)
        root.title(self.title)

        root.bind('<Control-o>', self._dismiss)

        if isinstance(self.icon, str):
            path = Path(Path(__file__).parent, 'images', icons[self.icon])
            try:
                self.icon_image = ImageTk.PhotoImage(Image.open(path))
            except FileNotFoundError:
                pass
        else:
            self.icon_image = self.icon

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        frame.columnconfigure(1, weight=1)

        try:
            label = tk.Label(frame, image=self.icon_image)
        except AttributeError:
            label = tk.Label(
                frame, text=icon_text[self.icon],
                font=(font.nametofont('TkDefaultFont'), 12, 'bold'))
        label.grid(row=0, column=0)

        label = ttk.Label(
            frame,
            textvariable=self.message_text,
            font=(font.nametofont('TkDefaultFont'), 12, 'bold')
            )
        label.grid(row=0, column=1, sticky=tk.NSEW, padx=PAD, pady=PAD)

        button_frame = self._button_frame(frame)
        button_frame.grid(row=1, column=0, columnspan=2,
                          sticky=tk.EW, padx=PAD, pady=PAD)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ttk.Frame(master)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        button = ttk.Button(
                frame,
                text=text.OK,
                command=self._dismiss,
                underline=0,
                )
        button.grid(row=0, column=0)
        return frame

    def _process(self, *args) -> None:
        ...

    def _dismiss(self, *args) -> None:
        self.root.destroy()


def showinfo(
        title: str = '',
        message: str = '',
        parent: tk.Tk = None,
        icon: str = 'info',
        ) -> None:

    messagebox = MessageBox(
        title=title,
        message=message,
        parent=parent,
        icon=icon,
        )

    messagebox.show()
    parent.wait_window(messagebox.parent)


def showerror(
        title: str = '',
        message: str = '',
        parent: tk.Tk = None,
        icon: str = 'error',
        ) -> None:

    messagebox = MessageBox(
        title=title,
        message=message,
        parent=parent,
        icon=icon,
        )

    messagebox.show()
    parent.wait_window(messagebox.parent)
