from wtforms import Form
from wtforms import StringField, FloatField, EmailField, PasswordField, IntegerField, RadioField, DecimalField
from wtforms import validators

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
         validators=[validators.DataRequired(message='Debes seleccionar una figura Papu')])

    dato1 = DecimalField('Dato 1', [validators.Optional()], places=2, default=0)
    # places = 2 // Muestra 2 decimales
                         
    dato2 = DecimalField('Dato 2', [validators.Optional()], places=2, default=0)