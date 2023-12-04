from http import HTTPStatus
from flask import Blueprint, jsonify, request, current_app
from models.DuenoModel import crearDueno, existeCorreo, loginDueno, modificarDueno, consultarDueno
from funciones.token import token_requerido
import jwt

duenos_bp = Blueprint("dueno", __name__, url_prefix="/dueno")
@duenos_bp.route("/login", methods=["POST"])
def validarLogin():
    json_recibido = request.get_json()
    req_correo = json_recibido["correo"]
    req_password = json_recibido["password"]

    dueno_loggeado = loginDueno(req_correo, req_password)
    if dueno_loggeado is None:
        return jsonify({"success": False, "error": "Usuario o contraseña incorrectos"}) , HTTPStatus.BAD_REQUEST

    token = jwt.encode({'id': dueno_loggeado["id"]}, current_app.config['JWT_SECRET_KEY'])
    
    return jsonify({"success": True, "message" : "¡Bienvenido!", "token": token}) , HTTPStatus.OK

@duenos_bp.route("/", methods=["POST"])
def crearNuevoDueno():
    json_recibido = request.get_json()
    req_cedula = json_recibido["cedula"]
    req_nombre = json_recibido["nombre"]
    req_direccion = json_recibido["direccion"]
    req_correo = json_recibido["correo"]
    req_password = json_recibido["password"]
    req_rpassword = json_recibido["rpassword"]

    if req_correo == "":
        return jsonify({"success": False, "error": "Debes ingresar un correo"}) , HTTPStatus.BAD_REQUEST


    if req_password != req_rpassword:
        return jsonify({"success": False, "error": "Las contraseñas no coinciden"}) , HTTPStatus.BAD_REQUEST

    if existeCorreo(None,req_correo):
        return jsonify({"success": False, "error": "El correo ya se encuentra registrado"}) , HTTPStatus.BAD_REQUEST


    dueno = crearDueno(req_cedula,req_nombre,req_direccion,req_correo,req_password)
    if dueno is None:
        return jsonify({"success": False, "error": "Error al crear el dueño"}) , HTTPStatus.BAD_REQUEST
    
    return jsonify({"success": True, "message" : "Te has registrado con éxito!"}) , HTTPStatus.OK

@duenos_bp.route("/", methods=["GET"])
@token_requerido
def obtenerDatosDueno():
    req_id_dueno = current_app.config['DUENO_ID']
    dueno = consultarDueno(req_id_dueno)
    if dueno is None:
        return jsonify({"success": False, "error": "No existe un dueño con ese id"}) , HTTPStatus.BAD_REQUEST
    
    return jsonify({"success": True, "message" : "Dueño consultado con éxito!", "dueno" : dueno}) , HTTPStatus.OK

@duenos_bp.route("/", methods=["PUT"])
@token_requerido
def modificarDatosDueno():
    json_recibido = request.get_json()
    req_cedula = json_recibido["cedula"]
    req_nombre = json_recibido["nombre"]
    req_direccion = json_recibido["direccion"]
    req_correo = json_recibido["correo"]
    req_password = json_recibido["password"]
    req_rpassword = json_recibido["rpassword"]
    req_id_dueno = current_app.config['DUENO_ID']

    if req_password != req_rpassword:
        return jsonify({"success": False, "error": "Las contraseñas no coinciden"}) , HTTPStatus.BAD_REQUEST

    if req_password == "":
        req_password = None

    if existeCorreo(req_id_dueno,req_correo):
        return jsonify({"success": False, "error": "El correo ya se encuentra registrado"}) , HTTPStatus.BAD_REQUEST

    dueno = modificarDueno(req_id_dueno,req_cedula,req_nombre,req_direccion,req_correo,req_password)
    if dueno is None:
        return jsonify({"success": False, "error": "No existe un dueño con ese id"}) , HTTPStatus.BAD_REQUEST
    
    return jsonify({"success": True, "message" : "Dueño modificado con éxito!"}) , HTTPStatus.OK