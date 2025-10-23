import tkinter as tk
from tkinter import messagebox
import random
import string


# --- Funções de Lógica ---

def gerar_senha():
    """Gera a senha com base nas opções selecionadas e no tamanho."""
    try:
        # Pega o tamanho da senha
        tamanho = int(entrada_tamanho.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido para o tamanho.")
        senha_gerada.set("")
        return

    if tamanho <= 0:
        messagebox.showerror("Erro", "O tamanho da senha deve ser maior que zero.")
        senha_gerada.set("")
        return

    # Define os conjuntos de caracteres com base nos checkboxes
    caracteres = ''

    if var_maiuscula.get():
        caracteres += string.ascii_uppercase

    if var_minuscula.get():
        caracteres += string.ascii_lowercase

    if var_numeros.get():
        caracteres += string.digits

    if var_especiais.get():
        caracteres += string.punctuation

    # Verifica se algum checkbox foi selecionado
    if not caracteres:
        messagebox.showwarning("Aviso", "Selecione pelo menos um tipo de caractere.")
        senha_gerada.set("")
        return

    # Gera a senha
    # random.choices é mais eficiente para esta tarefa
    senha = ''.join(random.choices(caracteres, k=tamanho))

    # Exibe a senha gerada no campo Entry
    senha_gerada.set(senha)


def copiar_senha():
    """Copia a senha gerada para a área de transferência."""
    senha = senha_gerada.get()
    if senha:
        janela.clipboard_clear()  # Limpa a área de transferência anterior
        janela.clipboard_append(senha)  # Adiciona a nova senha
        janela.update()  # Garante que o Tkinter atualize a área de transferência
        messagebox.showinfo("Sucesso", "Senha copiada.")
    else:
        messagebox.showwarning("Aviso", "Gere uma senha antes de copiar.")


# ---- ### Front do programa ### ---- #

# --- Configuração da Janela ---
janela = tk.Tk()
janela.title("Gerador de Senha")
janela.geometry("1000x450")

# DEFININDO O BACKGROUND DA JANELA PRINCIPAL
janela.configure(bg="#000000")


# --- Variáveis de Controle ---
# Variáveis para os Checkbox (IntVar para 0/1, que representa Desmarcado/Marcado)
var_maiuscula = tk.IntVar(value=0)  # Começa desmarcado
var_minuscula = tk.IntVar(value=0)
var_numeros = tk.IntVar(value=0)
var_especiais = tk.IntVar(value=0)

# Variável para a senha gerada (StringVar para texto)
senha_gerada = tk.StringVar()
senha_gerada.set("")

# --- Widgets ---

# 1. Título Grande
titulo = tk.Label(
    janela,
    text="Gerador de Senhas Aleatórias",
    font=("Helvetica", 32, "bold"),
    fg="#FFFFFF"  # Cor Branca para o texto
)
titulo.pack(pady=20)

# Separador visual
frame_opc = tk.Frame(janela)
tk.Label(frame_opc, text="--- Crie senhas fortes e seguras instantaneamente para proteger suas contas ---", fg= "#FFFFFF", font=("Helvetica", 18, "bold")).grid(row=1, column=0, columnspan=2, pady=10)


# 1. Campo para Exibir a Senha
entrada_senha = tk.Entry(
    janela,
    textvariable=senha_gerada,
    width=35,
    font=("Courier", 12),
    relief=tk.SUNKEN
)
entrada_senha.pack(pady=10, padx=20)

# 2. Frame para as Opções e Tamanho
frame_opcoes = tk.Frame(janela)
frame_opcoes.pack(pady=10, padx=20, fill='x')

# Label e Entrada para o Tamanho da Senha
label_tamanho = tk.Label(frame_opcoes, text="Tamanho da Senha:", fg= "#FFFFFF", font=("Helvetica", 14, "bold"))
label_tamanho.grid(row=0, column=0, sticky='w', pady=5, padx=5)

# A caixa de entrada
entrada_tamanho = tk.Entry(frame_opcoes, width=5)
entrada_tamanho.insert(0, "8")  # Valor inicial sugerido
entrada_tamanho.grid(row=0, column=1, sticky='w', pady=5, padx=5)


# 3. Botão Gerar Senha
btn_gerar = tk.Button(
    janela,
    text="Gerar Senha",
    command=gerar_senha,
    bg="#4CAF50",  # Verde
    fg="white",
    font=("Helvetica", 12, "bold")
)
btn_gerar.pack(pady=15, ipadx=10, ipady=5)



# 4. Botão Copiar Senha
btn_copiar = tk.Button(
    janela,
    text="Copiar Senha",
    command=copiar_senha,
    bg="#2196F3",  # Azul
    fg="white",
    font=("Helvetica", 10)
)
btn_copiar.pack(pady=5)

# 6. Checkboxes
chk_maiuscula = tk.Checkbutton(
    frame_opcoes,
    text="Letras Maiúsculas (A-Z)",
    variable=var_maiuscula,
    fg= "#FFFFFF"
)
chk_maiuscula.grid(row=2, column=0, columnspan=2, sticky='w', padx=5)

chk_minuscula = tk.Checkbutton(
    frame_opcoes,
    text="Letras Minúsculas (a-z)",
    variable=var_minuscula,
    fg= "#FFFFFF"
)
chk_minuscula.grid(row=3, column=0, columnspan=2, sticky='w', padx=5)

chk_numeros = tk.Checkbutton(
    frame_opcoes,
    text="Números (0-9)",
    variable=var_numeros,
    fg= "#FFFFFF"
)
chk_numeros.grid(row=4, column=0, columnspan=2, sticky='w', padx=5)

chk_especiais = tk.Checkbutton(
    frame_opcoes,
    text="Caracteres Especiais (!@#$%)",
    variable=var_especiais,
    fg= "#FFFFFF"
)
chk_especiais.grid(row=5, column=0, columnspan=2, sticky='w', padx=5)

# --- Loop Principal ---
janela.mainloop()