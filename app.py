import os, uuid, mimetypes
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from storage import Storage

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-development-key")
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024
storage = Storage()
ALLOWED = {"pdf","png","jpg","jpeg","doc","docx","xls","xlsx","ppt","pptx","txt","csv","zip"}

def allowed(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED

@app.route("/")
def index():
    files = storage.list_files()
    return render_template("index.html", files=files, storage_mode=storage.mode, allowed=", ".join(sorted(ALLOWED)))

@app.route("/upload", methods=["POST"])
def upload():
    f=request.files.get("file")
    if not f or not f.filename:
        flash("Choose a file to upload.", "error"); return redirect(url_for("index"))
    original=secure_filename(f.filename)
    if not allowed(original):
        flash("File type not allowed.", "error"); return redirect(url_for("index"))
    key=f"{uuid.uuid4().hex}_{original}"
    ok,msg=storage.upload(f,key,original)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))

@app.route("/download/<path:key>")
def download(key):
    result=storage.download(key)
    if storage.mode=="local":
        if result: return send_from_directory(storage.local_dir, result, as_attachment=True)
    elif result:
        return redirect(result)
    flash("File could not be downloaded.", "error")
    return redirect(url_for("index"))

@app.route("/delete/<path:key>", methods=["POST"])
def delete(key):
    ok,msg=storage.delete(key)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status":"ok","storage":storage.mode},200

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT",5000)),debug=False)
