import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import csv
import os
from PIL import Image, ImageTk
from database import DatabaseManager
from empleado import Empleado

class SistemaEmpleadosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Sistema de Empleados - Edición Especial")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        # Obtener la ruta base del proyecto
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.base_path, "assets")
        
        # --- IMAGEN DE FONDO ---
        self.cargar_fondo()
        
        # Conexión a la base de datos
        self.db = DatabaseManager()
        
        # Variables de control
        self.nombre_var = tk.StringVar()
        self.sexo_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.buscar_var = tk.StringVar()

        # Variables para animación del GIF
        self.gif_frames = []
        self.gif_label = None
        self.gif_anim_id = None
        self.gif_playing = False
        
        self.crear_widgets()
        self.actualizar_lista_empleados()
        self._preload_gif_frames()
    
    def cargar_fondo(self):
        """Carga y coloca la imagen de fondo"""
        try:
            bg_path = os.path.join(self.assets_path, "background.png")
            print(f"📌 Buscando imagen en: {bg_path}")
            
            if os.path.exists(bg_path):
                bg_image = Image.open(bg_path)
                bg_image = bg_image.resize((900, 650), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                self.bg_label = tk.Label(self.root, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                print("✅ Imagen de fondo cargada correctamente")
            else:
                print(f"❌ No se encontró la imagen: {bg_path}")
                self.root.configure(bg='#2C3E50')
                
        except Exception as e:
            print(f"⚠️ Error cargando imagen de fondo: {e}")
            self.root.configure(bg='#2C3E50')

    def crear_widgets(self):
        """Crea todos los elementos de la interfaz directamente sobre el fondo"""
        
        # --- TÍTULO PRINCIPAL ---
        title_label = tk.Label(self.root, text="Sistema de Gestión de Empleados",
                              font=("Fixedsys", 20, "bold"), fg="white")
        title_label.place(relx=0.5, y=30, anchor=tk.CENTER)

        # --- SECCIÓN DE BÚSQUEDA ---
        search_frame = tk.Frame(self.root)  # ← Sin bg
        form_frame = tk.Frame(self.root) 

        tk.Label(search_frame, text="ID del Empleado:", 
                font=("Consolas", 12, "bold"), fg="white").pack(side=tk.LEFT)

        buscar_entry = tk.Entry(search_frame, textvariable=self.buscar_var, 
                               font=("Consolas", 11), bg="white", fg="black", 
                               relief="solid", bd=1, width=15)
        buscar_entry.pack(side=tk.LEFT, padx=5)

        self.crear_boton_pixel(search_frame, "Buscar", self.buscar_empleado, "#3498DB", "#2980B9").pack(side=tk.LEFT, padx=5)
        self.crear_boton_pixel(search_frame, "Limpiar", self.limpiar_busqueda, "#E67E22", "#D35400").pack(side=tk.LEFT, padx=5)

        # --- FORMULARIO --- (70px más abajo)
        form_frame = tk.Frame(self.root)
        form_frame.place(relx=0.5, y=150, anchor=tk.CENTER)

        fields = [
            ("Nombre:", self.nombre_var, 'entry'),
            ("Sexo:", self.sexo_var, 'combo'), 
            ("Correo:", self.correo_var, 'entry')
        ]

        for i, (label_text, var, field_type) in enumerate(fields):
            field_frame = tk.Frame(form_frame)
            field_frame.pack(fill=tk.X, pady=8)

            label = tk.Label(field_frame, text=label_text, font=("Consolas", 12, "bold"),
                          fg="white", width=12, anchor="e")
            label.pack(side=tk.LEFT, padx=(0, 10))

            if field_type == 'combo':
                entry = ttk.Combobox(field_frame, textvariable=var, 
                                   values=["M", "F", "Otro"], state="readonly", width=25)
            else:
                entry = tk.Entry(field_frame, textvariable=var, font=("Consolas", 11), 
                               bg="white", fg="black", relief="solid", bd=1, width=27)
            entry.pack(side=tk.LEFT)

        # --- BOTONES DEL FORMULARIO --- (40px más abajo)
        form_buttons_frame = tk.Frame(self.root)
        form_buttons_frame.place(relx=0.5, y=250, anchor=tk.CENTER)

        self.crear_boton_pixel(form_buttons_frame, "Agregar Empleado", self.agregar_empleado, "#27AE60", "#2ECC71").pack(side=tk.LEFT, padx=5)
        self.crear_boton_pixel(form_buttons_frame, "Limpiar Campos", self.limpiar_campos, "#E74C3C", "#C0392B").pack(side=tk.LEFT, padx=5)

        # --- LISTA DE EMPLEADOS --- (60px más abajo)
        list_title = tk.Label(self.root, text="Lista de Empleados", 
                             font=("Consolas", 14, "bold"), fg="white")
        list_title.place(relx=0.5, y=300, anchor=tk.CENTER)

        # Treeview con frame transparente
        tree_frame = tk.Frame(self.root,)
        tree_frame.place(relx=0.5, y=450, anchor=tk.CENTER, width=700, height=200)

        columns = ('ID', 'Nombre', 'Sexo', 'Correo')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)

        # Configurar estilo del treeview para que sea visible sobre el fondo
        style = ttk.Style()
        style.configure("Treeview", background="white", fieldbackground="white", foreground="black")
        style.configure("Treeview.Heading", background="#34495E", foreground="white")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)

        self.tree.column('Nombre', width=200)
        self.tree.column('Correo', width=180)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botón eliminar (40px más abajo)
        delete_frame = tk.Frame(self.root)
        delete_frame.place(relx=0.5, y=550, anchor=tk.CENTER)

        self.crear_boton_pixel(delete_frame, "❌ Eliminar Empleado Seleccionado", 
                              self.eliminar_empleado, '#C0392B', '#A93226').pack()

        self.tree.bind('<Double-1>', self.editar_empleado_seleccionado)

        # --- BOTONES ESPECIALES --- (en la parte inferior)
        special_frame = tk.Frame(self.root, )
        special_frame.place(relx=0.5, y=600, anchor=tk.CENTER)

        # Botones especiales en línea
        self.crear_boton_pixel(special_frame, "🕵️ Hackear Base de Datos", 
                              self.exportar_csv, '#9B59B6', '#8E44AD').pack(side=tk.LEFT, padx=5)

        self.crear_boton_pixel(special_frame, "💡 Mensaje Interesante", 
                              self.toggle_gif_display, '#F1C40F', '#F39C12').pack(side=tk.LEFT, padx=5)

        # Frame especial para el botón cerrar que se mueve
        self.cerrar_container = tk.Frame(self.root, width=100, height=50)
        self.cerrar_container.place(x=750, y=590)  # Esquina inferior derecha
        self.cerrar_container.pack_propagate(False)

        self.boton_escapista = self.crear_boton_pixel(self.cerrar_container, "❌ Cerrar", 
                                                     self.cerrar_aplicacion, 
                                                     '#E74C3C', '#CB4335')
        self.boton_escapista.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Contenedor para el GIF (junto al botón de mensaje interesante)
        self.gif_container = tk.Frame(self.root, width=200, height=120)
        self.gif_container.place(x=650, y=500)  # Posición cerca del botón
        self.gif_container.pack_propagate(False)

        # Seguimiento del mouse para el botón cerrar
        self.boton_escapista.bind("<Enter>", self.evitar_cierre)

    def crear_boton_pixel(self, parent, texto, comando, color_normal, color_hover):
        """Crea un botón con estilo pixel art"""
        btn = tk.Button(parent, 
                       text=texto,
                       command=comando,
                       font=("Fixedsys", 9, "bold"),
                       bg=color_normal,
                       fg="white",
                       padx=12,
                       pady=6,
                       relief="raised",
                       borderwidth=3,
                       cursor="hand2")
        
        # Efectos hover
        def on_enter(e):
            btn.config(bg=color_hover, relief="sunken", borderwidth=4)
        
        def on_leave(e):
            btn.config(bg=color_normal, relief="raised", borderwidth=3)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def evitar_cierre(self, event):
        """Hace que el botón Cerrar se mueva cuando el mouse se acerca"""
        try:
            # Mover dentro del contenedor del botón cerrar
            max_x = self.cerrar_container.winfo_width() - self.boton_escapista.winfo_width()
            max_y = self.cerrar_container.winfo_height() - self.boton_escapista.winfo_height()
            
            if max_x > 0 and max_y > 0:
                new_x = random.randint(0, max_x)
                new_y = random.randint(0, max_y)
                self.boton_escapista.place(x=new_x, y=new_y)
        except Exception as e:
            print(f"Error moviendo botón: {e}")

    # --- FUNCIONALIDADES GIF ---
    def _preload_gif_frames(self):
        """Carga los frames del GIF en memoria"""
        self.gif_frames = []
        gif_path = os.path.join(self.assets_path, "hola_mundo.gif")
        
        if not os.path.exists(gif_path):
            print(f"❌ No se encontró el GIF: {gif_path}")
            # Crear GIF de fallback con texto animado
            self.crear_gif_fallback()
            return
            
        try:
            gif = Image.open(gif_path)
            try:
                while True:
                    frame = gif.copy().convert("RGBA")
                    frame = frame.resize((180, 100), Image.Resampling.LANCZOS)
                    self.gif_frames.append(ImageTk.PhotoImage(frame))
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass
            print(f"✅ GIF precargado: {len(self.gif_frames)} frames")
        except Exception as e:
            print(f"Error precargando GIF: {e}")
            self.crear_gif_fallback()

    def crear_gif_fallback(self):
        """Crea frames de fallback si no hay GIF"""
        try:
            # Crear frames simples con texto animado
            textos = ["¡HOLA!", "MUNDO", "🌍", "🌟", "🎉"]
            for i, texto in enumerate(textos):
                # Crear imagen simple con texto
                img = Image.new('RGBA', (180, 100), (0, 0, 0, 0))
                # Aquí podrías usar PIL para dibujar texto, pero por simplicidad usamos label
                self.gif_frames.append(None)  # Placeholder
            print("✅ GIF de fallback creado")
        except Exception as e:
            print(f"Error creando fallback: {e}")

    def toggle_gif_display(self):
        """Muestra u oculta el GIF"""
        if self.gif_playing:
            self._stop_gif()
        else:
            self._show_gif()

    def _show_gif(self):
        """Muestra el GIF animado"""
        # Limpiar contenedor primero
        for widget in self.gif_container.winfo_children():
            widget.destroy()

        if not self.gif_frames or self.gif_frames[0] is None:
            # Mostrar texto animado como fallback
            self.mostrar_texto_animado()
            return

        self.gif_label = tk.Label(self.gif_container)
        self.gif_label.pack(expand=True)
        self.gif_playing = True
        self._animate_gif(0)

    def mostrar_texto_animado(self):
        """Muestra texto animado como fallback cuando no hay GIF"""
        textos = ["¡HOLA!", "MUNDO", "🌍", "🌟", "🎉"]
        self.gif_label = tk.Label(self.gif_container, text=textos[0], 
                                 font=("Arial", 16, "bold"), fg="white")
        self.gif_label.pack(expand=True)
        self.gif_playing = True
        
        def animar_texto(index=0):
            if self.gif_playing and self.gif_label:
                self.gif_label.config(text=textos[index])
                next_index = (index + 1) % len(textos)
                self.root.after(500, animar_texto, next_index)
        
        animar_texto()

    def _animate_gif(self, index):
        if not self.gif_playing or not self.gif_frames:
            return
            
        frame = self.gif_frames[index]
        if self.gif_label and frame:
            self.gif_label.config(image=frame)
            self.gif_label.image = frame

        next_index = (index + 1) % len(self.gif_frames)
        self.gif_anim_id = self.root.after(100, self._animate_gif, next_index)

    def _stop_gif(self):
        """Detiene la animación del GIF"""
        try:
            if self.gif_anim_id:
                self.root.after_cancel(self.gif_anim_id)
                self.gif_anim_id = None
        except Exception:
            pass
            
        if self.gif_label:
            try:
                self.gif_label.destroy()
            except Exception:
                pass
            self.gif_label = None
            
        self.gif_playing = False

    def exportar_csv(self):
        """Exporta todos los registros a un archivo CSV"""
        try:
            empleados = self.db.obtener_empleados()
            
            if not empleados:
                messagebox.showinfo("Info", "No hay datos para exportar")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar archivo CSV"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['ID', 'Nombre', 'Sexo', 'Correo'])
                    
                    for empleado in empleados:
                        writer.writerow([
                            empleado.id_empleado,
                            empleado.nombre,
                            empleado.sexo,
                            empleado.correo
                        ])
                
                messagebox.showinfo("✅ Éxito", 
                                  f"¡Datos exportados exitosamente!\n"
                                  f"Archivo: {filename}\n"
                                  f"Registros: {len(empleados)}")
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo exportar: {e}")

    def cerrar_aplicacion(self):
        """Cierra la aplicación"""
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
            self._stop_gif()
            self.db.cerrar_conexion()
            self.root.quit()

    # --- MÉTODOS DE LA BASE DE DATOS ---
    def actualizar_lista_empleados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        empleados = self.db.obtener_empleados()
        for empleado in empleados:
            self.tree.insert('', tk.END, values=(
                empleado.id_empleado,
                empleado.nombre,
                empleado.sexo,
                empleado.correo
            ))

    def agregar_empleado(self):
        nombre = self.nombre_var.get().strip()
        sexo = self.sexo_var.get()
        correo = self.correo_var.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        if not sexo:
            messagebox.showerror("Error", "El sexo es obligatorio")
            return
        
        if not correo or '@' not in correo:
            messagebox.showerror("Error", "El correo electrónico no es válido")
            return
        
        nuevo_empleado = Empleado(nombre=nombre, sexo=sexo, correo=correo)
        empleado_id = self.db.agregar_empleado(nuevo_empleado)
        
        if empleado_id:
            messagebox.showinfo("Éxito", f"Empleado agregado correctamente\nID generado: {empleado_id}")
            self.limpiar_campos()
            self.actualizar_lista_empleados()
        else:
            messagebox.showerror("Error", "No se pudo agregar el empleado. Verifique que el correo no exista.")

    def eliminar_empleado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar")
            return
        
        item = seleccion[0]
        empleado_id = self.tree.item(item, 'values')[0]
        
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Está seguro de que desea eliminar al empleado con ID {empleado_id}?"
        )
        
        if confirmar:
            if self.db.eliminar_empleado(empleado_id):
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
                self.actualizar_lista_empleados()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el empleado")

    def buscar_empleado(self):
        id_buscar = self.buscar_var.get().strip()
        if not id_buscar:
            messagebox.showwarning("Advertencia", "Ingrese un ID para buscar")
            return
        
        try:
            empleado_id = int(id_buscar)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número válido")
            return
        
        empleado = self.db.buscar_empleado_por_id(empleado_id)
        
        if empleado:
            for item in self.tree.get_children():
                if self.tree.item(item, 'values')[0] == empleado_id:
                    self.tree.selection_set(item)
                    self.tree.focus(item)
                    self.tree.see(item)
                    break
            messagebox.showinfo("Empleado Encontrado", str(empleado))
        else:
            messagebox.showinfo("No Encontrado", f"No se encontró ningún empleado con ID {empleado_id}")

    def editar_empleado_seleccionado(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        
        item = seleccion[0]
        empleado_id = self.tree.item(item, 'values')[0]
        empleado = self.db.buscar_empleado_por_id(empleado_id)
        if empleado:
            messagebox.showinfo("Edición", f"Funcionalidad de edición para:\n{empleado}")

    def limpiar_campos(self):
        self.nombre_var.set("")
        self.sexo_var.set("")
        self.correo_var.set("")

    def limpiar_busqueda(self):
        self.buscar_var.set("")
        self.actualizar_lista_empleados()

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.cerrar_conexion()