from flask import Flask, request, render_template
import json
import boto3
import translator
from language import language
from dotenv import load_dotenv
import os

load_dotenv()
aws_id = str(os.getenv("id"))
aws_key = str(os.getenv("key"))

textractclient = boto3.client("textract", aws_access_key_id=aws_id,aws_secret_access_key=aws_key, region_name="us-west-1")


app = Flask(__name__)



@app.route("/", methods=["GET"])
def main():
    return render_template("index.html", jsonData=json.dumps({}))


@app.route("/extract", methods=["POST"])
def extractImage():

    file = request.files.get("filename")
    language_box = request.form.get("searchbox")
    language_box = language_box.lower()
    if not request.files['filename'].filename or not language_box or language_box not in language or not language_box.isalpha:
        return render_template("index.html", jsonData=json.dumps({"text":""}))
    language_box = language[language_box]
    
    binaryFile = file.read()
    response = textractclient.detect_document_text(
        Document={
            'Bytes': binaryFile
        }
    )

    extractedText = ""

    for block in response['Blocks']:
        if block["BlockType"] == "LINE":
            extractedText = extractedText+block["Text"]+" "

    extractedText = translator.translate_language(extractedText,language_box)
    responseJson = {

        "text": extractedText
    }
    

    return render_template("index.html", jsonData=json.dumps(responseJson))


app.run("0.0.0.0", port=5000, debug=True)