from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista temporal para almacenar los datos de los usuarios
usuarios = []

# Ruta para obtener todos los usuarios almacenados
@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(usuarios)

# Ruta para obtener un usuario específico por su ID
@app.route('/api/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    for usuario in usuarios:
        if usuario['id'] == id:
            return jsonify(usuario)
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# Ruta para crear un nuevo usuario
@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    contenido = request.json

    # Verificar si el ID ya existe
    for usuario in usuarios:
        if usuario['id'] == contenido['id']:
            return jsonify({'error': 'El ID ya existe'}), 400

    nuevo_usuario = {
        'id': contenido['id'],
        'FirstName': contenido['FirstName'],
        'LastName': contenido['LastName'],
        'username': contenido['username'],
        'email': contenido['email'],
        'address': contenido['address'],
        'phone': contenido['phone'],
        'website': contenido['website'],
        'company': contenido['company']
    }
    usuarios.append(nuevo_usuario)
    guardar_datos_en_archivo()
    return jsonify(nuevo_usuario), 201

# Ruta para actualizar un usuario existente
@app.route('/api/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    contenido = request.json
    for usuario in usuarios:
        if usuario['id'] == id:
            usuario['FirstName'] = contenido['FirstName']
            usuario['LastName'] = contenido['LastName']
            usuario['username'] = contenido['username']
            usuario['email'] = contenido['email']
            usuario['address'] = contenido['address']
            usuario['phone'] = contenido['phone']
            usuario['website'] = contenido['website']
            usuario['company'] = contenido['company']
            guardar_datos_en_archivo()
            return jsonify(usuario)
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# Ruta para eliminar un usuario existente
@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    for usuario in usuarios:
        if usuario['id'] == id:
            usuarios.remove(usuario)
            guardar_datos_en_archivo()
            return jsonify({'mensaje': 'Usuario eliminado correctamente'})
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# Función para guardar los datos de los usuarios en un archivo de texto
def guardar_datos_en_archivo():
    with open('usuarios.txt', 'a+') as archivo:
        for usuario in usuarios:
            archivo.write(f"{usuario['id']}: {usuario}\n")

if __name__ == '__main__':
    # Cargar datos desde el archivo al iniciar la aplicación
    try:
        with open('usuarios.txt', 'r') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                id, contenido = linea.strip().split(':', 1)
                usuarios.append({'id': int(id), **eval(contenido)})
    except FileNotFoundError:
        pass

    app.run(host='172.17.1.1', port=5000, debug=True)
