from tkinter.ttk import *
from tkinter import *
from tkinter import ttk,messagebox
import mysql.connector
from mysql.connector import Error


janela = Tk()
janela.geometry('1200x600')


entradaNome = Entry(janela)
entradaNome.place(relx=0, rely= 0.04, height=30)
entradaNomeTexto = Label(janela, text='INSIRA NOME:')
entradaNomeTexto.place(relx=0, rely=0)


entradaDN = Entry(janela)
entradaDN.place(relx= 0.15, rely= 0.04, width=180, height=30,)
entradaDNTexto = Label(janela, text='INSIRA SUA DATA NASCIMENTO:')
entradaDNTexto.place(relx=0.15, rely=0)

combo = Combobox(janela)
combo['values'] = ['MASCULINO', 'FEMININO']
combo.place(relx=0.35, rely= 0.04)
comboTexto = Label(janela, text='INSIRA O SEXO:')
comboTexto.place(relx=0.35, rely= 0)



comboCidade = Combobox(janela)
comboCidade['values'] = ['SANTA CRUZ DO SUL', 'VENANCIO AIRES', 'CRUZEIRO', 'PORTO ALEGRE']
comboCidade.place(relx=0.50, rely= 0.04)
comboCtexto = Label(janela, text='INSIRA SUA CIDADE')
comboCtexto.place(relx=0.50, rely=0)



con = mysql.connector.connect(
host='localhost',
database='colegio3',
user='root',
password=''
)

#/////////////////////////adicionar no TV/////////////////////////////
def adicionar_treeview():

        consulta_sql = "SELECT * FROM cliente"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()

        for item in tv.get_children():
            tv.delete(item)

        for linha in linhas:
            tv.insert('', 'end', values=linha)


def deletar():
    seletado = tv.selection()
    if seletado:
        item = seletado[0]
        excluir = tv.item(item, "text")

        con = mysql.connector.connect(
            host='localhost',
            database='colegio3',
            user='root',
            password=''
        )
        cursor = con.cursor()
        cursor.execute("DELETE FROM cliente WHERE idCliente = %s", (excluir,))

        con.commit()

        con.close
#//////////////////////////////treeview//////////////////////////////

tv = Treeview(janela, columns=("id","NOME","DATA NASCIMENTO","SEXO","CIDADE"), show='headings')


tv.heading("#1", text="id")
tv.heading("#2", text="nomeCliente")
tv.heading("#3", text="dataDeNascimento")
tv.heading("#4", text="idSexo")
tv.heading("#5", text="idCidade")

tv.column("#1", width=50)
tv.column("#2", width=150)
tv.column("#3", width=50)
tv.column("#4", width=50)
tv.column("#5", width=100)

tv.place(relx=0,rely=0.1, width=1000, height=400)


#////////////////ADICIONAR NO BANCO////////////////////////////////////
def adicionar():
    try:
        sexo = combo.get()
        nome = entradaNome.get()
        idade = entradaDN.get()
        cidade = comboCidade.get()

        if sexo == 'MASCULINO':
            sexo = 1
        elif sexo == 'FEMININO':
            sexo = 2

        if cidade == 'SANTA CRUZ DO SUL':
            cidade = 1
        elif cidade == 'VENANCIO AIRES':
            cidade = 2
        elif cidade == 'CRUZEIRO':
            cidade = 3
        elif cidade == 'PORTO ALEGRE':
            cidade = 4
        
        inserir_clientes = f"""INSERT INTO cliente
                                (nomeCliente, dataNascimentoCliente, idSexo, idCidade)
                                VALUES
                                ("{nome}", "{idade}", {sexo},{cidade})
                            """
        cursor = con.cursor()
        cursor.execute(inserir_clientes)
        con.commit()
        messagebox.showinfo(title='PARABENS', message='ADICIONADO COM SUCESSO')
        cursor.close()
        entradaNome.delete(0,END)
        entradaDN.delete(0,END)
        comboCidade.delete(0,END)
        combo.delete(0,END)
        
        adicionar_treeview()
    except:
        if sexo == '' or nome == '' or idade == '' or cidade == '':
            messagebox.showerror(title='SELECIONE', message='SELECIONE O QUE SE PEDE')
    finally:
        pass

def deletar():
    seletado = tv.selection()
    if seletado:
        itemSelecionado = tv.selection()[0]
        valores = tv.item(itemSelecionado, 'values')

        con = mysql.connector.connect(
            host='localhost',
            database='colegio3',
            user='root',
            password=''
        )
        print(valores)


        cursor = con.cursor()
        cursor.execute("DELETE FROM cliente WHERE idCliente = %s", (valores))
        con.commit()
        con.close()


#////////////////////////////////botaos/////////////////////////////////


botao_inserir = Button(janela, text="INSERIR",width=15,height=7,command=adicionar)
botao_inserir.place(relx=0.86,rely=0.1)


botao_deletar = Button(janela, text="DELETAR",width=15,height=7, command=deletar)
botao_deletar.place(relx=0.86,rely=0.34)


botao_carregar = Button(janela, width=15, height=7,text="CARREGAR DADOS", command=adicionar_treeview)
botao_carregar.place(relx=0.86,rely=0.58)


mainloop()