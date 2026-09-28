import tkinter as tk

root = tk.Tk()
root.title("Teste BRASIL CAMISAS")
root.geometry("600x400")

label = tk.Label(
    root,
    text="Tkinter funcionando!",
    font=("Arial", 24)
)
label.pack(pady=120)

root.mainloop()