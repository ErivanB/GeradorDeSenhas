import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import random
import string
import os

# --- Configurações de Cores e Tema ---
COR_FUNDO = "#1e1e1e"
COR_CARD = "#2d2d2d"
COR_TEXTO = "#ffffff"
COR_PRIMARIA = "#4CAF50"
COR_SECUNDARIA = "#2196F3"
COR_DESTAQUE = "#FF9800"

# Variável global para armazenar palavras do arquivo
palavras_arquivo = []


# --- Funções ---
def carregar_arquivo_palavras():
    """Carrega um arquivo de texto com palavras para usar na geração de senhas."""
    global palavras_arquivo

    arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo de texto com palavras",
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )

    if arquivo:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                # Lê todas as linhas, remove espaços em branco e filtra linhas vazias
                palavras_arquivo = [linha.strip() for linha in f.readlines() if linha.strip()]

            if palavras_arquivo:
                label_arquivo.config(text=f"✓ Arquivo carregado: {len(palavras_arquivo)} palavras")
                messagebox.showinfo("Sucesso",
                                    f"Arquivo carregado com sucesso!\n{len(palavras_arquivo)} palavras disponíveis.")
            else:
                palavras_arquivo = []
                label_arquivo.config(text="❌ Arquivo vazio ou inválido")
                messagebox.showerror("Erro", "O arquivo está vazio ou não contém palavras válidas.")

        except Exception as e:
            palavras_arquivo = []
            label_arquivo.config(text="❌ Erro ao carregar arquivo")
            messagebox.showerror("Erro", f"Não foi possível ler o arquivo:\n{str(e)}")


def gerar_senha_palavras():
    """Gera senha usando palavras de um arquivo carregado."""
    global palavras_arquivo

    if not palavras_arquivo:
        messagebox.showwarning("Aviso", "Por favor, carregue um arquivo de texto com palavras primeiro.")
        return

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

    # Gera senha baseada em palavras
    senha = ""
    tentativas = 0
    max_tentativas = 100

    while len(senha) < tamanho and tentativas < max_tentativas:
        palavra = random.choice(palavras_arquivo)

        # Decide se adiciona a palavra completa ou partes dela
        if len(senha) + len(palavra) <= tamanho:
            senha += palavra
        else:
            # Se a palavra for muito grande, pega um pedaço dela
            espaco_restante = tamanho - len(senha)
            if espaco_restante > 0:
                senha += palavra[:espaco_restante]

        # Adiciona separadores ocasionalmente
        if len(senha) < tamanho and random.random() < 0.3:
            separadores = ['-', '_', '.', '', '']
            separador = random.choice(separadores)
            if len(senha) + len(separador) <= tamanho:
                senha += separador

        tentativas += 1

    # Se ainda não atingiu o tamanho, completa com caracteres aleatórios
    if len(senha) < tamanho:
        caracteres = ''
        if var_maiuscula.get(): caracteres += string.ascii_uppercase
        if var_minuscula.get(): caracteres += string.ascii_lowercase
        if var_numeros.get(): caracteres += string.digits
        if var_especiais.get(): caracteres += string.punctuation

        if not caracteres:
            caracteres = string.ascii_letters + string.digits

        while len(senha) < tamanho:
            senha += random.choice(caracteres)

    # Aplica transformações baseadas nas opções selecionadas
    senha_transformada = aplicar_transformacoes(senha)

    # Garante que a senha tenha o tamanho exato
    senha_final = senha_transformada[:tamanho]

    senha_gerada.set(senha_final)
    atualizar_forca_senha(senha_final)


def aplicar_transformacoes(senha):
    """Aplica transformações na senha baseado nas opções selecionadas."""
    resultado = senha

    # Aplica maiúsculas/minúsculas baseado nas configurações
    chars = list(resultado)
    for i in range(len(chars)):
        if chars[i].isalpha():
            if var_maiuscula.get() and not var_minuscula.get():
                chars[i] = chars[i].upper()
            elif var_minuscula.get() and not var_maiuscula.get():
                chars[i] = chars[i].lower()
            else:
                # Se ambos estão selecionados, decide aleatoriamente
                if random.random() < 0.5:
                    chars[i] = chars[i].upper()
                else:
                    chars[i] = chars[i].lower()

    resultado = ''.join(chars)

    # Adiciona números se solicitado
    if var_numeros.get():
        # Substitui algumas letras por números similares ou adiciona números
        substituicoes = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5'}
        nova_senha = []
        for char in resultado:
            if char.lower() in substituicoes and random.random() < 0.3:
                nova_senha.append(substituicoes[char.lower()])
            else:
                nova_senha.append(char)
        resultado = ''.join(nova_senha)

    # Adiciona caracteres especiais se solicitado
    if var_especiais.get() and random.random() < 0.5:
        especiais = '!@#$%&*'
        pos = random.randint(0, len(resultado))
        resultado = resultado[:pos] + random.choice(especiais) + resultado[pos:]

    return resultado


