import sqlite3 as db

class Model:
        # Init
        def __init__(self):
                # Abrir conexão
                self.server = "banco.db"
                
                self.con = db.connect(self.server)
                self.con.execute("PRAGMA foreign_keys = ON")
                
                self.cur = self.con.cursor()
                # Criar tabela
                self.cur.execute('''CREATE TABLE IF NOT EXISTS pessoas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        id_pai INTEGER,
                        id_mae INTEGER,
                        descricao TEXT,
                        passagem_biblica TEXT,
                        
                        FOREIGN KEY (id_pai)
                                REFERENCES pessoas(id)
                                ON DELETE SET NULL,
                        
                        FOREIGN KEY (id_mae)
                                REFERENCES pessoas(id)
                                ON DELETE SET NULL
                        );'''
                )
        
        # Consulta
        def pesquisar_pessoa(self, id, nome, id_pai, nome_pai, id_mae, nome_mae, descricao, passagem):
                # Conexão e cursor local
                conexao_local = db.connect(self.server)
                conexao_local.execute("PRAGMA foreign_keys = ON")
                
                cursor_local = conexao_local.cursor()
                
                # Montando consulta
                ## Definincdo extrutura da tabela
                comando = """
                        SELECT
                                p.id,
                                p.nome,
                                pai.id AS id_pai,
                                pai.nome AS nome_pai,
                                mae.id AS id_mae,
                                mae.nome AS nome_mae,
                                p.descricao,
                                p.passagem_biblica
                        FROM pessoas p
                        LEFT JOIN pessoas pai ON p.id_pai = pai.id
                        LEFT JOIN pessoas mae ON p.id_mae = mae.id
                        Where
                                1=?"""
                parametros = [1]
                ## Adicionando condições
                ### Ids
                if id != '':
                        comando += """
                                AND p.id = ?"""
                        parametros.append(id)
                if id_pai != '':
                        comando += """
                                AND pai.id = ?"""
                        parametros.append(id_pai)
                if id_mae != '':
                        comando += """
                                AND mae.id = ?"""
                        parametros.append(id_mae)
                
                ### Nomes
                if nome != '':
                        comando += """
                                AND p.nome LIKE ?"""
                        parametros.append(f"%{nome}%")
                if nome_pai != '':
                        comando += """
                                AND pai.nome LIKE ?"""
                        parametros.append(f"%{nome_pai}%")
                if nome_mae != '':
                        comando += """
                                AND mae.nome LIKE ?"""
                        parametros.append(f"%{nome_mae}%")
                
                ### Textos
                if descricao != '':
                        comando += """
                                AND p.descricao LIKE ?"""
                        parametros.append(f"%{descricao}%")
                if passagem != '':
                        comando += f"""
                                AND p.passagem_biblica LIKE ?"""
                        parametros.append(f"%{passagem}%")
                
                ## Adicionando ORDER BY
                comando += """
                        ORDER BY p.id ASC;"""
                
                # Executando consulta a o banco de dados
                cursor_local.execute(comando, parametros)
                fet = cursor_local.fetchall()
                
                # Fechando cursor e conexão locais
                cursor_local.close()
                conexao_local.close()
                
                # Retornando consulta
                return fet
                
                # Tratamento de excessão
                """
                except:
                        print('Erro')
                        resultado = []
                finally:
                        conexao_local.close()
                        cursor_local.close()
                """
                
                # Retornando resultado formatado
                """
                resultado = []
                #
                for item in fet:
                        resultado.append([
                                f'{str(item[0]):4} - {item[1]}',
                                f'{str(item[2]):4} - {item[3]}',
                                f'{str(item[4]):4} - {item[5]}',
                                item[6],
                                item[7],
                        ])
                return resultado
                """
        
        # Eclusão
        def excluir_registro(self, id:int):
                self.cur.execute('DELETE FROM pessoas WHERE id = ?', (id,))
                self.con.commit()
        
        # Retorna todos os registro da tabela
        def get_todos_registros(self):
                self.cur.execute('SELECT id, nome, descricao, id_pai, id_mae, passagem_biblica FROM pessoas ORDER BY id ASC')
                fet = self.cur.fetchall()
                return fet
        
        # Recebe uma lista formatada da seguinte maneira: 'id - nome'
        def get_id_e_nomes(self):
                # Executando e armazenando consulta
                self.cur.execute('SELECT id, nome FROM pessoas ORDER BY id ASC')
                resultado_consulta = self.cur.fetchall()
                # Formatando resultado da consulta
                lista_formatada = []
                for registro in resultado_consulta:
                        lista_formatada.append(f'{registro[0]} - {registro[1]}')
                # Retornando resultado formatado
                return lista_formatada
        
        # Cadastra uma pessoa
        def cadastrar_registro(self, nome, id_pai, id_mae, descricao, passagem):
                self.cur.execute(
                        'INSERT INTO pessoas(nome, id_pai, id_mae, descricao, passagem_biblica) VALUES(?, ?, ?, ?, ?)',
                        (nome, id_pai, id_mae, descricao, passagem)
                )
                self.con.commit()
        
        # Edita uma registro de uma pessoa
        def editar_registro(self, id:int, nome:str, id_pai:int, id_mae:int, descricao:str, passagem:str):
                if id_pai == '':
                        id_pai = None
                if id_mae == '':
                        id_mae = None
                
                comando = '''UPDATE pessoas
                        SET
                                nome = ?,
                                id_pai = ?,
                                id_mae = ?,
                                descricao = ?,
                                passagem_biblica = ?
                        WHERE id = ?;'''
                parametros = (nome, id_pai, id_mae, descricao, passagem, id)
                self.cur.execute(comando, parametros)
                self.con.commit()
        
        # Fechar conexão
        def fechar_conexao(self):
                self.cur.close()
                self.con.close()
                #print('Conexão fechada')
        
        # Criar arvore
        def arvore(self, descricao=False, pais=False):
                return Arvore(self.cur, descricao, pais)

