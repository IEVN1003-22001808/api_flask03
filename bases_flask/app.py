from flask import Flask, render_template, request
from flask import make_response, jsonify
import json
import forms
import math
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
 
@app.route('/')
def home():
    return "Hello Papu"
 
@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    mat = 0
    nom = ""
    ape = ""
    ema = ""
    alumnos_clase = forms.UserForm(request.form)
 
    datos_str = request.cookies.get('estudiante')
    if datos_str:
        try:
            lista_estudiantes = json.loads(datos_str)
            if isinstance(lista_estudiantes, dict):
                lista_estudiantes = [lista_estudiantes]
            elif not isinstance(lista_estudiantes, list):
                 lista_estudiantes = []
                 
        except (json.JSONDecodeError, TypeError):
            lista_estudiantes = []
    else:
        lista_estudiantes = []
 
    if request.method == 'POST' and alumnos_clase.validate():
        mat = alumnos_clase.matricula.data
        nom = alumnos_clase.nombre.data
        ape = alumnos_clase.apellidos.data
        ema = alumnos_clase.email.data
        datos = {"Matrícula":mat, "Nombre(s)":nom, "Apellidos":ape, "Correo":ema}
 
        lista_estudiantes.append(datos)
   
    response = make_response(render_template('alumnos.html', form=alumnos_clase, mat=mat, nom=nom, ape=ape, ema=ema))
    response.set_cookie('estudiante', json.dumps(lista_estudiantes))
    return response
 
@app.route("/get_cookie")
def get_cookie():
    datos_str=request.cookies.get('estudiante')
    if not datos_str:
        return"No hay cookies"
    datos=json.loads(datos_str)
    return jsonify(datos)
 
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
 
@app.route('/pizzas', methods=['GET', 'POST'])
def pizzas():
   
    try:
        cliente_actual = json.loads(request.cookies.get('cliente_actual'))
    except (json.JSONDecodeError, TypeError):
        cliente_actual = {}
    if not isinstance(cliente_actual, dict):
        cliente_actual = {}
 
    try:
        pedido_actual = json.loads(request.cookies.get('pedido_actual'))
    except (json.JSONDecodeError, TypeError):
        pedido_actual = []
    if not isinstance(pedido_actual, list):
        pedido_actual = []
 
    try:
        ventas_dia = json.loads(request.cookies.get('ventas_dia'))
    except (json.JSONDecodeError, TypeError):
        ventas_dia = {}
    if not isinstance(ventas_dia, dict):
        ventas_dia = {}
   
    mostrar_Ventas = False
 
    if request.method == 'GET' and cliente_actual:
        form = forms.PizzasForm(data=cliente_actual)
    else:
        form = forms.PizzasForm(request.form)
 
    if request.method == 'POST':
        accion = request.form.get('accion')
 
        #         BOTÓN "AGREGAR"
        if accion == 'agregar' and form.validate():
 
            cliente_actual = {
                'nombre': form.nombre.data,
                'direccion': form.direccion.data,
                'telefono': form.telefono.data
            }
 
            precios_tam = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
            tam = form.tamanio.data
            num = form.num_pizzas.data
           
            subtotal_ingredientes = 0
            ing_lista = []
           
            if form.jamon.data:
                subtotal_ingredientes += 10
                ing_lista.append('Jamón')
            if form.pinia.data:
                subtotal_ingredientes += 10
                ing_lista.append('Piña')
            if form.champiniones.data:
                subtotal_ingredientes += 10
                ing_lista.append('Champiñones')
           
            subtotal_por_pizza = precios_tam.get(tam, 0) + subtotal_ingredientes
            subtotal_final = subtotal_por_pizza * num
           
            pizza_nueva = {'tamanio': tam, 'ingredientes': ing_lista, 'num_pizzas': num, 'subtotal': subtotal_final}
           
            pedido_actual.append(pizza_nueva)
            print(f"LOG: Pizza agregada: {pizza_nueva}")
 
        #         BOTÓN "QUITAR"
        elif accion == 'quitar':
            indice_str = request.form.get('indice_pizza')
           
            if indice_str and indice_str.isdigit():
                indice = int(indice_str)
               
                if 0 <= indice < len(pedido_actual):
                    pizza_quitada = pedido_actual.pop(indice)
                    print(f"LOG: Pizza en índice {indice} quitada: {pizza_quitada}")
                else:
                    print(f"ERROR: Índice de 'quitar' fuera de rango: {indice}")
            else:
                print(f"ERROR: Índice de 'quitar' no es un número: {indice_str}")
 
        #         BOTÓN "TERMINAR"
        elif accion == 'terminar':
            nombre_cliente = cliente_actual.get('nombre')
 
            if not pedido_actual:
                print("LOG: Intento de terminar, pero el pedido está vacío.")
            elif not nombre_cliente:
                print("ERROR: Faltan datos del cliente para terminar el pedido.")
           
            else:
                total_final = sum(pizza.get('subtotal', 0) for pizza in pedido_actual)
                ventas_dia[nombre_cliente] = ventas_dia.get(nombre_cliente, 0) + total_final
               
                pedido_actual = []
                cliente_actual = {}
               
                print(f"LOG: Pedido terminado. Venta registrada: {ventas_dia}")
       
        #         BOTÓN "MOSTRAR VENTAS"
        elif accion == 'mostrar_ventas':
            mostrar_Ventas = True
            print("LOG: Mostrando panel de ventas.")
 
        #         BOTÓN "LIMPIAR"
        elif accion == 'adios_popo':
            pedido_actual = []
            ventas_dia = {}
            cliente_actual = {}
            mostrar_Ventas = False
            form = forms.PizzasForm()
            print("LOG: Cookies limpiadas (pedido, ventas y cliente).")
 
   
    response = make_response(
        render_template('pizzas.html', form=form, pedido_actual=pedido_actual, ventas_dia=ventas_dia,mostrar_Ventas=mostrar_Ventas) # <-- Pasamos la nueva variable
    )
   
    response.set_cookie('pedido_actual', json.dumps(pedido_actual))
    response.set_cookie('ventas_dia', json.dumps(ventas_dia))
    response.set_cookie('cliente_actual', json.dumps(cliente_actual))
    return response
 
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
    return
    """
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
