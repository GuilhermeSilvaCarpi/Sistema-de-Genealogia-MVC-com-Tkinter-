import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import messagebox as mb


class View(tk.Tk):
    # INICIALIZANDO
    def __init__(self, model):
        super().__init__()
        # Tentando conectar banco de dados
        try:
            self.model = model
            self.arvore = self.model.arvore()
        except Exception as e:
            mb.showerror('Genealogias - Banco de dados inacessível', 'Não é possível abrir essa aplicação offline, reconecte-se e tente novamente')
            print(e)
        
        # tkinter
        self.title('Genealogias')
        self.geometry('400x600')
        
        ttk.Style('cosmo')
        # Métodos
        self.id_pessoas = self.model.get_id_e_nomes()
        self.menu_superior()
    
    
    # MENU SUPERIOR
    def menu_superior(self):
        # Criando e posicionando menu superior
        self.menu = ttk.Notebook(self)
        self.menu.pack(fill='both', expand=True)
        
        # Criando janelas
        self.janela_inicio  = Janela_inicio(self)
        self.janela_cadastro = Janela_cadastro(self)
        self.janela_consulta = Janela_consulta(self)
        self.janela_arvore   = Janela_arvore(self)
        self.janela_config   = Janela_configurações(self)
        
        # Posicionando as janelas no menu superior
        janelas = [self.janela_inicio, self.janela_cadastro, self.janela_consulta, self.janela_arvore, self.janela_config]
        nomes_menus = ['Inicio', 'Cadastro', 'Consulta', 'Arvore', 'Configurações']
        
        for i in range(len(nomes_menus)):
            self.menu.add(janelas[i], text=nomes_menus[i])


# JANELA INICIO
class Janela_inicio(ttk.Frame):
    def __init__(self, root:View):
        super().__init__(root)
        # Root
        self.root = root
        # Widgets da janela inicial
        tk.Label(self, text='Registros').pack(pady=10)
        self.botao_atualizar = tk.Button(self, text='Atualizar')
        self.botao_atualizar.pack(pady=10)
        
        # Widget tabela inicial
        colunas = ['id', 'nome', 'descricao', 'pai', 'mae', 'passagem']
        
        self.tabela = ttk.Treeview(
            self,
            columns=colunas,
            show='headings'
        )
        
        for celula in colunas:
            self.tabela.heading(celula, text=celula)
            self.tabela.column(celula, width=2)
        
        self.tabela.pack(fill='both', expand=True)


# JANELA CADASTRO
class Janela_cadastro(ttk.Frame):
    def __init__(self, root:View):
        super().__init__(root)
        # Root
        self.root = root
        # Frame de centralização
        self.cent = tk.Frame(self)
        self.cent.pack()
        
        # Inicializando variaveis importantes
        pad_x, pad_y, larg_ent = 10, 10, 35
        id_pessoas = self.root.model.get_id_e_nomes()
        
        # Posicionando labels
        self.labels = ['Nome', 'Id pai', 'Id mãe', 'Descrição', 'Passagem']
        for i in range(len(self.labels)):
            tk.Label(self.cent, text=self.labels[i]).grid(row=i, column=0, padx=pad_x, pady=pad_y)
        
        # Criando idgets de entrada
        self.ent_nome = tk.Entry(self.cent, width=larg_ent)
        self.ent_pai = ttk.Combobox(self.cent, width=larg_ent-3, values=id_pessoas)
        self.ent_mae = ttk.Combobox(self.cent, width=larg_ent-3, values=id_pessoas)
        self.ent_descricao = tk.Text(self.cent, width=larg_ent, height=4)
        self.ent_passagem  = tk.Text(self.cent, width=larg_ent, height=2)
        
        # Posicionando widgets de entrada
        self.entradas = [self.ent_nome, self.ent_pai, self.ent_mae, self.ent_descricao, self.ent_passagem]
        for i in range(len(self.entradas)):
            self.entradas[i].grid(row=i, column=1, padx=pad_x, pady=pad_y)
        
        # Botões
        self.botao_limpar = tk.Button(self.cent, text='Limpar')
        self.botao_cadastrar = tk.Button(self.cent, text='Cadastrar')
        
        self.botao_limpar.grid(row=5, column=0, padx=pad_x)
        self.botao_cadastrar.grid(row=5, column=1, padx=pad_x)


