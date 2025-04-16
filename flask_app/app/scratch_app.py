# flask_app/app/scratch_app.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_app.models import db, Comment

scratch_bp = Blueprint('scratch', __name__)

@scratch_bp.route("/scratch", methods=["GET", "POST"])
def scratch():
    if request.method == "POST":
        if 'user_id' in session:
            content = request.form["comment"]
            user_id = session["user_id"]
            comment = Comment(content=content, user_id=user_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("You must be logged in to post a comment.", "warning")
            return redirect(url_for("auth.login"))  # Redirect to login
        return redirect(url_for("scratch.scratch"))

    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    return render_template("scratch/scratch.html", comments=comments)

@scratch_bp.route("/edit-comment/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if session.get('user_id') != comment.user_id:
        flash("You are not authorized to edit this comment.", "danger")
        return redirect(url_for('scratch.scratch'))

    if request.method == "POST":
        new_content = request.form["comment"]
        comment.content = new_content
        db.session.commit()
        flash("Comment updated successfully!", "success")
        return redirect(url_for('scratch.scratch'))

    return render_template("scratch/edit_comment.html", comment=comment)


@scratch_bp.route("/delete-comment/<int:comment_id>")
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if session.get('user_id') != comment.user_id:
        flash("You are not authorized to delete this comment.", "danger")
        return redirect(url_for('scratch.scratch'))

    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully!", "info")
    return redirect(url_for('scratch.scratch'))