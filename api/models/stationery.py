from api.database import db


class Stationery(db.Model):

    __tablename__ = "stationery"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=True)

    def format_long(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

        return self

    def update(self):
        db.session.commit()

        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class StationeryRequisition(db.Model):

    __tablename__ = "stationery_requisitions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    authorized_by = db.Column(db.ForeignKey("users.id"), nullable=False)
    approved_by = db.Column(db.ForeignKey("users.id"), nullable=False)
    issued_by = db.Column(db.ForeignKey("users.id"), nullable=False)


class StationeryRequisitionDetails(db.Model):

    __tablename__ = "stationery_requisition_details"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("stationery_requisitions.id"))
    item = db.Column(db.Integer, db.ForeignKey("stationery.id"))
    quantity = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String, nullable=True)
