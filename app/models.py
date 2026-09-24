from datetime import date

from . import db

STATUSES = ("applied", "interview", "offer", "rejected")


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="applied")
    url = db.Column(db.String(500))
    notes = db.Column(db.Text)
    applied_on = db.Column(db.Date, default=date.today)

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "status": self.status,
            "url": self.url,
            "notes": self.notes,
            "applied_on": self.applied_on.isoformat() if self.applied_on else None,
        }
