from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista temporal para almacenar los datos
datos = []

# Ruta para obtener todos los datos almacenados
@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    return jsonify(datos)

# Ruta para obtener un dato específico por su ID
@app.route('/api/datos/<int:id>', methods=['GET'])
def obtener_dato(id):
    for dato in datos:
        if dato['id'] == id:
            return jsonify(dato)
    return jsonify({'mensaje': 'Dato no encontrado'}), 404

# Ruta para crear un nuevo dato
@app.route('/api/datos', methods=['POST'])
def crear_dato():
    contenido = request.json
    nuevo_dato = {
        'id': len(datos) + 1,
        'contenido': contenido['contenido']
    }
    datos.append(nuevo_dato)
    guardar_datos_en_archivo()
    return jsonify(nuevo_dato), 201

# Ruta para actualizar un dato existente
@app.route('/api/datos/<int:id>', methods=['PUT'])
def actualizar_dato(id):
    contenido = request.json
    for dato in datos:
        if dato['id'] == id:
            dato['contenido'] = contenido['contenido']
            guardar_datos_en_archivo()
            return jsonify(dato)
    return jsonify({'mensaje': 'Dato no encontrado'}), 404

# Ruta para eliminar un dato existente
@app.route('/api/datos/<int:id>', methods=['DELETE'])
def eliminar_dato(id):
    for dato in datos:
        if dato['id'] == id:
            datos.remove(dato)
            guardar_datos_en_archivo()
            return jsonify({'mensaje': 'Dato eliminado correctamente'})
    return jsonify({'mensaje': 'Dato no encontrado'}), 404

# Función para guardar los datos en un archivo de texto
def guardar_datos_en_archivo():
    with open('datos.txt', 'w') as archivo:
        for dato in datos:
            archivo.write(f"{dato['id']}: {dato['contenido']}\n")

if __name__ == '__main__':
    # Cargar datos desde el archivo al iniciar la aplicación
    try:
        with open('datos.txt', 'r') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                id, contenido = linea.strip().split(': ')
                datos.append({'id': int(id), 'contenido': contenido})
    except FileNotFoundError:
        pass

    app.run(debug=True)
