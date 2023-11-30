from db import db, ma
from models.DuenoMascotaModel import DuenoMascota

class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)


class MascotaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mascota
        fields = ["id", "nombre", "especie", "raza","edad"]


def crearMascota(nombre,especie,raza,edad):
    mascota = Mascota(nombre=nombre,especie=especie,raza=raza,edad=edad)
    db.session.add(mascota)
    db.session.commit()
    mascotaSchema = MascotaSchema()
    return mascotaSchema.dump(mascota)


def modificarMascota(id,nombre,especie,raza,edad):
    mascota = Mascota.query.filter_by(id=id).first()
    
    if mascota is not None:
        mascota.nombre = nombre
        mascota.especie = especie
        mascota.raza = raza
        mascota.edad = edad
        db.session.commit()
        mascotaSchema = MascotaSchema()
        return mascotaSchema.dump(mascota)
    return None


def eliminarMascota(id):
    mascota = Mascota.query.filter_by(id=id).delete()
    if mascota == 1:
        db.session.commit()
        return True
    return False


def consultarMascotas_x_Dueno(id_dueno):
    mascota = db.session.query(Mascota).join(DuenoMascota).filter(Mascota.id == DuenoMascota.mascota_id, DuenoMascota.dueno_id == id_dueno).all()
    mascotaSchema = MascotaSchema()
    return [mascotaSchema.dump(mascota) for mascota in mascota]


def consultarMascota_x_Dueno(id_dueno, id_mascota):
    mascota = db.session.query(Mascota).join(DuenoMascota).filter(Mascota.id == DuenoMascota.mascota_id, 
                                                                  DuenoMascota.dueno_id == id_dueno, 
                                                                  Mascota.id==id_mascota).first()
    mascotaSchema = MascotaSchema()
    return mascotaSchema.dump(mascota)
