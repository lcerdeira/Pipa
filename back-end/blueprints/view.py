from doctest import debug
import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
bp = Blueprint("view", __name__, template_folder='templates', static_folder='static')

@bp.route("/")
def index():
    current_app.pipa.FolderVerificationRun()
    return render_template("index.html")

@bp.route("/save_file", methods=["POST"])
def save_file():
    form = request.form.to_dict()
    type_end = ""
    if "type_end" in form:
        type_end = form["type_end"]
        del form["type_end"]
    for f in form:
        name_files = "file_"+f
        files = request.files.getlist(name_files)
        if f == "illumina":
            if type_end == "paread":
                if len(files) % 2 != 0:
                    return "Número de pares incorretos!"
        for file in files:
            path = "./data/input/" + f + "/" + secure_filename(file.filename)
            file.save(path)
    return redirect(url_for("view.trimage"))

@bp.route("/trimage")
def trimage():
    current_app.pipa.TrimageRun()
    return redirect(url_for("view.montage"))

@bp.route("/montage")
def montage():
    current_app.pipa.AssemblyRun()
    return redirect(url_for("view.predict"))

@bp.route("/predict")
def predict():
    current_app.pipa.PredictRun()
    return redirect(url_for("view.report"))

@bp.route("/report")
def report():
    report = current_app.pipa.ReportRun()
    return render_template("report.html", report=report)

def init_app(app):
    app.register_blueprint(bp)