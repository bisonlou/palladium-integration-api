from api.database import db


class Project(db.Model):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    client_name = db.Column(db.String, nullable=False)
    contact_person_name = db.Column(db.String, nullable=False)
    contact_person_title = db.Column(db.String, nullable=False)
    contact_person_tel = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    contract_value = db.Column(db.Float, nullable=False)
    staff_months = db.Column(db.Float, nullable=True)
    consultant_months = db.Column(db.Float, nullable=True)
    senior_proffesional = db.Column(db.String, nullable=True)
    project_description = db.Column(db.String, nullable=True)
    service_description = db.Column(db.String, nullable=True)

    associate_consultants = db.relationship(
        "AssociateConsultant",
        backref="project",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def format_long(self):
        return {
            "id": self.id,
            "project_name": self.project_name,
            "country": self.country,
            "client_name": self.client_name,
            "contact_person_name": self.contact_person_name,
            "contact_person_title": self.contact_person_title,
            "contact_person_tel": self.contact_person_tel,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "contract_value": self.contract_value,
            "staff_months": self.staff_months,
            "consultant_months": self.consultant_months,
            "senior_proffesional": self.senior_proffesional,
            "project_description": self.project_description,
            "service_description": self.service_description,
            "associate_consultants": [consultant.format_long() for consultant in self.associate_consultants]
        }

    def add(self):
        db.session.add(self)
        return self

    def delete(self):
        db.session.delete(self)

    def save(self):
        db.session.commit()


class AssociateConsultant(db.Model):

    __tablename__ = "associate_consultants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    def add(self):
        db.session.add(self)
        return self

    def delete(self):
        db.session.delete(self)

    def save(self):
        db.session.commit()

    def format_long(self):
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
        }
