import firebase_admin
from flask import Flask, request, jsonify
import os, json, io, traceback

from firebase_admin import credentials, firestore, storage, db as rtdb, messaging

app = Flask(__name__)
RTD_URL1 = "https://scales-ofm-default-rtdb.asia-southeast1.firebasedatabase.app/"
BUCKET_NAME = "scales-ofm.firebasestorage.app"

service_account_json = os.environ.get("FIREBASE_SERVICE_KEY")
if not service_account_json:
    raise RuntimeError("Missing FIREBASE_SERVICE_KEY")

cred = credentials.Certificate(json.loads(service_account_json))
firebase_admin.initialize_app(
    cred,
    {
        "storageBucket": BUCKET_NAME,
        "databaseURL": RTD_URL1
    }
)

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
