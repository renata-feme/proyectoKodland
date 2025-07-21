from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    contrasena= db.Column(db.String(50), nullable=False)
    puntaje = db.Column(db.Integer, default=0)

    #atributos para las preguntas
    agua = db.Column(db.Float, default=0)
    luz = db.Column(db.Float, default=0)

    gasolina = db.Column(db.Float, default=0.0) #HAY QUE ACTUALIZAR


with app.app_context():
    db.create_all()

@app.route("/registro", methods=["GET", "POST"])  #methods, decorador de FLASK: dice qué tipo de solicitud acepta la url
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"] #request.form[]: guarda los datos enviados de un formulario (tipo diccionario, busca la key, debe coincidir con lo que esté en name)
        contrasena = request.form["contrasena"]
        nuevoUsuario = Usuario(nombre=nombre, contrasena=contrasena)
        db.session.add(nuevoUsuario)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("registro.html")

@app.route("/", methods=["GET", "POST"]) #decorador de FLASK: lit dice qué hacer (o mostrar) cuando se está en esa url
def login():
    if request.method == "POST":
        nombre = request.form["nombre"]
        contrasena = request.form["contrasena"]
        usuario = Usuario.query.filter_by(nombre=nombre, contrasena=contrasena).first() #.query : sistema de consultas

        if usuario:
            return redirect(f"/menu/{usuario.id}")
        else:
            error = "Usuario o contraseña incorrectos"
            return render_template("login.html", error=error) 
    return render_template("login.html")

@app.route("/menu/<int:id_usuario>", ) #pasamos el usuario de una página a otra
def menu(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    return render_template("menu.html", usuario=usuario)



#PREGUNTAS
@app.route("/p1/<int:id_usuario>", methods=["GET", "POST"]) #<int:id_usuario>:  se espera un número y se guarda como id_usuario
def p1(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario) #busca en la base de datos con ese id, si no lo encuentra manda error
    if request.method == "POST":
        agua = float(request.form.get("agua", 0))
        usuario.agua = agua
        db.session.commit()
        return redirect(f"/p2/{usuario.id}")
    return render_template("pregunta1.html", usuario=usuario) # usuario (var del html) = usuario (var de Python (obtenida del request.form)), pasa como param

@app.route("/p2/<int:id_usuario>", methods=["GET", "POST"])
def p2(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        luz = float(request.form.get("luz", 0))
        usuario.luz = luz
        db.session.commit()
        return redirect(f"/p3{usuario.id}")
    return render_template("pregunta2.html", usuario=usuario)

@app.route("/p3/<int:id_usuario>", methods=["GET", "POST"])
def p3(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        gasolina = float(request.form.get("gasolina", 0))
        usuario.gasolina = gasolina
        db.session.commit()
        return redirect(f"/p4/{usuario.id}")
    return render_template("pregunta3.html", usuario=usuario)




app.run(debug=True)