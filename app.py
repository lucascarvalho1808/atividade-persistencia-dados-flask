from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Nome do ficheiro de texto para persistência dos dados
FICHEIRO_DADOS = 'mensagens.txt'

# --- Funções de Manipulação do Ficheiro ---
def ler_mensagens():
   """Lê as mensagens guardadas no ficheiro de texto."""
   if os.path.exists(FICHEIRO_DADOS):
       with open(FICHEIRO_DADOS, 'r', encoding='utf-8') as f:
           # Remove espaços em branco e ignora linhas vazias
           return [linha.strip() for linha in f if linha.strip()]
   return []


def guardar_mensagem(nome, mensagem):
   """Adiciona uma nova linha ao final do ficheiro (Modo 'a' - Append)."""
   with open(FICHEIRO_DADOS, 'a', encoding='utf-8') as f:
       f.write(f"{nome}: {mensagem}\n")


def apagar_mensagens():
    """Apaga todas as mensagens do arquivo mensagens.txt"""
    with open('mensagens.txt', 'w', encoding='utf-8') as arquivo:
        pass  

# --- Aqui estão as rotas da Aplicação ---
@app.route("/", methods=['GET', 'POST'])
def livro_mensagem():
   if request.method == 'POST':
       # Captura os dados do formulário de envio
       nome = request.form.get('nome')
       mensagem = request.form.get('mensagem')
      
       if nome and mensagem:
           guardar_mensagem(nome, mensagem)
          
       # Redireciona para o GET da própria página
       return redirect(url_for('livro_mensagem'))


   # No método GET, lemos os dados para exibir na página
   mensagens = ler_mensagens()
   return render_template("index.html", mensagens=mensagens)

@app.route('/confirmar-limpeza', methods=['GET'])
def confirmar_limpeza():
    """Exibe a página de confirmação antes de apagar"""
    return render_template('confirmar.html')

@app.route('/limpar', methods=['POST'])
def limpar_dados():
    """Apaga todas as mensagens e redireciona para a página inicial"""
    apagar_mensagens()
    return redirect(url_for('livro_mensagem'))