def gerar_senha():
    """Gera a senha com base nas opções selecionadas e no tamanho."""
    # Verifica se há arquivo carregado e usa a função de palavras se disponível
    if palavras_arquivo and var_usar_palavras.get():
        gerar_senha_palavras()
    else:
        gerar_senha_tradicional()


def gerar_senha_tradicional():
    """Gera senha usando o método tradicional de caracteres aleatórios."""
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
janela.geometry("550x650")
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
var_usar_palavras = tk.IntVar(value=0)
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

# Seção de Arquivo de Palavras
frame_arquivo = tk.Frame(frame_card, bg=COR_CARD)
frame_arquivo.pack(fill='x', padx=15, pady=10)

label_arquivo_titulo = tk.Label(
    frame_arquivo,
    text="📁 Gerar a partir de palavras:",
    font=("Arial", 10, "bold"),
    fg=COR_TEXTO,
    bg=COR_CARD
)
label_arquivo_titulo.pack(anchor='w')

frame_arquivo_botoes = tk.Frame(frame_arquivo, bg=COR_CARD)
frame_arquivo_botoes.pack(fill='x', pady=5)

btn_carregar_arquivo = tk.Button(
    frame_arquivo_botoes,
    text="📂 Carregar Arquivo de Texto",
    command=carregar_arquivo_palavras,
    bg="#6D4C41",
    fg="white",
    font=("Arial", 9),
    relief=tk.FLAT,
    cursor="hand2"
)
btn_carregar_arquivo.pack(side='left', padx=(0, 10))

chk_usar_palavras = tk.Checkbutton(
    frame_arquivo_botoes,
    text="Usar palavras do arquivo",
    variable=var_usar_palavras,
    font=("Arial", 9),
    fg=COR_TEXTO,
    bg=COR_CARD,
    selectcolor="gray20",
    activebackground=COR_CARD,
    activeforeground=COR_TEXTO
)
chk_usar_palavras.pack(side='left')

label_arquivo = tk.Label(
    frame_arquivo,
    text="Nenhum arquivo carregado",
    font=("Arial", 8),
    fg="#888888",
    bg=COR_CARD
)
label_arquivo.pack(anchor='w')

# Separador
separador = ttk.Separator(frame_card, orient='horizontal')
separador.pack(fill='x', padx=15, pady=5)

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

# Tipos de Caracteres - TODOS NA MESMA LINHA
frame_tipos = tk.Frame(frame_card, bg=COR_CARD)
frame_tipos.pack(fill='x', padx=15, pady=15)


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


# Checkboxes todos na mesma linha com espaçamento igual
chk_maiuscula = criar_checkbox(frame_tipos, "Maiúsculas", var_maiuscula)
chk_maiuscula.grid(row=0, column=0, sticky='w', padx=10)

chk_minuscula = criar_checkbox(frame_tipos, "Minúsculas", var_minuscula)
chk_minuscula.grid(row=0, column=1, sticky='w', padx=10)

chk_numeros = criar_checkbox(frame_tipos, "Números", var_numeros)
chk_numeros.grid(row=0, column=2, sticky='w', padx=10)

chk_especiais = criar_checkbox(frame_tipos, "Especiais", var_especiais)
chk_especiais.grid(row=0, column=3, sticky='w', padx=10)

# Centralizar os checkboxes na linha
for i in range(4):
    frame_tipos.columnconfigure(i, weight=1)

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
    text="💡 Dica: Use senhas com pelo menos 12 caracteres e combine diferentes tipos. Arquivos de palavras criam senhas mais memoráveis!",
    font=("Arial", 8),
    fg="#888888",
    bg=COR_FUNDO,
    wraplength=500
)
texto_dicas.pack()

# --- Inicialização ---
atualizar_forca_senha("")

# --- Loop Principal ---
janela.mainloop()