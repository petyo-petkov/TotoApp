from tkinter import messagebox
import customtkinter
import db
from addBoleto import AddBoleto
from deleteBoleto import Delete

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


def mostrar_boletos(n):
    global campos_boletos, campo_boleto
    cursor = db.toto.find({}, {'Combinaciones': False,
                               '_id': False,
                               'Reintegro': False,
                               'Fecha millon': False,
                               'Numero millon': False})
    for i in cursor:
        numero = str(i['Numero de serie'])
        tipo = str(i['Tipo'])
        fecha = str(i['Fecha'])
        precio = str(i['Precio'])
        result = f'{numero[-10:]}      |      {tipo}      |      {fecha}      |      {precio} \N{euro sign}'

        campos_boletos = []
        campo_boleto = customtkinter.CTkTextbox(scroll_boletos, height=10, width=450, activate_scrollbars=False,
                                                font=("Roboto", 13))
        campo_boleto.insert("0.0", result)
        campo_boleto.grid(pady=2)
        campos_boletos.append(campo_boleto)
    if n == 1:
        for elemento in scroll_boletos.grid_slaves():
            elemento.grid_forget()


def insert_boletos():
    AddBoleto.captura_qr()
    AddBoleto.sum_precios()
    refresh()


def cancel():
    yes = messagebox.askyesno("Cancelar", "Salir ?")
    if yes:
        quit()


def refresh():
    mostrar_boletos(1)
    mostrar_boletos(0)
    textbox_gastado.delete("0.0", "end")
    textbox_gastado.insert(customtkinter.END,
                           f'{db.gastos.distinct("gastado")} \N{euro sign}'.replace('[', '').replace(']', ''))


def delete_all():
    yes = messagebox.askyesno("Delete", "Borrar todo ?")
    if yes:
        Delete.deleteAll()
        Delete.deleteGastado()
        # refresh()


# config. windows
root = customtkinter.CTk()
root.title("LotoApp")
root.geometry("680x420")
root.resizable(width=False, height=False)

# config. grid 3x4
root.grid_columnconfigure((0, 1, 2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=0)

# config. side_frame
side_frame = customtkinter.CTkFrame(root, width=200, height=340, fg_color="#F7DC6F")
side_frame.grid(row=0, column=0, rowspan=2, padx=(10, 5), pady=10, sticky="nsew")
side_frame.grid_rowconfigure(3, weight=1)

# textbox ganado-gastado
textbox_gastado = customtkinter.CTkTextbox(side_frame, width=150, height=20, activate_scrollbars=False)
textbox_gastado.grid(row=1, column=0, padx=10, pady=(0, 20))
textbox_gastado.insert(customtkinter.END,
                       f'{db.gastos.distinct("gastado")} \N{euro sign}'.replace('[', '').replace(']', ''))
gastado_label = customtkinter.CTkLabel(side_frame, text="GASTADO", text_color="#17202A")
gastado_label.grid(row=0, column=0)

textbox_ganado = customtkinter.CTkTextbox(side_frame, width=150, height=20, activate_scrollbars=False)
textbox_ganado.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="n")
ganado_label = customtkinter.CTkLabel(side_frame, text="GANADO", text_color="#17202A")
ganado_label.grid(row=2, column=0)

# scrollable_frame boletos
scroll_boletos = customtkinter.CTkScrollableFrame(root, width=460, height=290, label_anchor="w",
                                                  label_fg_color="#F7DC6F", label_text_color="black",
                                                  label_text="NUMERO DE SERIE        |        TIPO        |       "
                                                             "FECHA       |       PRECIO")

scroll_boletos.grid(row=0, column=1, columnspan=3, padx=5, pady=10, sticky="nsew")
mostrar_boletos(0)

# botones
button_new = customtkinter.CTkButton(root, width=100, height=30, text="NUEVO", text_color="#17202A",
                                     fg_color="#27AE60", hover_color="#229954", command=refresh)
button_new.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

button_add = customtkinter.CTkButton(root, width=100, height=30, text="AÑADIR", text_color="#17202A",
                                     fg_color="#27AE60", hover_color="#229954", command=insert_boletos)
button_add.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

button_borrar = customtkinter.CTkButton(root, width=100, height=30, text="BORRAR", text_color="#17202A",
                                        fg_color="#E74C3C", hover_color="#FE1800", command=delete_all)
button_borrar.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
button_cancelar = customtkinter.CTkButton(root, width=100, height=30, text="CANCELAR",
                                          text_color="#17202A", fg_color="#F4D03F", hover_color="#F1C40F",
                                          command=cancel)

button_cancelar.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

root.mainloop()
