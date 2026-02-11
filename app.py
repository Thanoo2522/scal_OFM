import firebase_admin
from flask import Flask
import os, json, io, traceback
from firebase_admin import credentials, firestore,request, jsonify
from firebase_admin import credentials, storage, db as rtdb, firestore, messaging

app = Flask(__name__)

service_account_json = os.environ.get("FIREBASE_SERVICE_KEY")
if not service_account_json:
    raise RuntimeError("Missing FIREBASE_SERVICE_KEY")

cred = credentials.Certificate(json.loads(service_account_json))
firebase_admin.initialize_app(cred)

db = firestore.client()
rtdb_ref = rtdb.reference("/")
bucket = storage.bucket()


@app.route("/get_api_config", methods=["GET"])
def get_api_config():
    ofm = request.args.get("ofm")

    doc = db.collection("ofm_servers").document(ofm).get()

    if doc.exists:
        data = doc.to_dict()
        return jsonify({
            "api_base": data["api_base"]
        })

    return jsonify({
        "api_base": "https://ofmserver-default.onrender.com"
    })
