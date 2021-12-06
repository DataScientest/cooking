from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cooking.routers.auth import login_required
from cooking.db import get_db

bp = Blueprint("participant", __name__, url_prefix="/participant")

@bp.route("/")
def index():
    """Show all the commands for the participant"""
    db = get_db()
    participants = db.execute(
        "SELECT p.id, name, mail, command_details,command_id,restaurant,command_day,command_hour "
        " FROM participant p JOIN command c ON p.command_id = c.id "
        " ORDER BY command_day DESC "
    ).fetchall()
    return render_template("participant/index.html", participants=participants)

@bp.route("/commands")
def index_2():
    """Show all the commands for the participant, most recent first."""
    db = get_db()
    commands = db.execute(
        "SELECT id, restaurant, menu, Command_day, command_hour"
        " FROM command"
        " ORDER BY Command_day DESC"
    ).fetchall()
    return render_template("participant/command_index.html", commands=commands)

@bp.route("/order/command/<int:command_id>", methods=("GET", "POST"))
@login_required
def order(command_id):
    """Let the participant order a command."""
    if request.method == "POST":
        mail = request.form["mail"]
        name = request.form["name"]
        command_details = request.form["command_details"]
        error = None

        if not mail or not name or not command_details:
            error = "One field is missing is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO participant (mail, name, command_details, command_id) VALUES (?, ?, ?,?)",
                (mail, name, command_details,command_id),
            )
            db.commit()
            return redirect(url_for("participant.index_2"))

    return render_template("participant/order.html")



def get_participant(id, ):
    """Get a participant and its author by id.

    Checks that the id exists.

    :param id: id of participant to get
    :return: the participant
    :raise 404: if a participant with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    participant = (
        get_db().execute(
            "SELECT p.id, name, mail, command_details, command_id,restaurant"
            " FROM participant p JOIN command c ON p.command_id = c.id "
            " WHERE p.id = ?",
            (id,),
        ).fetchone()
    )

    if participant is None:
        abort(404, "participant id {0} doesn't exist.".format(id))

    return participant


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new participant."""
    db = get_db()
    commands = db.execute(
        "SELECT id, restaurant "
        " FROM command"
    ).fetchall()
    if request.method == "POST":
        mail = request.form["mail"]
        name = request.form["name"]
        command_details = request.form["command_details"]
        command_id = request.form["command_id"]
        error = None

        if not mail or not name or not command_details:
            error = "One field is missing is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO participant (mail, name, command_details, command_id) VALUES (?, ?, ?,?)",
                (mail, name, command_details,command_id),
            )
            db.commit()
            return redirect(url_for("participant.index"))

    return render_template("participant/create.html",commands=commands)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a participant"""
    participant = get_participant(id)
    db = get_db()
    commands = db.execute(
        "SELECT id, restaurant "
        " FROM command"
    ).fetchall()
    if request.method == "POST":
        name = request.form["name"]
        mail = request.form["mail"]
        error = None

        if not name:
            error = "name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE participant SET name = ?, mail = ? WHERE id = ?", (name, mail, id)
            )
            db.commit()
            return redirect(url_for("participant.index"))

    return render_template("participant/update.html", participant=participant,commands=commands)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a participant.

    Ensures that the post exists.
    """
    get_participant(id)
    db = get_db()
    db.execute("DELETE FROM participant WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("participant.index"))
