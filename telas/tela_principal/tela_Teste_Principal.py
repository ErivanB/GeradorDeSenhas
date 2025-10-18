import tkinter as tk
from tkinter import ttk, messagebox


class MinhaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.configurar_janela()
        self.criar_componentes()

    def configurar_janela(self):
        self.root.title("GERADOR DE SENHAS SEGURAS")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

    def criar_componentes(self):
        # Criar um frame container
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Adicionar widgets aqui
        self.label = ttk.Label(frame, text="Bem-vindo!")
        self.label.pack(pady=10)

        self.botao = ttk.Button(frame, text="Clique", command=self.acao_botao)
        self.botao.pack(pady=5)

    def acao_botao(self):
        messagebox.showinfo("Mensagem", "Botão funcionando!")

    def executar(self):
        self.root.mainloop()


# Instanciar e executar
app = MinhaApp()
app.executar()