from datetime import date

from flask import Blueprint, current_app, jsonify, request

from . import db
from .models import STATUSES, Application

bp = Blueprint("api", __name__)
FIELDS = ("company", "role", "status", "url", "notes", "applied_on")


def validate(data, partial=False):
    """Return a dict of field errors (empty if the payload is valid)."""
    errors = {}
    if not partial:
        for field in ("company", "role"):
            if not str(data.get(field, "")).strip():
                errors[field] = "is required"
    if "status" in data and data["status"] not in STATUSES:
        errors["status"] = f"must be one of {list(STATUSES)}"
    if "applied_on" in data:
        try:
            date.fromisoformat(data["applied_on"])
        except (ValueError, TypeError):
            errors["applied_on"] = "must be YYYY-MM-DD"
    return errors


def apply_fields(item, data):
    for field in FIELDS:
        if field in data:
            value = data[field]
            if field == "applied_on":
                value = date.fromisoformat(value)
            setattr(item, field, value)


@bp.get("/")
def index():
    return current_app.send_static_file("index.html")


@bp.get("/api/applications")
def list_applications():
    query = Application.query
    status = request.args.get("status")
    if status:
        query = query.filter_by(status=status)
    items = query.order_by(Application.applied_on.desc(), Application.id.desc()).all()
    return jsonify([a.to_dict() for a in items])


@bp.post("/api/applications")
def create_application():
    data = request.get_json(silent=True) or {}
    errors = validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    item = Application()
    apply_fields(item, data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@bp.get("/api/applications/<int:app_id>")
def get_application(app_id):
    return jsonify(db.get_or_404(Application, app_id).to_dict())


@bp.put("/api/applications/<int:app_id>")
def update_application(app_id):
    item = db.get_or_404(Application, app_id)
    data = request.get_json(silent=True) or {}
    errors = validate(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    apply_fields(item, data)
    db.session.commit()
    return jsonify(item.to_dict())


@bp.delete("/api/applications/<int:app_id>")
def delete_application(app_id):
    item = db.get_or_404(Application, app_id)
    db.session.delete(item)
    db.session.commit()
    return "", 204


@bp.get("/api/stats")
def stats():
    counts = {s: 0 for s in STATUSES}
    rows = (
        db.session.query(Application.status, db.func.count(Application.id))
        .group_by(Application.status)
        .all()
    )
    for status, count in rows:
        counts[status] = count
    return jsonify({"total": sum(counts.values()), "by_status": counts})
