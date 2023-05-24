# Import general
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GObject

# Esta clase es de tipo dialogo, por lo que funciona parecido, no igual a la de
#window, suando sus propios metodos
class ExampleDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Dialog", transient_for=parent)
        self.add_buttons(                                                       # Añade los buttons de abajo
            "_OK",                                                              # Texto que lleva
            Gtk.ResponseType.OK,                                                # Tipo de repuesta
            "_Cancel",
            Gtk.ResponseType.CANCEL,
        )
        box = self.get_content_area()                                           # Agrega Button
        box.append(Gtk.Button(label="HOLA"))
        self.entrada_texto = Gtk.Entry()                                        # Agrega entrada de texto
        box.append(self.entrada_texto)
