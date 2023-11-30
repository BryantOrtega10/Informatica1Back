from db import db, ma
from werkzeug.security import generate_password_hash, check_password_hash


class Dueno(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cedula = db.Column(db.String(12), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200))


class DuenoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Dueno
        fields = ["id", "cedula", "nombre", "direccion","correo"]




def crearDueno(cedula, nombre, direccion, correo, password_b):
    dueno = Dueno(cedula=cedula, nombre=nombre, direccion=direccion, correo=correo, password = generate_password_hash(password_b))
    db.session.add(dueno)
    db.session.commit()
    duenoSchema = DuenoSchema()
    return duenoSchema.dump(dueno)


def modificarDueno(id,cedula, nombre, direccion, correo, password):
    
    dueno = Dueno.query.filter_by(id=id).first()
    if dueno != None:
        
        dueno.cedula = cedula
        dueno.nombre = nombre
        dueno.direccion = direccion
        dueno.correo = correo
        if password is not None:
            dueno.password = generate_password_hash(password)
        db.session.commit()
        duenoSchema = DuenoSchema()
        return duenoSchema.dump(dueno)
    
    return None



def existeCorreo(id,correo):
    dueno = Dueno.query.filter(id!=id, correo == correo).first()
    if dueno != None:
        return True
    return False


def loginDueno(correo, password):
    dueno = Dueno.query.filter_by(correo=correo).first()
    if dueno != None:
        if check_password_hash(dueno.password, password):
            dueno_schema = DuenoSchema()
            return dueno_schema.dump(dueno)
    return None

def consultarDueno(id):
    dueno = Dueno.query.filter_by(id=id).first()
    dueno_schema = DuenoSchema()
    return dueno_schema.dump(dueno)
