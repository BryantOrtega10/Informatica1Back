from http import HTTPStatus
from flask import Blueprint, jsonify, request, current_app
from models.MascotaModel import consultarMascotas_x_Dueno,crearMascota ,modificarMascota ,eliminarMascota, consultarMascota_x_Dueno
from models.DuenoMascotaModel import existeOtroDueno, crearDuenoMascota, existeDuenoMascota, eliminarDuenoMascota
from funciones.token import token_requerido

mascotas_bp = Blueprint("mascotas", __name__, url_prefix="/mascotas")


@mascotas_bp.route("/", methods=["GET"])
@token_requerido
def obtenerMascotas():
    dueno_id = current_app.config['DUENO_ID']
    mascotas = consultarMascotas_x_Dueno(dueno_id)
    return jsonify({"success": True, "mascotas": mascotas}) , HTTPStatus.OK

@mascotas_bp.route("/<int:mascota_id>", methods=["GET"])
@token_requerido
def obtenerMascotasEspecifica(mascota_id):
    dueno_id = current_app.config['DUENO_ID']
    mascota = consultarMascota_x_Dueno(dueno_id, mascota_id)
    return jsonify({"success": True, "mascota": mascota}) , HTTPStatus.OK




@mascotas_bp.route("/", methods=["POST"])
@token_requerido
def agregarMascotas():
    json_recibido = request.get_json()
    dueno_id = current_app.config['DUENO_ID']
    nombre = json_recibido["nombre"]
    especie = json_recibido["especie"]
    raza = json_recibido["raza"]
    edad = json_recibido["edad"]

    mascota = crearMascota(nombre,especie,raza,edad)

    crearDuenoMascota(mascota["id"],dueno_id)

    return jsonify({"success": True, "message": "Se ha creado la mascota correctamente"}) , HTTPStatus.OK


@mascotas_bp.route("/asociar/<int:mascota_id>", methods=["POST"])
@token_requerido
def asociarMascotas(mascota_id):
    dueno_id = current_app.config['DUENO_ID']
    if existeDuenoMascota(mascota_id,dueno_id):
        return jsonify({"success": False, "error": "Error ya estas asociado a esta mascota"}) , HTTPStatus.BAD_REQUEST

    crearDuenoMascota(mascota_id,dueno_id)

    return jsonify({"success": True, "message": "Se ha asociado la mascota correctamente"}) , HTTPStatus.OK



@mascotas_bp.route("/<int:mascota_id>", methods=["PUT"])
@token_requerido
def modificarMascotas(mascota_id):
    json_recibido = request.get_json()
    
    nombre = json_recibido["nombre"]
    especie = json_recibido["especie"]
    raza = json_recibido["raza"]
    edad = json_recibido["edad"]
    dueno_id = current_app.config['DUENO_ID']
    if existeDuenoMascota(mascota_id,dueno_id) is False:
        return jsonify({"success": False, "error": "Error no estas asociado a esta mascota"}) , HTTPStatus.BAD_REQUEST
    

    mascota = modificarMascota(mascota_id,nombre,especie,raza,edad)
    if mascota is None:
        return jsonify({"success": False, "error": "Id de mascota no encontrado"}) , HTTPStatus.BAD_REQUEST
    
    return jsonify({"success": True, "message": "Mascota modificada correctamente!", "mascota": mascota}) , HTTPStatus.OK


@mascotas_bp.route("/<int:mascota_id>", methods=["DELETE"])
@token_requerido
def eliminarMascotas(mascota_id):

    dueno_id = current_app.config['DUENO_ID']
    if existeDuenoMascota(mascota_id,dueno_id) is False:
        return jsonify({"success": False, "error": "Error no estas asociado a esta mascota"}) , HTTPStatus.BAD_REQUEST
    
    eliminarDuenoMascota(mascota_id,dueno_id)
    
    if existeOtroDueno(mascota_id,dueno_id) is False:
        eliminarMascota(mascota_id)
        
    
    return jsonify({"success": True, "message": "Mascota eliminada de base de datos correctamente!"}) , HTTPStatus.OK