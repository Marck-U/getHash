import tkinter as tk
import os
import hashlib

class DragAndDropFile(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=700, height=400, bg="#F7F7F7")
        self.canvas.pack(fill='both', expand=True)

        # Establecemos los eventos para el arrastre del archivo
        self.label = tk.Label(self, text="Presiona en la ventana para añadir el hash al archivo.", bg="#F7F7F7", fg="black", font=("Garamond", 18))
        self.canvas.create_window(90, 0, anchor='nw', window=self.label)
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.dragging)
        self.canvas.bind("<ButtonRelease-1>", self.drop)

    def start_drag(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def dragging(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def drop(self, event):
        ruta = self.master.tk.splitlist(self.canvas.tk.call('tk_getOpenFile', '-multiple', 'true', '-filetypes', '{{All files} {*}}'))
        if ruta:
            self.archivo_arrastrado = True
            md5 = obtenerHash(ruta[0])
            nombre_completo = os.path.basename(ruta[0])
            nombre, extension = os.path.splitext(nombre_completo)
            nuevo_nombre = nombre + '_' + md5 + extension
            os.rename(ruta[0], nuevo_nombre)
            self.label = tk.Label(self, text=f"El hash es :\n{nuevo_nombre}.", bg="#F7F7F7", fg="red", font=("Garamond", 12, "bold"))
            self.canvas.create_window(90, 110, anchor='nw', window=self.label)
        else:
            self.label = tk.Label(self, text="Presiona en la ventana para añadir el hash al archivo.", bg="#F7F7F7", fg="red", font=("Garamond", 12, "bold"))
            self.canvas.create_window(14, 0, anchor='nw', window=self.label)
            self.archivo_arrastrado = False

def obtenerHash(ruta):
    with open(ruta, 'rb') as f:
        md5 = hashlib.md5(f.read())
        return md5.hexdigest()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Get_Hash")
    root.geometry("700x400+{}+{}".format(int(root.winfo_screenwidth()/2 - 700/2), int(root.winfo_screenheight()/2 - 400/2)))
    app = DragAndDropFile(root)
    app.pack(fill='both', expand=True)
    root.mainloop()
