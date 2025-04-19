import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://localhost:8000"  # URL da sua API

def listar_contas():
    resposta = requests.get(f"{API_URL}/contas")
    if resposta.status_code == 200:
        contas = resposta.json()
        lista_contas.delete(0, tk.END)
        for conta in contas:
            texto = f"{conta['id_conta']} - {conta['nome_titular']} (Saldo: R${conta['saldo']})"
            lista_contas.insert(tk.END, texto)
    else:
        messagebox.showerror("Erro", "Erro ao buscar contas")

def criar_conta():
    dados = {
        "saldo": float(entry_saldo.get()),
        "tipo_chave_pix": entry_tipo_pix.get(),
        "chave_pix": entry_pix.get(),
        "nome_titular": entry_nome.get(),
        "data_nascimento": entry_nascimento.get(),
        "numero_agencia": entry_agencia.get(),
        "numero_conta": entry_conta.get(),
        "numero_banco": entry_banco.get(),
        "instituicao_bancaria": entry_banco_nome.get(),
        "cpf": entry_cpf.get()
    }
    
    resposta = requests.post(f"{API_URL}/contas", json=dados)
    if resposta.status_code == 200:
        messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
        listar_contas()
    else:
        messagebox.showerror("Erro", "Erro ao criar conta")

# GUI
janela = tk.Tk()
janela.title("ARDIU")
janela.geometry("1000x1000")






tk.Label(janela, text="Nome do Titular").pack()
entry_nome = tk.Entry(janela)
entry_nome.pack()

tk.Label(janela, text="CPF").pack()
entry_cpf = tk.Entry(janela)
entry_cpf.pack()

tk.Label(janela, text="Data de Nascimento (YYYY-MM-DD)").pack()
entry_nascimento = tk.Entry(janela)
entry_nascimento.pack()

tk.Label(janela, text="Saldo Inicial").pack()
entry_saldo = tk.Entry(janela)
entry_saldo.pack()

tk.Label(janela, text="Tipo Chave Pix").pack()
entry_tipo_pix = tk.Entry(janela)
entry_tipo_pix.pack()

tk.Label(janela, text="Chave Pix").pack()
entry_pix = tk.Entry(janela)
entry_pix.pack()

tk.Label(janela, text="Número Agência").pack()
entry_agencia = tk.Entry(janela)
entry_agencia.pack()

tk.Label(janela, text="Número Conta").pack()
entry_conta = tk.Entry(janela)
entry_conta.pack()

tk.Label(janela, text="Número Banco").pack()
entry_banco = tk.Entry(janela)
entry_banco.pack()

tk.Label(janela, text="Instituição Bancária").pack()
entry_banco_nome = tk.Entry(janela)
entry_banco_nome.pack()

tk.Button(janela, text="Criar Conta", command=criar_conta).pack(pady=10)
tk.Button(janela, text="Listar Contas", command=listar_contas).pack(pady=5)

lista_contas = tk.Listbox(janela)
lista_contas.pack(fill=tk.BOTH, expand=True)

janela.mainloop()
