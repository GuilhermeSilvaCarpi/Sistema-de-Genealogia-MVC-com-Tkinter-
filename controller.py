from view import View, Janela_edicao, Janela_configurações
from model import Model
from tkinter import messagebox as mb
import tkinter as tk
import ttkbootstrap as ttk

class Controller:
    # Inicializando
    def __init__(self, model:Model, view:View):
        self.model = model
        self.view = view
        
        # Botões
        ## Inicio
        self.view.janela_inicio.botao_atualizar.config(command=self.atualizar_tabela_inicio)
        ## Cadastro
        self.view.janela_cadastro.botao_limpar.config(command=self.limpar_ent_cad)
        self.view.janela_cadastro.botao_cadastrar.config(command=self.cadastrar)
        ## Consulta
        botoes = [
            view.janela_consulta.botao_limpar, 
            view.janela_consulta.botao_pesquisar,
            view.janela_consulta.botao_editar,
            view.janela_consulta.botao_excluir
        ]
        botoes[0].config(command=self.limpar_ent_constulta)
        botoes[1].config(command=self.atualizar_tabela_consulta)
        botoes[2].config(command=self.criar_janela_edicao)
        botoes[3].config(command=self.excluir_registro)
        ## Arvore
        self.view.janela_arvore.botao.config(command=self.escrever_arvore)
        ## Config
        self.config = Config(self.view.janela_config)
        
        # Inicializando algumas funções
        self.atualizar_tabela_inicio()
    
    # Atualizando comboboxs
    def atualizando_comboboxs(self):
        # Captando id-pessoas
        self.id_pessoas = self.model.get_id_e_nomes()
        # Atualizando comboboxs
        comboboxs = [
            self.view.janela_cadastro.ent_pai,
            self.view.janela_cadastro.ent_mae,
            self.view.janela_arvore.selecao
        ]
        for combobox in comboboxs:
            combobox.config(values=self.id_pessoas)
    
    # INICIO
    # Atualizar tabela inicio
    def atualizar_tabela_inicio(self):
        tabela = self.view.janela_inicio.tabela
        # Deletando itens anteriores
        tabela.delete(*tabela.get_children())
        # Inserindos valores da consulta geral
        for linha in self.model.get_todos_registros():
            tabela.insert("", "end", values=linha)
        # Atualizando comboboxs
        self.atualizando_comboboxs()
    
    # CADASTRO
    # Cadastrar entradas do cadastro
    def cadastrar(self):
        # Inicioalizando variáveis
        j_cadastro = self.view.janela_cadastro
        # Verificando se há pais selecionados
        pai_local = j_cadastro.ent_pai.get()
        if pai_local == '':
            pai_local = None
        else:
            pai_local = int(j_cadastro.ent_pai.get().split()[0])
        
        mae_local = j_cadastro.ent_mae.get()
        if mae_local == '':
            mae_local = None
        else:
            mae_local = int(j_cadastro.ent_mae.get().split()[0])
        
        # Cadastrando as entradas
        self.model.cadastrar_registro(
            j_cadastro.ent_nome.get(),
            pai_local,
            mae_local,
            j_cadastro.ent_descricao.get("1.0", 'end-1c'),
            j_cadastro.ent_passagem.get("1.0", 'end-1c')
        )
        
        #
        self.limpar_ent_cad()
        self.atualizar_tabela_inicio()
    
    # Limpar entradas do cadastro
    def limpar_ent_cad(self):
        j_cadastro = self.view.janela_cadastro
        j_cadastro.ent_nome.delete(0, 'end')
        j_cadastro.ent_mae.set('')
        j_cadastro.ent_pai.set('')
        j_cadastro.ent_descricao.delete('1.0', 'end')
        j_cadastro.ent_passagem.delete('1.0', 'end')
    
    # CONSULTA
    def atualizar_tabela_consulta(self):
        tabela = self.view.janela_consulta.tabela
        # Resetando a tabela
        tabela.delete(*tabela.get_children())
        # Captando e armazenando entradas
        con_entradas = self.view.janela_consulta.entradas
        entradas = []
        for i in range(len(con_entradas)):
            entradas.append(con_entradas[i].get().strip())
        # Preenchendo tabela
        for linha in self.model.pesquisar_pessoa(*entradas):
            tabela.insert("", "end", values=linha)
    
    def limpar_ent_constulta(self):
        entradas = self.view.janela_consulta.entradas
        for entrada in entradas:
            entrada.delete(0, 'end')
    
    def excluir_registro(self):
        tabela = self.view.janela_consulta.tabela
        # Tenta verificar qual é o registro selecionado
        try:
            # Capta o id de tabela de item selecionado
            selecao = tabela.selection()            
            texto = 'Confirmar exclusão de:'
            ids = []
            
            for linha in selecao[::-1]:
                # Capta os valores do item da tabela no id
                valores = tabela.item(linha)['values']
                # Capta o id da pessoa no banco de dados
                ids.append(valores[0])
                
                # Confirmação de exclusão
                texto += f'\n   {valores[0]} - {valores[1]} {valores[3], valores[5]}'
            
            if mb.askyesno(f'Excluir regsitro(s)?', texto):
                for id in ids:
                    # Método do banco de dados para excluir registro
                    self.model.excluir_registro(id)
        
        # Caso não haja registro selecionado
        except IndexError:
            mb.showerror('Erro para excluir', 'Não há registro selecionado para exclusão')
        
        # Atualizando a tabela inicial e a de consulta
        self.atualizar_tabela_inicio()
        self.atualizar_tabela_consulta()
        self.atualizando_comboboxs()

    # EDIÇÃO
    def criar_janela_edicao(self):
        # Criando objeto
        self.view_edicao =  Janela_edicao(self.view)
        # Configurando botões
        self.view_edicao.botao_cancelar.config(command=self.fechar_edição)
        self.view_edicao.botao_salvar.config(command=self.editar_registro)
        
    #
    def fechar_edição(self):
        self.view_edicao.destroy()
    
    def editar_registro(self):
        # Captando valores das entradas
        entradas = self.view_edicao.entradas
        ## Id e nome
        edicao = [
            self.view_edicao.valores[0],
            self.view_edicao.entradas[0].get(),
        ]
        ## Pai
        if entradas[1].get() == '':
            edicao.append(None)
        else:
            edicao.append(int(entradas[1].get().split()[0]))
        ## Mae
        if entradas[2].get() == '':
            edicao.append(None)
        else:
            edicao.append(int(entradas[2].get().split()[0]))
        ## Descrição e passagem
        edicao += [
            entradas[3].get("1.0", 'end-1c'),
            entradas[4].get("1.0", 'end-1c')
        ]
        
        # Alterando rgistro no banco de dados
        self.model.editar_registro(*edicao)
        # Atualiando tabela inicial, de consulta e comboboxs
        self.atualizar_tabela_inicio()
        self.atualizar_tabela_consulta()
        self.atualizando_comboboxs()
        # Fechando janela de edição
        self.fechar_edição()
    
    # Arvore
    def escrever_arvore(self):
        jan_arvore = self.view.janela_arvore
        try:
            id = jan_arvore.selecao.get().split()[0]
            
            jan_arvore.root.arvore.resetar_arvore()
            jan_arvore.root.arvore.processar_arvore(id)
            texto = jan_arvore.root.arvore.get_arvore_str()
            
            #self.output.config(text=texto)
            jan_arvore.output.config(state=tk.NORMAL)
            jan_arvore.output.delete(1.0, 'end')
            jan_arvore.output.insert(1.0, texto)
            jan_arvore.output.config(state=tk.DISABLED)
        
        except IndexError:
            mb.showerror('Erro para gerar árvore', 'Nenhum registro selecionado')
    
    # Config

class Config:
    def __init__(self, view:Janela_configurações):
        view.apl_tema_claro.config(command=self.tema_claro)
        view.apl_tema_escuro.config(command=self.tema_escuro)
        view.apl_font_arv.config(command=self.fonte_arvore)
        view.apl_config_arv.config(command=self.config_arvore)
        
        self.view = view
    
    def tema_claro(self):
        ttk.Style(self.view.ent_tema_claro.get())
        self.view.ent_tema_escuro.set('')
    
    def tema_escuro(self):
        ttk.Style(self.view.ent_tema_escuro.get())
        self.view.ent_tema_claro.set('')
    
    def fonte_arvore(self):
        self.view.root.janela_arvore.output.config(font=self.view.ent_fontes.get())
    
    def config_arvore(self):
        arv = self.view.root.arvore
        
        arv.mostrar_pais = bool(self.view.arv_pais.get())
        arv.mostrar_descricao = bool(self.view.arv_descricao.get())
    
    def salvar_configurações():
        pass
