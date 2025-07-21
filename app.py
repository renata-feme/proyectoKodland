from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    puntaje = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

#primera página
@app.route("/") #decorador de FLASK: lit dice qué hacer (o mostrar) cuando se está en esa url
def index():
    return render_template("index.html") #función de FLASK: busca el archivo html en la carpeta templates. Así que por el amor de Dios, pon todo en templates

@app.route("/inicio", methods=['POST']) #methods, decorador de FLASK: dice qué tipo de solicitud acepta la url
def inicio():
    nombre = request.form["nombre"] #request.form[]: guarda los datos enviados de un formulario (tipo diccionario, busca la key, debe coincidir con lo que esté en name)
    nuevo_usuario = Usuario(nombre=nombre)
    db.session.add(nuevo_usuario) 
    db.session.commit() #guarda al usuario
    return redirect(f"/p1/{nuevo_usuario.id}") #manejamos por id

@app.route("/p1/<int:id_usuario>", methods=["GET", "POST"]) #pasamos el usuario de una página a otra
def p1(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    #usuario = Usuario.query.get(id_usuario)
    #if usuario is None:
        #abort(404)
    if request.method == "POST":
        p1 = int(request.form.get("p1", 0))
        usuario.puntaje += p1
        db.session.commit()
        return redirect(f"/p2/{usuario.id}")
    return render_template("pregunta1.html", usuario=usuario) # usuario (var del html) = usuario (var de Python (obtenida del request.form)), pasa como param

@app.route("/p2/<int:id_usuario>", methods=["GET", "POST"])
def p2(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        p2 = int(request.form.get("p2", 0))
        usuario.puntaje += p2
        db.session.commit()
        return redirect(f"/p3/{usuario.id}")
    return render_template("pregunta2.html", usuario=usuario)

@app.route("/p3/<int:id_usuario>", methods=["GET", "POST"])
def p3(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        p3 = int(request.form.get("p3", 0))
        usuario.puntaje += p3
        db.session.commit()
        return f"Gracias {usuario.nombre}. Tu puntaje final es: {usuario.puntaje}"
    return render_template("pregunta3.html", usuario=usuario)




app.run(debug=True)