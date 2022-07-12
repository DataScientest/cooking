from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cooking.routers.auth import login_required
from cooking.db import get_db

bp = Blueprint("command", __name__, url_prefix="/command")


@bp.route("/")
def index():
    """Show all commands, most recent first."""
    db = get_db()
    commands = db.execute(
        "SELECT c.id, restaurant, menu, command_day, command_hour, group_concat(p.name) as participants_names "
        "FROM command c LEFT JOIN participant p ON p.command_id= c.id "
        "GROUP BY c.id "
        "ORDER BY command_day DESC "
    ).fetchall()
    return render_template("command/index.html", commands=commands)


def get_command(id):
    """Get a command

    Checks that the id exists

    :param id: id of command to get
    :return: the command with author information
    :raise 404: if a command with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    command = (
        get_db().execute(
            "SELECT id, restaurant, menu, command_day, command_hour"
            " FROM command"
            " WHERE id = ?",
            (id,),
        ).fetchone()
    )

    if command is None:
        abort(404, "command id {0} doesn't exist.".format(id))

    return command


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new command."""
    if request.method == "POST":
        restaurant = request.form["restaurant"]
        menu = request.form["menu"]
        command_day = request.form["command_day"]
        command_hour = request.form["command_hour"]
        error = None

        if not restaurant or not menu or not command_day or not command_hour:
            error = "One field is missing is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO command (restaurant, menu, command_day,command_hour ) VALUES (?, ?, ?, ?)",
                (restaurant, menu, command_day, command_hour),
            )
            db.commit()
            return redirect(url_for("command.index"))

    return render_template("command/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a command"""
    command = get_command(id)

    if request.method == "POST":
        restaurant = request.form["restaurant"]
        menu = request.form["menu"]
        command_day = request.form["command_day"]
        command_hour = request.form["command_hour"]
        error = None

        if not restaurant:
            error = "Restaurant is required."
        if not menu:
            error = "Menu is required."
        if not command_day:
            error = "Command Day is required."
        if not command_hour:
            error = "Command Hour is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE command SET restaurant = ?, menu = ?, command_hour= ?,command_day= ? WHERE id = ?", (restaurant, menu , command_hour ,command_day, id)
            )
            db.commit()
            return redirect(url_for("command.index"))

    return render_template("command/update.html", command=command)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a command.

    Ensures that the post exists.
    """
    get_command(id)
    db = get_db()
    db.execute("DELETE FROM command WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("command.index"))
