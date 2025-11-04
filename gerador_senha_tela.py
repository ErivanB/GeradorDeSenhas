import tkinter as tk
from tkinter import messagebox, ttk
import random
import string

# --- Configurações de Cores e Tema ---
COR_FUNDO = "#1e1e1e"
COR_CARD = "#2d2d2d"
COR_TEXTO = "#ffffff"
COR_PRIMARIA = "#4CAF50"
COR_SECUNDARIA = "#2196F3"
COR_DESTAQUE = "#FF9800"


# --- Funções ---
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

    # Atualizar força da senha
    atualizar_forca_senha(senha)


def atualizar_forca_senha(senha):
    """Atualiza a barra de força da senha baseada na complexidade."""
    if not senha:
        barra_forca['value'] = 0
        return

    comprimento = len(senha)
    tipos = sum([
        any(c in string.ascii_uppercase for c in senha),
        any(c in string.ascii_lowercase for c in senha),
        any(c in string.digits for c in senha),
        any(c in string.punctuation for c in senha)
    ])

    # Cálculo simples da força
    forca = min(100, (comprimento * 3) + (tipos * 15))
    barra_forca['value'] = forca

    # Atualizar cor da barra
    if forca < 40:
        barra_forca.configure(style="Red.Horizontal.TProgressbar")
    elif forca < 70:
        barra_forca.configure(style="Yellow.Horizontal.TProgressbar")
    else:
        barra_forca.configure(style="Green.Horizontal.TProgressbar")


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


def alternar_visibilidade_senha():
    """Alterna entre mostrar e ocultar a senha."""
    if entrada_senha.cget('show') == '':
        entrada_senha.config(show='•')
        btn_visibilidade.config(text="👁️")
    else:
        entrada_senha.config(show='')
        btn_visibilidade.config(text="👁️‍🗨️")


# --- Configuração da Janela ---
janela = tk.Tk()
janela.title("Gerador de Senhas Seguras")
janela.geometry("500x600")
janela.configure(bg=COR_FUNDO)
janela.resizable(False, False)

# --- Configurar estilos para a barra de progresso ---
style = ttk.Style()
style.theme_use('clam')
style.configure("Green.Horizontal.TProgressbar", background="#4CAF50")
style.configure("Yellow.Horizontal.TProgressbar", background="#FFC107")
style.configure("Red.Horizontal.TProgressbar", background="#F44336")

# --- Variáveis de Controle ---
var_maiuscula = tk.IntVar(value=1)
var_minuscula = tk.IntVar(value=1)
var_numeros = tk.IntVar(value=1)
var_especiais = tk.IntVar(value=0)
senha_gerada = tk.StringVar()
senha_gerada.set("")

# --- Layout Principal ---

# Cabeçalho
frame_cabecalho = tk.Frame(janela, bg=COR_FUNDO)
frame_cabecalho.pack(pady=20)

titulo = tk.Label(
    frame_cabecalho,
    text="🔐 Gerador de Senhas",
    font=("Arial", 20, "bold"),
    fg=COR_TEXTO,
    bg=COR_FUNDO
)
titulo.pack()

subtitulo = tk.Label(
    frame_cabecalho,
    text="Crie senhas fortes e seguras instantaneamente",
    font=("Arial", 10),
    fg="#CCCCCC",
    bg=COR_FUNDO
)
subtitulo.pack(pady=5)

# Card Principal
frame_card = tk.Frame(janela, bg=COR_CARD, relief=tk.RAISED, bd=1)
frame_card.pack(padx=20, pady=10, fill='both', expand=True)

# Seção de Configurações
label_config = tk.Label(
    frame_card,
    text="Configurações da Senha",
    font=("Arial", 12, "bold"),
    fg=COR_TEXTO,
    bg=COR_CARD
)
label_config.pack(anchor='w', padx=15, pady=(15, 10))

# Tamanho da Senha
frame_tamanho = tk.Frame(frame_card, bg=COR_CARD)
frame_tamanho.pack(fill='x', padx=15, pady=5)

label_tamanho = tk.Label(
    frame_tamanho,
    text="Tamanho:",
    font=("Arial", 10),
    fg=COR_TEXTO,
    bg=COR_CARD
)
label_tamanho.pack(side='left')

entrada_tamanho = tk.Spinbox(
    frame_tamanho,
    from_=4,
    to=50,
    width=5,
    bg="gray20",
    fg=COR_TEXTO,
    insertbackground=COR_TEXTO,
    justify='center'
)
entrada_tamanho.delete(0, 'end')
entrada_tamanho.insert(0, "12")
entrada_tamanho.pack(side='left', padx=5)

