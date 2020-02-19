from api.database import db


class Stationery(db.Model):

    __tablename__ = "stationery"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=True)
    requisitions = db.relationship(
        "StationeryRequisitionDetails",
        backref="stationery",
        cascade="all, delete-orphan",
    )

    def format_long(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
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
    requisition_date = db.Column(db.DateTime, nullable=False)
    authorized_by = db.Column(db.Integer, nullable=True)
    approved_by = db.Column(db.Integer, nullable=True)
    issued_by = db.Column(db.Integer, nullable=True)
    details = db.relationship(
        "StationeryRequisitionDetails",
        backref="header",
        lazy=True,
        cascade="all, delete-orphan",
    )

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

    def get_user_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def format_long(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.get_user_full_name(),
            "requisition_date": self.requisition_date,
            "authorized_by": self.authorized_by,
            "approved_by": self.approved_by,
            "issued_by": self.issued_by,
            "details": [detail.format_long() for detail in self.details],
        }


class StationeryRequisitionDetails(db.Model):

    __tablename__ = "stationery_requisition_details"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    requisition_id = db.Column(
        db.Integer, db.ForeignKey("stationery_requisitions.id")
    )
    item_id = db.Column(db.Integer, db.ForeignKey("stationery.id"))
    quantity = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String, nullable=True)
    item = db.relationship("Stationery", backref="stationery_requisition")

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format_long(self):
        return {
            "id": self.id,
            "requisition_id": self.requisition_id,
            "quantity": self.quantity,
            "purpose": self.purpose,
            "item_id": self.item_id,
            "item": self.item.format_long(),
        }