# JANELA EDIÇÃO
class Janela_edicao(ttk.Toplevel):
    # Recomendado ler depois de 'JANELA CONSULTA'
    def __init__(self, root:View):
        super().__init__(root)
        # Root
        self.root = root
        
        # Tenta verificar qual é o registro selecionado
        try:
            # Capta o id de tabela de item selecionado
            id_selecao = self.root.janela_consulta.tabela.selection()
            # Capta os valores do item da tabela no id
            self.valores = self.root.janela_consulta.tabela.item(id_selecao)['values']
            self.valores[1]
            
            # Criando uma janela paar edição de registro
            self.title(f'Edição ({self.valores[0]} - {self.valores[1]})')
            self.geometry('350x350')
            
            # Valores importantes para o lauyout
            pad_x, pad_y, larg_ent = 10, 10, 35
            
            # Posicionando labels
            pad_x, pad_y = 10, 10
            
            self.labels = ['Nome', 'Id pai', 'Id mãe', 'Descrição', 'Passagem']
            for i in range(len(self.labels)):
                tk.Label(self, text=self.root.janela_cadastro.labels[i]).grid(row=i, column=0, padx=pad_x, pady=pad_y)
            
            # Criando widgets de entrada
            self.ent_nome = tk.Entry(self, width=larg_ent)
            self.ent_pai = ttk.Combobox(self, width=larg_ent-3, values=self.root.id_pessoas)
            self.ent_mae = ttk.Combobox(self, width=larg_ent-3, values=self.root.id_pessoas)
            self.ent_descricao = tk.Text(self, width=larg_ent, height=4)
            self.ent_passagem  = tk.Text(self, width=larg_ent, height=2)
            
            # Posicionando widgets de entrada
            self.entradas = [self.ent_nome, self.ent_pai, self.ent_mae, self.ent_descricao, self.ent_passagem]
            for i in range(len(self.entradas)):
                self.entradas[i].grid(row=i, column=1, padx=pad_x, pady=pad_y)
            
            # Preenchendo widgets de entrada
            self.ent_nome.insert(0, self.valores[1])
            self.ent_descricao.insert(1.0, self.valores[6])
            self.ent_passagem.insert(1.0, self.valores[7])
            
            if self.valores[2] != 'None':
                self.ent_pai.set(f'{self.valores[2]} - {self.valores[3]}')
            if self.valores[4] != 'None':
                self.ent_mae.set(f'{self.valores[4]} - {self.valores[5]}')
            
            # Criando botões
            self.botao_cancelar = tk.Button(self, text='Cancelar')
            self.botao_salvar = tk.Button(self, text='Salvar edições')
            
            
            self.botao_cancelar.grid(row=5,  column=0)
            self.botao_salvar.grid(row=5, column=1)
            
        
        # Caso não haja registro selecionado
        except IndexError:
            mb.showerror('Erro para editar', 'Não há registro selecionado para editar')


# JANELA CONSULTA
class Janela_consulta(ttk.Frame):
    def __init__(self, root:View):
        super().__init__(root)
        self.root = root
        # Layout da consulta
        tk.Label(self ,text='Pesquisar pessoa').pack(pady=5)
        self.cent = ttk.Frame(self)
        self.cent.pack()
        
        # Labels e entrys
        self.labels = [
            ['Id', 'Nome'],
            ['Id do pai', 'Nome do pai'],
            ['Id da mãe', 'Nome da mãe'],
            ['Decrição', 'Passagem']
        ]
        self.entradas = []
        
        for y in range(len(self.labels)):
            for x in range(2):
                tk.Label(self.cent, text=self.labels[y][x]).grid(row=y*2, column=x)
                self.entradas.append(tk.Entry(self.cent, width=30))
                self.entradas[-1].grid(row=y*2+1, column=x, padx=5)
        
        # Botões
        ## Criando botões
        self.botao_limpar = tk.Button(self.cent, text='Limpar formulário', width=25)
        self.botao_pesquisar = tk.Button(self.cent, text='Pesquisar', width=25)
        self.botao_editar = tk.Button(self.cent, text='Editar', width=25)
        self.botao_excluir = tk.Button(self.cent, text='Excluir', width=25)
                
        ## Posicionando botões
        botoes = [
            self.botao_limpar, self.botao_pesquisar,
            self.botao_editar, self.botao_excluir
        ]
        botoes[0].grid(row=8, column=1, pady=10)
        botoes[1].grid(row=9, column=1, pady=10)
        botoes[2].grid(row=9, column=0, pady=10)
        botoes[3].grid(row=8, column=0, pady=10)
        
        # Tabela de consulta
        self.colunas = ['Id', 'Nome', 'Id_pai', 'Nome_pai', 'Id_mae', 'Nome_mae', 'Descrição', 'Passagens']
        #con_colunas = ['Pessoa', 'Pai', 'Mae', 'Descrição', 'Passagens']
        
        self.tabela = ttk.Treeview(
            self,
            columns=self.colunas,
            show='headings'
        )
        
        for celula in self.colunas:
            self.tabela.heading(celula, text=celula)
            self.tabela.column(celula, width=2)
        
        self.tabela.pack(fill='both', expand=True)


