from flask import Flask, render_template, request, url_for, redirect


from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.secret_key = 'String aleatoria'

engine = create_engine("sqlite:///lab05.sqlite")
Session = sessionmaker(bind=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

Pessoa = Base.classes.Pessoa
Telefones = Base.classes.Telefones


@app.route('/')
def inicial():
    return render_template('index.html')

@app.route('/listar')
def listar_pessoas():
    sessionSQL = Session()
    pessoas = sessionSQL.query(Pessoa).all()
    sessionSQL.close()

    return render_template('listar.html', lista=pessoas)

@app.route('/inserir', methods=['POST', 'GET'])
def cadastrar_pessoas():

    if request.method == 'GET':
        return render_template('inserir.html')
    else:
        sessionSQL = Session()
        nome = request.form['nome']

        pessoa = Pessoa()

        pessoa.nome = nome

        sessionSQL.add(pessoa)
        sessionSQL.commit()
        sessionSQL.close()

        return redirect(url_for('listar_pessoas'))
        # return listar_pessoas()

@app.route('/excluir', methods=['POST', 'GET'])
def excluir_pessoa():
    sessionSQL = Session()
    idPessoa = str(request.args.get('id'))

    if request.method == 'GET':
        linha = sessionSQL.query(Pessoa).filter(Pessoa.idPessoa == idPessoa).first()

        if linha is None:
            return redirect(url_for('listar_pessoas'))

        return render_template('excluir.html',pessoa=linha)
    else:
        idPessoa = request.form['id']
        linha = sessionSQL.query(Pessoa).filter(Pessoa.idPessoa == idPessoa).first()

        linha.telefones_collection[:] = []

        sessionSQL.delete(linha)
        sessionSQL.commit()
        sessionSQL.close()

        return redirect(url_for('listar_pessoas'))

@app.route('/editar',  methods=['POST', 'GET'])
def editar_pessoa():
    sessionSQL = Session()

    if request.method == 'GET':

        idPessoa = str(request.args.get('id'))
        linha = sessionSQL.query(Pessoa).filter(Pessoa.idPessoa == idPessoa).first()

        if linha is None:
            return redirect(url_for('listar_pessoas'))

        return render_template('editar.html', pessoa=linha)
    else:

        idPessoa = request.form['id']

        linha = sessionSQL.query(Pessoa).filter(Pessoa.idPessoa == idPessoa).first()

        nome = request.form['nome']

        # Atualizando o nome
        linha.nome = nome

        for campo in request.form.items():
            if 'tele-' in campo[0]:
                idTelefone = campo[0].split('-')[1]
                idTelefone = int(idTelefone)
                for telefone in linha.telefones_collection:
                    if telefone.idTelefone == idTelefone:
                        telefone.numero = campo[1]

        sessionSQL.commit()
        sessionSQL.close()

        return redirect(url_for('listar_pessoas'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
