# Se importa sistema

import sys

# Se importa gi como libreria base

import gi

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, Gio, GObject

# Se importa la clase de otra ventana

from dialog import ExampleDialog

# Clase base de la ventana de la aplicacion

class MainWindow(Gtk.ApplicationWindow):

    # Definicion de como va a ser la ventana

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Parametros base (Tamaño, Titulo)

        self.set_default_size(800, 250)

        self.set_title("Ejemplo")

        # Contenedores base. La orientacion VERTICAL es hacia la derecha 

        #mientras que la HORIZONTAL es hacia abajo

        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Coloca los contenedores en la ventana o dentro de los mismos

        self.set_child(self.box1)                                               # Box1 en la ventana

        self.box1.append(self.box2)                                             # Box2 en Box1

        self.box1.append(self.box3)                                             # Box3 en Box1

        # grid? pero esta en la box 3

        self.grid1 = Gtk.GridView()

        self.box3.append(self.grid1)

        # Se puden colocar textos en una regilla(grid) con el self label

        self.label = Gtk.Label()

        self.box3.append(self.label)                                            # Linea x1 y x2

        self.label1 = Gtk.Label()

        self.label1.set_text(" SOY UN TEXTO")

        self.box3.append(self.label1)

        self.label2 = Gtk.Label()

        self.label2.set_text("______________________")

        self.box3.append(self.label2)

        # Añadir Hello Button

        self.button_hello = Gtk.Button(label="Hola")                            # Ponerle nombre al boton

        self.button_hello.connect('clicked', self.hello)                        # Hace la funcion(hello)

        self.box2.append(self.button_hello)                                     # Se agrega Box2

        # Añadir Dialog Button

        self.button_dialog = Gtk.Button(label="Abrir Dialogo")

        self.button_dialog.connect('clicked', self.open_dialog)                 # Hace la funcion(abrir_dialog)

        self.box2.append(self.button_dialog)

        # Añadir Save Button

        self.button_save = Gtk.Button(label="Guardar")

        self.button_save.connect('clicked', self.save)                          # Hace la funcion(save)

        self.box2.append(self.button_save)

        

        # Añadir Open Button

        self.button_open = Gtk.Button(label="Abrir")

        self.button_open.connect('clicked', self.open)                          # Hace la funcion(abrir)

        self.box2.append(self.button_open)

        # Añadir un check-button

        self.check = Gtk.CheckButton(label="Chao")                              # Pone nombre al check-button

        self.box2.append(self.check)                                            # Se agrega al Box2

        # atributos para el guardado

        self._native1 = self.dialog_save()                                       # Hace la funcion(dialog guardado)

        self._native1.connect("response", self.on_file_save_response)            # Hace la funcion(guardando)

        # atributos para el abrido

        self._native2 = self.dialog_open()                                       # Hace la funcion(dialog abrido)

        self._native2.connect("response", self.on_file_open_response)            # Hace la funcion(abriendo)

        # Atributo de clase Dialog

        self.entrada_texto = None

    # Funcion(Hello)

    def hello(self, button):

        print("Hola Mundo!")

        self.label.set_text("Hola Mundo")

        # Si el check-button esta activado dice chao mundo y cierra el programa

        if self.check.get_active():

            print("Chao Mundo!")

            self.close()                                                        # Cierra la ventana

    # Funcion(abrir_dialog)

    def open_dialog(self, button):

        # abre el otro archivo y lo conecta con la funcion(respuesta)

        dialog = ExampleDialog(parent=self.get_root())                          # Busca la ruta para abrir dialog

        dialog.connect("response", self.on_dialog_response)                     # Envia la respuesta la a funcion

        dialog.set_visible(True)                                                # Hace visible la ventana

    # Funcion(respuesta)

    def on_dialog_response(self, dialog, response):

        # Si la respuesta es OK guarda y muestra el texto

        if response == Gtk.ResponseType.OK:

            print("Presionó OK")

            self.entrada_texto = dialog.entrada_texto.get_text()                # Traspaso de variable

            self.label.set_text(dialog.entrada_texto.get_text())                # coloca en el label el texto

        # Si la respuesta es CANCEL no hace nada

        elif response == Gtk.ResponseType.CANCEL:

            print("Presionó Cancelar")

        dialog.close()                                                          # Cierra el dialog

    # Funcion(save)

    def save(self, button):

        self._native1.show()                                                     # Muestra la instancia para guardar

    # Funcion(Dialog guardar)

    def dialog_save(self): 

        # Abre un dialog para guardar un archivo

        return Gtk.FileChooserNative(title="Save File",

                                    # "self.main_window" is defined elsewhere as a Gtk.Window

                                    #transient_for=self.main_window,

                                    action=Gtk.FileChooserAction.SAVE,

                                    accept_label="_Save",

                                    cancel_label="_Cancel",

                                    )

    # Funcion(guardando)

    def on_file_save_response(self, native, response):

        # Conecta la respuesta del dialog para guadar el texto

        # Si la respuesta es "ACCEPT" guardara el archivo

        if response == Gtk.ResponseType.ACCEPT:

            _path = native.get_file().get_path()

            print(_path)

            with open(_path, "w") as _file:

                _file.write(f'{self.entrada_texto} - {self.label.get_text()}\n')# El formato en que se guardara

        #self._native1 = None                                                   # Hace que no se vuelva a repetir

    # Funcion(Abrir)

    def open(self, button):

        self._native2.show()

    # Funcion(Dialog abrido)

    def dialog_open(self): 

        # Abre un dialog para abrir un archivo

        return Gtk.FileChooserNative(title="Open File",

                                    # "self.main_window" is defined elsewhere as a Gtk.Window

                                    #transient_for=self.main_window,

                                    action=Gtk.FileChooserAction.OPEN,

                                    accept_label="_Open",

                                    cancel_label="_Cancel",

                                    )

    # Fucnion(abriendo)

    def on_file_open_response(self, native, response):

        # Abre el archivo y lo lee dejandolo en el label

        # Si la respuesta es "ACCEPT" abrira el archivo

        if response == Gtk.ResponseType.ACCEPT:

            _path = native.get_file().get_path()

            print(_path)

            with open(_path) as _file:

                for i in _file.readlines():

                    print(i)

                    self.label.set_text(i)

                    break

        #self._native2 = None                                                   # Hace que no se vuelva a repetir

class MyApp(Gtk.Application):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.connect('activate', self.on_activate)

    def on_activate(self, app):

        self.win = MainWindow(application=app)

        self.win.present()

app = MyApp(application_id="com.example.GtkApplication")

app.run(sys.argv)
