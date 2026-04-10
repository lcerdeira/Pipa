import os

from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

bp = Blueprint("view", __name__, template_folder='templates', static_folder='static')


@bp.route("/")
def index():
    current_app.pipa.ensure_directories()
    return render_template("index.html")


@bp.route("/save_file", methods=["POST"])
def save_file():
    form = request.form.to_dict()
    type_end = form.pop("type_end", "")

    for f in form:
        name_files = "file_" + f
        files = request.files.getlist(name_files)
        if f == "illumina" and type_end == "paread":
            if len(files) % 2 != 0:
                return "Incorrect number of paired files!", 400
        for file in files:
            data_dir = current_app.config["PIPA_DATA_DIR"]
            path = os.path.join(data_dir, "input", f, secure_filename(file.filename))
            file.save(path)

    return redirect(url_for("view.trimage"))


@bp.route("/trimage")
def trimage():
    current_app.pipa._run_trimming(callback=None)
    return redirect(url_for("view.montage"))


@bp.route("/montage")
def montage():
    from extensions.services import PipelineConfig
    config = PipelineConfig()
    current_app.pipa._run_assembly(config, callback=None)
    return redirect(url_for("view.predict"))


@bp.route("/predict")
def predict():
    from extensions.services import PipelineConfig
    config = PipelineConfig()
    current_app.pipa._run_prediction(config, callback=None)
    return redirect(url_for("view.report"))


@bp.route("/report")
def report():
    result = current_app.pipa._run_report(callback=None)
    return render_template("report.html", report=result)
