from flask import Flask, render_template, request
import forms
import math

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello Papu"

@app.route('/Alumnos', methods=['GET', 'POST'])
def alumnos():
    mat = 0
    nom = ""
    ape = ""
    ema = ""
    alumnos_clase = forms.UserForm(request.form)

    if request.method == 'POST' and alumnos_clase.validate():
        mat = alumnos_clase.matricula.data
        nom = alumnos_clase.nombre.data
        ape = alumnos_clase.apellidos.data
        ema = alumnos_clase.email.data
    return render_template ('alumnos.html', form = alumnos_clase, mat=mat, nom=nom, ape=ape, ema=ema)

@app.route('/figuras', methods = ['GET', 'POST'])
def figuras():
    area = None
    figura = None
    form = forms.FigurasForm(request.form)

    if request.method == 'POST' and form.validate():
        figuraSel = form.figuraSel.data
        
        try:
            dato1 = float(form.dato1.data)
            dato2 = float(form.dato2.data)
            if figuraSel == 'triangulo':
                area = 0.5 * dato1 * dato2
                figura = 'Triángulo'
            elif figuraSel == 'rectangulo':
                area = dato1 * dato2
                figura = 'Rectángulo'
            elif figuraSel == 'circulo':
                area = math.pi * (dato1 ** 2)
                figura = 'Círculo'
            elif figuraSel == 'pentagono':
                lado = dato1
                apotema = lado / (2 * math.tan(math.radians(36)))
                perimetro = 5 * lado
                area = (perimetro * apotema) / 2
                figura = 'Pentágono'

        except ValueError:
            pass 

        except Exception as e:
            print(f"Ocurrió un error: {e}")

    return render_template('figuras.html', area=area, figura=figura, form=form)

@app.route("/index")
def index():

    titulo= "IEVN1003 - PWA"
    listado= ["Opera 1", "Opera 2","Opera 3", "Opera 4"]

    return render_template('/index.html', titulo = titulo, listado = listado)

@app.route('/distancia')
def distancia():
    return render_template('/distancia.html')

@app.route('/operas', methods= ['GET', 'POST'])
def operas():

    resultado = 0   

    if request.method == 'POST':
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')
        resultado = float(n1)+float(n2)

    return render_template('/operas.html', resultado = resultado)

@app.route('/about')
def about():
    return "<h1>This is about the page<h1/>"

@app.route("/numero/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID {} nombre: {}".format(id, username)

@app.route("/suma/<float:n1>/<float:n2>")
def func(n1, n2):
    return "La suma: {}".format(n1 + n2)

@app.route("/prueba")
def prueba():
    return """
    <h1>Prueba de HTML<h1/>
    <p>Esto es una prueba</p>
    <ul>
        <li>Elemento 1</li>
        <li>Elemento 2</li>
        <li>Elemento 3</li>
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True)