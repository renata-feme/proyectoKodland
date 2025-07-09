from flask import Flask, render_template, request, redirect

app =  Flask(__name__)

nombre = ""
puntaje = 0

#primera página
@app.route("/") #decorador de FLASK: lit dice qué hacer (o mostrar) cuando se está en esa url
def index():
    return render_template("index.html") #función de FLASK: busca el archivo html en la carpeta templates. Así que por el amor de Dios, pon todo en templates

@app.route("/inicio", methods=['POST']) #methods, decorador de FLASK: dice qué tipo de solicitud acepta la url
def inicio():
    global nombre, puntaje
    nombre = request.form['nombre']  #request.form[]: guarda los datos enviados de un formulario (tipo diccionario, busca la key, debe coincidir con lo que esté en name)
    puntaje = 0
    return redirect("/p1")

@app.route("/p1", methods=["POST", "GET"]) 
def p1():
    global puntaje
    if request.method == "POST":
        p1 = int(request.form[p1])
        puntaje += p1
        return redirect("/p2")
    return render_template("pregunta1.html", nombre=nombre) # nombre (var del html) = name (var de Python (obtenida del request.form)), pasa como param

#DUDAAAA: no sé por qué no sale, help
#@app.route("/p2", methods=["POST", "GET"]) #pa' enviar el formulario y mostrarlo
#def p2():
  #  if request.method == "POST":
   #     p2 = request.form[p2]
    #    return f"Respondiste: {p2}" #OJO, nada más era para que funcionara, según yo lol
   # else:
    #    return render_template("pregunta2.html")

app.run(debug=True)