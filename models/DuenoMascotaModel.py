from db import db, ma

class DuenoMascota(db.Model):
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False, primary_key=True)
    dueno_id = db.Column(db.Integer, db.ForeignKey('dueno.id'), nullable=False, primary_key=True)

class DuenoMascotaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DuenoMascota
        fields = ["mascota_id", "dueno_id"]


def crearDuenoMascota(mascota_id,dueno_id):
    duenoMascota = DuenoMascota(mascota_id=mascota_id,dueno_id=dueno_id)
    db.session.add(duenoMascota)
    db.session.commit()
    duenoMascotaSchema = DuenoMascotaSchema()
    return duenoMascotaSchema.dump(duenoMascota)

def existeDuenoMascota(mascota_id,dueno_id):
    existe = DuenoMascota.query.filter_by(mascota_id=mascota_id, dueno_id=dueno_id).first()
    if existe is not None:
        return True
    return False


def eliminarDuenoMascota(mascota_id,dueno_id):
    elimino = DuenoMascota.query.filter_by(mascota_id=mascota_id, dueno_id=dueno_id).delete()
    if elimino == 1:
        db.session.commit()
        return True
    return False


def existeOtroDueno(mascota_id,dueno_id):
    otroDueno = DuenoMascota.query.filter(mascota_id==mascota_id, dueno_id!=dueno_id).first()
    if otroDueno != None:
        return True
    return False

