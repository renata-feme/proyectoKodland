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
    bano = db.Column(db.Float, default=0) 
    aguaEmbot = db.Column(db.Float, default=0)
    reciclaje = db.Column(db.Integer, default=0)
    ropa = db.Column(db.Integer, default=0)
    consumoLocal = db.Column(db.Integer, default=0)

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

# id_usuario : número recibido desde la URL

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

@app.route("/p4/<int: id_usuario>", methods=["GET", "POST"])
def p4(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        bano = float(request.form.get("bano", 0))
        usuario.bano = bano
        db.session.commit()
        return redirect(f"/p5/{usuario.id}")
    return render_template("pregunta4.html", usuario=usuario)

@app.route("/p5/<int:id_usuario>", methods=["GET", "POST"])
def p5(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.methos == ["POST"]:
        aguaEmbot = float(request.form.get("aguaEmbot", 0))
        usuario.aguaEmbot = aguaEmbot
        db.session.commit()
        return redirect(f"/p6/{usuario.id}")
    return render_template("pregunta5.html", usuario=usuario)

@app.route("/p6/<int:id_usuario>", methods=["GET", "POST"])
def p6(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        reciclaje = int(request.form.get("reciclaje", 0))
        usuario.reciclaje = reciclaje
        db.session.commit()
        return redirect(f"/p7/{usuario.id}")
    return render_template("pregunta6.html", usuario=usuario)

@app.route("/p7/<int:id_usuario>", methods=["GET", "POST"])
def p7(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        ropa = int(request.form.get("ropa", 0))
        usuario.ropa = ropa
        db.session.commit()
        return redirect(f"/p8/{usuario.id}")
    return render_template("pregunta7.html", usuario=usuario)

@app.route("/p8/<int:id_usuario>", methods=["GET", "POST"])
def p8(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        consumoLocal = int(request.form.get("consumoLocal", 0))
        usuario.consumoLocal = consumoLocal
        db.session.commit()
        return redirect(f"/resultado/{usuario.id}")
    return render_template("pregunta8.html", usuario=usuario)

@app.route("/resultado/<int:id_usuario>")
def resultado(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)

    #directos
    aguaTotal = usuario.agua * 0.0013
    luzTotal = usuario.luz * 0.5
    gasolinaTotal = usuario.gasolina * 2.31
    duchaTotal = usuario.bano * 9 * 30 * 0.0013
    botellasTotal = usuario.aguaEmbot * 4 * 0.3
    ropaTotal = usuario.ropa * 7.5

     # Factores recicalje
    if usuario.reciclaje == 0:
        factor_reciclaje = 1.0
    elif usuario.reciclaje == 1:
        factor_reciclaje = 0.9
    elif usuario.reciclaje == 2:
        factor_reciclaje = 0.7
    else:
        factor_reciclaje = 0.5

    # Factores consumo local
    if usuario.consumoLocal == 0:
        factor_consumo = 1.0
    elif usuario.consumoLocal == 1:
        factor_consumo = 0.85
    else:
        factor_consumo = 0.7

    # Cálculo total con factores aplicados
    total = ( aguaTotal + luzTotal + gasolinaTotal + duchaTotal +
        ropaTotal + botellasTotal) * factor_reciclaje * factor_consumo

    usuario.puntaje = round(total, 2)
    db.session.commit()

    return render_template("resultado.html", usuario=usuario)

app.run(debug=True)