class Arvore():
        def __init__(self, cursor, descricao=False, pais=False):
                self.presencas = []
                self.arvore = ''
                
                self.mostrar_pais = pais
                self.mostrar_descricao = descricao
                
                self.cur = cursor
        
        # Get pais
        def pais(self, id_pai, id_mae):
                self.cur.execute("SELECT nome FROM pessoas WHERE id = ? OR id = ?", (id_pai, id_mae))
                
                pais = []
                
                for i in self.cur.fetchall():
                        for j in i:
                                pais.append(j)
                
                return ', '.join(pais)
        
        
        # Processa uma string com a árvore genealógica descendente de um pessoa
        def processar_arvore(self, identificador:int, pos:int=0, ultimo:bool =False):
                # Escrevendo as "setas" de referencia
                self.arvore += "│   "*(pos-1)
                if pos > 0:
                        if ultimo:
                                self.arvore += "└─"
                        else:
                                self.arvore += "├─"
                
                # --------------------------------
                # Escrevendo dados da pessoa atual ├│
                # Caso já tenha aparecido
                if identificador in self.presencas:
                        self.cur.execute('SELECT nome FROM pessoas WHERE id = ?', (identificador,))
                        nome = self.cur.fetchone()[0]
                        self.arvore += f' {nome}*\n  '
                # Caso não tenha aparecido
                else:
                        self.presencas.append(identificador)
                        # --------------------------------
                        # Nome, descricao e pais
                        if self.mostrar_descricao and self.mostrar_pais:
                                self.cur.execute('SELECT nome, descricao FROM pessoas WHERE id = ?', (identificador,))
                                nome, descricao = self.cur.fetchone()
                                
                                self.cur.execute('SELECT id, nome, id_pai, id_mae FROM pessoas WHERE id = ?', (identificador,))
                                dados = self.cur.fetchone()
                                pais = self.pais(dados[2], dados[3])
                                
                                self.arvore += f' {nome} {pais, descricao[:20]}\n  '
                        
                        # Nome e decricao
                        elif self.mostrar_descricao:
                                self.cur.execute('SELECT nome, descricao FROM pessoas WHERE id = ?', (identificador,))
                                nome, descricao = self.cur.fetchone()
                                #self.arvore += f' {nome} ({descricao[:20]})\n  '
                                if descricao:
                                        self.arvore += f' {nome.upper()}   →   {descricao}\n  '
                                else:
                                        self.arvore += f' {nome}\n  '
                        
                        # Nome e pais
                        elif self.mostrar_pais:
                                self.cur.execute('SELECT id, nome, id_pai, id_mae FROM pessoas WHERE id = ?', (identificador,))
                                dados = self.cur.fetchone()
                                self.arvore += f" {dados[1]} ({self.pais(dados[2], dados[3])})\n  "
                        
                        # Somente nome
                        else:
                                self.cur.execute('SELECT nome FROM pessoas WHERE id = ?', (identificador,))
                                nome = self.cur.fetchone()[0]
                                self.arvore += f' {nome}\n  '
                        
                        # --------------------------------
                        # Aplicando recursividade nos filhos
                        self.cur.execute("SELECT id FROM pessoas WHERE id_pai = ? OR id_mae = ? ORDER BY id", (identificador, identificador,))
                        descendentes = self.cur.fetchall()
                        # Para cada descendente
                        for i in range(len(descendentes)):
                                        # Marca caso seja o ultimo
                                        if descendentes[i] == descendentes[-1]:
                                                self.processar_arvore(descendentes[i][0], pos+1, ultimo=True)
                                        else:
                                                self.processar_arvore(descendentes[i][0], pos+1)
        
        
        # Reset e retorno da árvore
        def resetar_arvore(self):
                self.arvore = ''
                self.presencas = []
        
        
        def get_arvore_str(self):
                # Formatar árvore
                linhas = self.arvore.split('\n')
                arv_format = []
                
                # Para cada linha, em seguida, para cada letra
                for y in range(len(linhas)):
                        arv_format.append([])
                        for x in range(len(linhas[y])):
                                # Se letra atual for barra
                                arv_format[y].append(linhas[y][x])
                                if arv_format[y][x] == "│":
                                        # Verifica qual a letra de cima
                                        if arv_format[y-1][x] == '└' or arv_format[y-1][x] == ' ':
                                                #linhas[y][x] = 'X'
                                                arv_format[y][x] = ' '#҈֍■□█  ▓
                                #print(novas_linhas[y][x], end='')
                        #print('')
                
                # Juntando os caracteres soltos
                for i in range(len(arv_format)):
                        arv_format[i] = ''.join(arv_format[i])
                arv_format = '\n'.join(arv_format)
                
                # Enviar árvore
                return arv_format