# Tipos de Caracteres
frame_tipos = tk.Frame(frame_card, bg=COR_CARD)
frame_tipos.pack(fill='x', padx=15, pady=10)


def criar_checkbox(parent, text, variable):
    return tk.Checkbutton(
        parent,
        text=text,
        variable=variable,
        font=("Arial", 9),
        fg=COR_TEXTO,
        bg=COR_CARD,
        selectcolor="gray20",
        activebackground=COR_CARD,
        activeforeground=COR_TEXTO
    )


# Checkboxes em duas colunas
chk_maiuscula = criar_checkbox(frame_tipos, "Letras Maiúsculas (ABC)", var_maiuscula)
chk_maiuscula.grid(row=0, column=0, sticky='w', pady=3)

chk_minuscula = criar_checkbox(frame_tipos, "Letras Minúsculas (abc)", var_minuscula)
chk_minuscula.grid(row=1, column=0, sticky='w', pady=3)

chk_numeros = criar_checkbox(frame_tipos, "Números (123)", var_numeros)
chk_numeros.grid(row=0, column=1, sticky='w', pady=3, padx=(20, 0))

chk_especiais = criar_checkbox(frame_tipos, "Caracteres Especiais (@#!)", var_especiais)
chk_especiais.grid(row=1, column=1, sticky='w', pady=3, padx=(20, 0))

# Botão Gerar
btn_gerar = tk.Button(
    frame_card,
    text="🔄 Gerar Senha",
    command=gerar_senha,
    bg=COR_PRIMARIA,
    fg="white",
    font=("Arial", 11, "bold"),
    relief=tk.FLAT,
    cursor="hand2"
)
btn_gerar.pack(pady=15, ipadx=20, ipady=8)

# Seção de Resultado
label_resultado = tk.Label(
    frame_card,
    text="Sua Senha Gerada",
    font=("Arial", 12, "bold"),
    fg=COR_TEXTO,
    bg=COR_CARD
)
label_resultado.pack(anchor='w', padx=15, pady=(10, 5))

# Campo da Senha com botão de visibilidade
frame_senha = tk.Frame(frame_card, bg=COR_CARD)
frame_senha.pack(fill='x', padx=15, pady=5)

entrada_senha = tk.Entry(
    frame_senha,
    textvariable=senha_gerada,
    width=30,
    font=("Courier", 12, "bold"),
    relief=tk.SUNKEN,
    bg="gray15",
    fg=COR_DESTAQUE,
    insertbackground=COR_DESTAQUE,
    show='•',
    justify='center'
)
entrada_senha.pack(side='left', fill='x', expand=True, ipady=8)

btn_visibilidade = tk.Button(
    frame_senha,
    text="👁️",
    command=alternar_visibilidade_senha,
    bg="gray30",
    fg=COR_TEXTO,
    font=("Arial", 10),
    width=3,
    relief=tk.FLAT
)
btn_visibilidade.pack(side='right', padx=(5, 0), ipady=4)

# Indicador de Força da Senha
frame_forca = tk.Frame(frame_card, bg=COR_CARD)
frame_forca.pack(fill='x', padx=15, pady=(10, 5))

label_forca = tk.Label(
    frame_forca,
    text="Força da Senha:",
    font=("Arial", 9),
    fg=COR_TEXTO,
    bg=COR_CARD
)
label_forca.pack(anchor='w')

barra_forca = ttk.Progressbar(
    frame_forca,
    orient='horizontal',
    length=100,
    mode='determinate',
    style="Red.Horizontal.TProgressbar"
)
barra_forca.pack(fill='x', pady=5)

# Botões de Ação
frame_botoes = tk.Frame(frame_card, bg=COR_CARD)
frame_botoes.pack(pady=15)

btn_copiar = tk.Button(
    frame_botoes,
    text="📋 Copiar Senha",
    command=copiar_senha,
    bg=COR_SECUNDARIA,
    fg="white",
    font=("Arial", 10, "bold"),
    relief=tk.FLAT,
    cursor="hand2"
)
btn_copiar.pack(side='left', padx=5, ipadx=15, ipady=6)

# Rodapé
frame_rodape = tk.Frame(janela, bg=COR_FUNDO)
frame_rodape.pack(pady=10)

texto_dicas = tk.Label(
    frame_rodape,
    text="💡 Dica: Use senhas com pelo menos 12 caracteres e combine diferentes tipos",
    font=("Arial", 8),
    fg="#888888",
    bg=COR_FUNDO,
    wraplength=400
)
texto_dicas.pack()

# --- Inicialização ---
atualizar_forca_senha("")

# --- Loop Principal ---
janela.mainloop()