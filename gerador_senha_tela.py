import tkinter as tk
from tkinter import messagebox
import random
import string

# --- Configurações de Cores ---
COR_FUNDO = "black"
COR_TEXTO = "white"


# (Mantenha as funções 'gerar_senha' e 'copiar_senha' sem alterações)
def gerar_senha():
    """Gera a senha com base nas opções selecionadas e no tamanho."""
    try:
        tamanho = int(entrada_tamanho.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido para o tamanho.")
        senha_gerada.set("")
        return

    if tamanho <= 0:
        messagebox.showerror("Erro", "O tamanho da senha deve ser maior que zero.")
        senha_gerada.set("")
        return

    caracteres = ''
    if var_maiuscula.get(): caracteres += string.ascii_uppercase
    if var_minuscula.get(): caracteres += string.ascii_lowercase
    if var_numeros.get(): caracteres += string.digits
    if var_especiais.get(): caracteres += string.punctuation

    if not caracteres:
        messagebox.showwarning("Aviso", "Selecione pelo menos um tipo de caractere.")
        senha_gerada.set("")
        return

    senha = ''.join(random.choices(caracteres, k=tamanho))
    senha_gerada.set(senha)


def copiar_senha():
    """Copia a senha gerada para a área de transferência."""
    senha = senha_gerada.get()
    if senha:
        janela.clipboard_clear()
        janela.clipboard_append(senha)
        janela.update()
        messagebox.showinfo("Sucesso", "Senha copiada para a área de transferência!")
    else:
        messagebox.showwarning("Aviso", "Gere uma senha antes de copiar.")


# --- Configuração da Janela ---
janela = tk.Tk()
janela.title("Gerador de Senha")
janela.geometry("1000x450")  # Aumentei um pouco a largura para caber os checkboxes
janela.configure(bg=COR_FUNDO)

# --- Variáveis de Controle ---
var_maiuscula = tk.IntVar(value=1)
var_minuscula = tk.IntVar(value=1)
var_numeros = tk.IntVar(value=1)
var_especiais = tk.IntVar(value=0)

senha_gerada = tk.StringVar()
senha_gerada.set("")

# --- Widgets ---

# 1. Título Grande
titulo = tk.Label(
    janela,
    text="Gerador de Senha",
    font=("Helvetica", 24, "bold"),
    fg="#FFFFFF",
    bg=COR_FUNDO
)
titulo.pack(pady=20)

# 2. Frame para as Opções e Tamanho
frame_opcoes = tk.Frame(janela, bg=COR_FUNDO)
frame_opcoes.pack(pady=10, padx=20, fill='x')

# Label e Entrada para o Tamanho da Senha
label_tamanho = tk.Label(
    frame_opcoes,
    text="Tamanho da Senha:",
    fg=COR_TEXTO,
    bg=COR_FUNDO
)
label_tamanho.grid(row=0, column=0, sticky='w', pady=5, padx=5)

entrada_tamanho = tk.Entry(frame_opcoes, width=5, bg="gray20", fg=COR_TEXTO, insertbackground=COR_TEXTO)
entrada_tamanho.insert(0, "8")
entrada_tamanho.grid(row=0, column=1, sticky='w', pady=5, padx=5)

# Separador visual
tk.Label(
    frame_opcoes,
    text="--- Crie senhas fortes e seguras instantaneamente para proteger suas contas ---",
    fg=COR_TEXTO,
    bg=COR_FUNDO
).grid(row=1, column=0, columnspan=2, pady=10)


# Função auxiliar para criar Checkbuttons com as cores configuradas
def criar_checkbox(parent, text, variable):
    return tk.Checkbutton(
        parent,
        text=text,
        variable=variable,
        fg=COR_TEXTO,
        bg=COR_FUNDO,
        selectcolor="gray20",
        activebackground=COR_FUNDO,
        activeforeground=COR_TEXTO
    )


# 3. Checkboxes (LADO A LADO)

# Usaremos a linha 2 para os primeiros dois e a linha 3 para os dois últimos.
# Cada linha terá 2 colunas.
linha_checkbox = 2

chk_maiuscula = criar_checkbox(frame_opcoes, "Maiúsculas", var_maiuscula)
chk_maiuscula.grid(row=linha_checkbox, column=0, sticky='w', padx=5)

chk_minuscula = criar_checkbox(frame_opcoes, "Minúsculas", var_minuscula)
chk_minuscula.grid(row=linha_checkbox, column=1, sticky='w', padx=5)

# Próxima linha para os restantes
linha_checkbox += 1

chk_numeros = criar_checkbox(frame_opcoes, "Números", var_numeros)
chk_numeros.grid(row=linha_checkbox, column=0, sticky='w', padx=5)

chk_especiais = criar_checkbox(frame_opcoes, "Especiais", var_especiais)
chk_especiais.grid(row=linha_checkbox, column=1, sticky='w', padx=5)

# 4. Botão Gerar Senha
btn_gerar = tk.Button(
    janela,
    text="Gerar Senha",
    command=gerar_senha,
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 12, "bold")
)
# Note que os widgets abaixo do frame não precisam de alterações, pois usam .pack()
btn_gerar.pack(pady=15, ipadx=10, ipady=5)

# 5. Campo para Exibir a Senha
entrada_senha = tk.Entry(
    janela,
    textvariable=senha_gerada,
    width=35,
    font=("Courier", 12),
    relief=tk.SUNKEN,
    bg="gray15",
    fg="yellow",
    insertbackground="yellow"
)
entrada_senha.pack(pady=10, padx=20)

# 6. Botão Copiar Senha
btn_copiar = tk.Button(
    janela,
    text="Copiar Senha",
    command=copiar_senha,
    bg="#2196F3",
    fg="white",
    font=("Helvetica", 10)
)
btn_copiar.pack(pady=5)

# --- Loop Principal ---
janela.mainloop()