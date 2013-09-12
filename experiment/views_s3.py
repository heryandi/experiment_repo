from boto.s3.connection import S3Connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response

from .models import *

from datetime import datetime, timedelta
import base64
import hmac, hashlib
import json
import time
import urllib

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_KEY = ""
S3_BUCKET_NAME = ""
S3_BUCKET_URL = "//" + S3_BUCKET_NAME + ".s3.amazonaws.com" 

def index(request, experiment_id):
    data = {
        "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
        "S3_BUCKET_NAME": S3_BUCKET_NAME,
        "S3_BUCKET_URL": S3_BUCKET_URL,
        "S3_FOLDER": "/".join([str(request.user.id), experiment_id]),
        "experiment_id": experiment_id
    }
    return render_to_response("s3/upload.html", data)

def init_multipart(request, experiment_id):
    objectName = encodeURI(request.GET["objectName"])

    url = "//{bucketName}.s3.amazonaws.com/{objectName}?uploads".format(
        bucketName=S3_BUCKET_NAME,
        objectName=objectName
    )
    date = curdatetime()

    string = "POST\n\n\n\nx-amz-date:{date}\n/{bucketName}/{objectName}?uploads".format(
        date=date,
        bucketName=S3_BUCKET_NAME,
        objectName=objectName
    )
    signature = sign_string(string)
    authorization = "AWS " + AWS_ACCESS_KEY_ID + ":" + signature

    return HttpResponse(json.dumps({
        "url": url,
        "date": date,
        "authorization": authorization
    }), content_type="application/json")

def send_chunk(request, experiment_id):
    objectName = encodeURI(request.GET["objectName"])
    partNumber = request.GET["partNumber"]
    uploadId = request.GET["uploadId"]
    contentMD5 = request.GET["contentMD5"]

    url = "//{bucketName}.s3.amazonaws.com/{objectName}?partNumber={partNumber}&uploadId={uploadId}".format(
        bucketName=S3_BUCKET_NAME,
        objectName=objectName,
        partNumber= partNumber,
        uploadId= uploadId
    )
    date = curdatetime()

    string = "PUT\n{contentMD5}\n\n\nx-amz-date:{date}\n/{bucketName}/{objectName}?partNumber={partNumber}&uploadId={uploadId}".format(
        contentMD5=contentMD5,
        date=date,
        bucketName=S3_BUCKET_NAME,
        objectName=objectName,
        partNumber=partNumber,
        uploadId=uploadId
    )
    signature = sign_string(string)
    authorization = "AWS " + AWS_ACCESS_KEY_ID + ":" + signature

    return HttpResponse(json.dumps({
        "url": url,
        "date": date,
        "authorization": authorization
    }), content_type="application/json")

def complete_file(request, experiment_id):
    objectName = encodeURI(request.GET["objectName"])
    uploadId = request.GET["uploadId"]
    contentType = request.GET["contentType"]

    url = "//{bucketName}.s3.amazonaws.com/{objectName}?uploadId={uploadId}".format(
        bucketName=S3_BUCKET_NAME,
        objectName=objectName,
        uploadId=uploadId
    )
    date = curdatetime()

    string = "POST\n\n{contentType}\n\nx-amz-date:{date}\n/{bucketName}/{objectName}?uploadId={uploadId}".format(
        contentType=contentType,
        date=date, 
        bucketName=S3_BUCKET_NAME,
        objectName=objectName,
        uploadId=uploadId
    )
    signature = sign_string(string)
    authorization = "AWS " + AWS_ACCESS_KEY_ID + ":" + signature

    return HttpResponse(json.dumps({
        "url": url,
        "date": date,
        "authorization": authorization
    }), content_type="application/json")

def report(request, experiment_id):
    imageUrl = request.GET["imageUrl"]
    imageKey = request.GET["imageKey"]

    exp = get_object_or_404(Experiment, id=experiment_id)
    if hasattr(exp, "s3file"):
        if exp.s3file.key != imageKey:
            conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_KEY)
            b = conn.get_bucket(S3_BUCKET_NAME)
            b.get_key(exp.s3file.key).delete()
        exp.s3file.delete()
    S3File.objects.create(experiment_id = exp.id, url = imageUrl, key = imageKey)
    return HttpResponse()

# Mimic javascript encodeURI() function
def encodeURI(str):
    try:
        from urllib import quote
    except ImportError:
        from urllib.parse import quote
    return quote(str, ";,/?:@&=+$!~*'()")

def curdatetime():
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime()).strip()

def sign_string(string):
    return base64.b64encode(hmac.new(AWS_SECRET_KEY, string, hashlib.sha1).digest())