# JANELA ARVORE
class Janela_arvore(ttk.Frame):
    def __init__(self, root:View):
        super().__init__(root)
        # Root
        self.root = root
        
        # Centralizando
        self.cent = tk.Frame(self)
        self.cent.pack()
        
        # Paddings
        pad_x = 10
        pad_y = 20
        
        # Criando widgets
        self.label   = tk.Label(self.cent, text='Pessoa')
        self.selecao = ttk.Combobox(self.cent, values=self.root.id_pessoas)
        self.botao   = tk.Button(self.cent, text='Gerar árvore', height=2, width=20)
        ##self.output  = tk.Label(self, text='', justify='left', font='Consolas')
        self.output  = tk.Text(self, font='Consolas')
        self.output.config(state=tk.DISABLED, wrap=tk.NONE)
        
        # Poscicionando widgets
        self.label.grid(row=0, column=0, padx=pad_x)
        self.selecao.grid(row=0, column=1, padx=pad_x, pady=pad_y)
        self.botao.grid(row=0, column=2, padx=pad_x)
        self.output.pack(expand=True)


# JANELA CONFIGURAÇÕES
class Janela_configurações(ttk.Frame):
    def __init__(self, root:View):
        super().__init__(root)
        # Root
        self.root = root
        
        # Centralizando
        self.cent = tk.Frame(self)
        self.cent.pack(pady=10)
        # Paddings
        pad_x, pad_y = 20, 10
        
        # TEMAS CLAROS
        ## Combobox
        temas_claros = ['cosmo', 'journal', 'minty', 'pulse', 'sandstone', 'morph']
        self.ent_tema_claro = ttk.Combobox(self.cent, values=temas_claros)
        self.ent_tema_claro.grid(row=0, column=1)
        ## Label e botão
        tk.Label(self.cent, text='Temas claros').grid(row=0, column=0, padx=pad_x, pady=pad_y)
        self.apl_tema_claro = tk.Button(self.cent, text='Aplicar')
        self.apl_tema_claro.grid(row=0, column=2, padx=pad_x)
        
        
        # TEMAS ESCUROS
        ## Combobox
        temas_escuros = ['darkly', 'cyborg', 'superhero', 'solar']
        self.ent_tema_escuro = ttk.Combobox(self.cent, values=temas_escuros)
        self.ent_tema_escuro.grid(row=1, column=1)
        ## Label e botão
        tk.Label(self.cent, text='Temas escuros').grid(row=1, column=0, padx=pad_x, pady=pad_y)
        self.apl_tema_escuro = tk.Button(self.cent, text='Aplicar')
        self.apl_tema_escuro.grid(row=1, column=2, padx=pad_x)
        
        
        # FONT DA ARVORE GENEALÓGICA
        ## Combobox
        """
        fontes = [
            'Courier', 'Courier New', 'Consolas',
            'DejaVu Sans Mono', 'Lucida Sans Typewriter',
            'OCR A'
        ]
        """
        fontes = ['Courier', 'Consolas']
        self.ent_fontes = ttk.Combobox(self.cent, values=fontes)
        self.ent_fontes.grid(row=2, column=1)
        ## Label e botão
        tk.Label(self.cent, text='Fonte da árvore*').grid(row=2, column=0, padx=pad_x, pady=pad_y)
        self.apl_font_arv = tk.Button(self.cent, text='Aplicar')
        self.apl_font_arv.grid(row=2, column=2, padx=pad_x)
        
        
        # ON/OFF PAIS E DESCRIÇÃO NA ÁRVORE
        ## Ciando checkbuttons
        self.arv_pais = tk.IntVar()
        tk.Checkbutton(self.cent, text='Pais', variable=self.arv_pais).grid(row=3, column=0)
        self.arv_descricao = tk.IntVar()
        tk.Checkbutton(self.cent, text='Descrição', variable=self.arv_descricao).grid(row=3, column=1)
        ## Botão de aplicar
        self.apl_config_arv = tk.Button(self.cent, text='Aplicar')
        self.apl_config_arv.grid(row=3, column=2, padx=pad_x)
        
        """
        # SALVAR CONFIGURAÇÕES
        salvar_config = tk.Button(
            self, text='Salvar configurações*',
            height=2, width=20
        ).pack(pady=pad_y)
        """
