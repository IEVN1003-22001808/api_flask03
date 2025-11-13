from wtforms import Form
from wtforms import StringField, FloatField, EmailField, PasswordField, IntegerField, RadioField, DecimalField, BooleanField
from wtforms import validators
from wtforms.validators import NumberRange
 
class UserForm(Form):
    matricula = IntegerField('Matricula',
        [validators.DataRequired(message = "Papu, ocupamos tu matrícula pa doxxearte")])
    nombre = StringField('Nombre(s)',
        [validators.DataRequired(message = "Papu, ocupamos tu nombre pa doxxearte")])
    apellidos = StringField('Apellidos',
        [validators.DataRequired(message = "Papu, ocupamos tus apellidos pa doxxearte")])
    email = EmailField('Correo',
        [validators.Email(message = "Igrese el correo correspondiente")])
 
class FigurasForm(Form):
    opciones = [
        ('triangulo', 'Triángulo (Dato 1: Base, Dato 2: Altura)'),
        ('rectangulo', 'Rectángulo (Dato 1: Longitud, Dato 2: Anchura)'),
        ('circulo', 'Círculo (Dato 1: Radio)'),
        ('pentagono', 'Pentágono (Dato 1: Lado)')
    ]
 
    figuraSel = RadioField('Selecciona una figura', choices=opciones,
         validators=[validators.DataRequired(message='Debes seleccionar una figura, Papu')])
 
    dato1 = DecimalField('Dato 1', [validators.Optional()], places=2, default=0)
    # places = 2 // Muestra 2 decimales
                         
    dato2 = DecimalField('Dato 2', [validators.Optional()], places=2, default=0)
 
class PizzasForm(Form):
 
    nombre = StringField('Nombre', [
        validators.DataRequired(message="Papu, ocupamos tu nombre")
    ])
    direccion = StringField('Dirección', [
        validators.DataRequired(message="Papu, ocupamos tu dirección")
    ])
    telefono = IntegerField('Teléfono', [
        validators.DataRequired(message="Papu, ocupamos tu teléfono")
    ])
    opciones_tamanio = [
    ('Chica', 'Chica $40'),
    ('Mediana', 'Mediana $80'),
    ('Grande', 'Grande $120')
    ]
    tamanio = RadioField('Tamaño Pizza',
        choices=opciones_tamanio,
        validators=[validators.DataRequired(message='Debes seleccionar un tamaño de pizza, Papu')]
    )
    jamon = BooleanField('Jamón $10')
    pinia = BooleanField('Piña $10')
    champiniones = BooleanField('Champiñones $10')
   
    num_pizzas = IntegerField('Num. de Pizzas', [
        validators.DataRequired(message='¿Cuántas pizzas quieres?'),
        validators.NumberRange(min=1, message='Debe ser al menos 1 pizza')
    ])