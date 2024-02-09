from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta para recibir datos y guardarlos en un archivo de texto
@app.route('/guardar', methods=['POST'])
def guardar_datos():
    try:
        # Obtener los datos del cuerpo de la solicitud POST
        datos = request.json

        # Guardar los datos en un archivo de texto
        with open('datos.txt', 'a') as archivo:
            archivo.write(str(datos) + '\\n')

        return jsonify({'mensaje': 'Datos guardados correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
