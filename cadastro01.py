
from tkinter import *
from tkinter import ttk
from awesometkinter import * 
import awesometkinter as atk
import sqlite3
from tkinter import font

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

root = Tk()

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def geraRelatorioCliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entrey.get()
        self.nomeRel = self.nome_entrey.get()
        self.telefoneRel = self.telefone_entrey.get()
        self.cidadeRel = self.cidade_entrey.get()

        self.c.setFont("Helvetica-Bold", 20)
        self.c.drawString(200, 790, 'Ficha de Cadastro ')

        self.c.setFont("Helvetica-Bold", 14) ##Fonte do PDF
        self.c.drawString(50, 700, 'CÓDIGO:')
        self.c.drawString(180,700, 'NOME:')
        self.c.drawString(50, 674, 'CIDADE:')
        self.c.drawString(50, 648, 'FONE:')

        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawString(130, 700, self.codigoRel)
        self.c.drawString(230, 700, self.nomeRel)
        self.c.drawString(115, 674, self.cidadeRel)
        self.c.drawString(115, 648, self.telefoneRel)

        self.c.rect(30, 625, 550, 190, fill=False, stroke=True ) ## cria um retangulo no PDF
        self.c.rect(40, 697, 130, 18, fill=False, stroke=True ) ## cria um retangulo no Codigo
        self.c.rect(178, 697, 350, 18, fill=False, stroke=True ) ## cria um retangulo no Nome
        self.c.rect(40, 670, 320, 18, fill=False, stroke=True ) ## cria um retangulo no cidade
        self.c.rect(40, 644, 200, 18, fill=False, stroke=True ) ## cria um retangulo no Telefone




        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():
    def limpaTela(self):
        self.codigo_entrey.delete(0,END)
        self.nome_entrey.delete(0,END)
        self.telefone_entrey.delete(0,END)
        self.cidade_entrey.delete(0,END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor();
        print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close();
        print("Desconectando ao banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        ### Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)               
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()
    def variaveis(self):
        self.codigo = self.codigo_entrey.get()
        self.nome = self.nome_entrey.get()
        self.telefone = self.telefone_entrey.get()
        self.cidade = self.cidade_entrey.get()
        self.conecta_bd()  # conecta ao banco de dados
    def add_cliente(self):  # adiciona os valores ao banco de dados digitados na tela
        self.variaveis()
        self.conecta_bd()  # conecta ao banco de dados

        self.cursor.execute(""" INSERT INTO clientes(nome_cliente, telefone, cidade)
         VALUES(?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()  # validar os dados
        self.desconecta_bd()
        self.select_lista()
        self.limpaTela()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes 
        ORDER BY nome_cliente ASC; """)  # cod, nome_cliente, telefone, cidade
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def busca_Cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.nome_entrey.insert(END,'%')
        nome = self.nome_entrey.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente  LIKE '%s' ORDER BY nome_cliente ASC  """ % nome )
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END,values=i)
        self.limpaTela()
        self.desconecta_bd()

    def Duploclick(self, event):
        self.limpaTela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n,'values')
            self.codigo_entrey.insert(END, col1)
            self.nome_entrey.insert(END, col2)
            self.telefone_entrey.insert(END, col3)
            self.cidade_entrey.insert(END, col4)
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpaTela()
        self.select_lista()
    def alterar_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
            WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpaTela()

class Application(Funcs, Relatorios):
    def __init__(self, ):
        self.root = root
        self.tela()
        self.freme_da_tela()
        self.criando_botoes()
        self.criando_label_entrada_codigo()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()

    def tela(self):
        self.root.title("cadastro de Clientes")
        self.root.configure(background='#1e3743')
        self.root.geometry("700x600")
        self.root.resizable(True,True)
        self.root.maxsize(width=1024, height=768)
        self.root.minsize(width=640, height=480)
    def freme_da_tela(self):
       
        ## Frames 1 e 2 
        self.frame_1 = Frame(self.root, bd = 4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_1.place(relx= 0.02, rely= 0.02, relwidth= 0.96 , relheight= 0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee' , highlightbackground='#759fe6', highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def criando_botoes(self):

        ### Abas do frame 1
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)
 
        self.aba1.configure(background = "#dfe3ee",  )
        self.aba2.configure(background = "lightgray",  )

        self.abas.add(self.aba1, text = 'DADOS DO CLIENTE  ' )
        self.abas.add(self.aba2, text = "ABA 2 ")
    

        self.abas.place(relx= 0, rely= 0, relwidth= 1 , relheight= 1)

        ### Criação do botão limmpar.
        self.bt_limpar = Button (self.aba1, text='Limpar', bd=3, bg='#4F4F4F', fg='white', font= ("verdana" ,8,"bold"), command= self.limpaTela)
        self.bt_limpar.place(relx=0.25, rely=0.08, relwidth=0.1, relheight=0.14)
        
        ### Criação do botão buscar.
        
        self.bt_buscar = Button(self.aba1, text='Buscar', bd=3, bg='#4F4F4F', fg='white', font= ("verdana" ,8,"bold"), command=self.busca_Cliente )
        self.bt_buscar.place(relx=0.15, rely=0.08, relwidth=0.1, relheight=0.14)
       
        ###Balão de mensagem Botaão buscar

        atk.tooltip(self.bt_buscar,"Para realizar uma busca digite o nome do cliente! ")
      
        ### Criação do botão novo.

        self.bt_novo = Button(self.aba1, text='Novo', bd=3, bg='#4F4F4F', fg='white', font= ("verdana" ,8,"bold"), command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.08, relwidth=0.1, relheight=0.14)
       
        ### Criação do botão alterar.
       
        self.bt_alterar = Button(self.aba1, text='Alterar', bd=3, bg='#4F4F4F', fg='white', font= ("verdana" ,8,"bold"), command=self.alterar_cliente )
        self.bt_alterar.place(relx=0.7, rely=0.08, relwidth=0.1, relheight=0.14)
       
        ##Balão de mensagem Botaão alterar
        
        atk.tooltip(self.bt_alterar,"Para alterar os dados, selecione os dados do cliente desejado clicando duas vezes.")
        
        ### Criação do botão apagar.
       
        self.bt_apagar = Button(self.aba1, text='Apagar', bd=3, bg='#4F4F4F', fg='white', font= ("verdana" ,8,"bold"), command=self.deleta_cliente )
        self.bt_apagar.place(relx=0.8, rely=0.08, relwidth=0.1, relheight=0.14,)
    def criando_label_entrada_codigo(self):
        ###criação da laebl e da entrada  do código.
        self.lb_codigo = Label(self.aba1, text = 'Código', bd=0, bg='#dfe3ee', fg='black', font= ("verdana" ,10,"bold"))
        self.lb_codigo.place(relx=0.04, rely=0.08, )
        self.codigo_entrey = Entry(self.aba1, bg='#c0c0c0', fg='black', font=("verdana" ,8,"bold") )
        self.codigo_entrey.place(relx=0.04, rely=0.19,relwidth=0.06, relheight=0.08, )

        ###criação da laebl e da entrada  do nome.
        self.lb_nome = Label(self.aba1, text='Nome', bd=0, bg='#dfe3ee', fg='black', font= ("verdana" ,10,"bold"))
        self.lb_nome.place(relx=0.04, rely=0.40)
        self.nome_entrey = Entry(self.aba1,  bg='#c0c0c0', fg='black', font=("verdana" ,8,"bold"))
        self.nome_entrey.place(relx=0.04, rely=0.50, relwidth=0.85, relheight=0.08)

        ###criação da laebl e da entrada  do tolefone.
        self.lb_telefone = Label(self.aba1, text='Telefone', bd=0, bg='#dfe3ee', fg='black', font= ("verdana" ,10,"bold"))
        self.lb_telefone.place(relx=0.04, rely=0.65)
        self.telefone_entrey = Entry(self.aba1,  bg='#c0c0c0', fg='black', font=("verdana" ,8,"bold"))
        self.telefone_entrey.place(relx=0.04, rely=0.75, relwidth=0.33, relheight=0.08, )

        ###criação da laebl e da entrada  do cidade.
        self.lb_cidade = Label(self.aba1, text='Cidade', bd=0, bg='#dfe3ee', fg='black', font= ("verdana" ,10,"bold"))
        self.lb_cidade.place(relx=0.45, rely=0.65)
        self.cidade_entrey = Entry(self.aba1, bg='#c0c0c0', fg='black', font=("verdana" ,8,"bold") )
        self.cidade_entrey.place(relx=0.45, rely=0.75, relwidth=0.44, relheight=0.08, )
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=("col1", 'col2', 'col3', 'col4'))
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='Código')
        self.listaCli.heading('#2', text='Nome')
        self.listaCli.heading('#3', text='Telefone')
        self.listaCli.heading('#4', text='Cidade')

        self.listaCli.column('#0', width=1)
        self.listaCli.column('#1', width=50)
        self.listaCli.column('#2', width=200)
        self.listaCli.column('#3', width=125)
        self.listaCli.column('#4', width=125)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.90)
        ###Barra de bolagem.
        self.scroolLista = Scrollbar(self.frame_2, orient="vertical")
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.90)
        self.listaCli.bind("<Double-1>", self.Duploclick)
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu= menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade( label= "Opções", menu= filemenu )
        menubar.add_cascade(label= "Relatórios", menu= filemenu2)

        filemenu.add_command(label="Sair")
        filemenu.add_command(label= "Limpa Tela", command= self.limpaTela)

        filemenu2.add_command(label= "Ficha do cliente", command= self.geraRelatorioCliente)

        



Application()
