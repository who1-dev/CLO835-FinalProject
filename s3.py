import boto3
import random
import os


S3_BUCKET = os.environ.get("S3_BUCKET") or "background-s3-jcaranay"
BG = os.environ.get("BG") or ""

def get_background_image():
    global BG
    if BG == "":
        contents = list_files() or []
        bimage = random.choice(contents)
        BG = bimage["Key"]
 
    return BG


def list_files():
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    # Fetch the list of objects from S3 bucket
    response = s3.list_objects(Bucket=S3_BUCKET)
    
    # Check if 'Contents' exists in the response
    if 'Contents' in response:
        for item in response['Contents']:
            contents.append(item)
    
    return contents

def upload_file(file_name):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, S3_BUCKET, object_name)

    return response

def download_file(file_name):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(S3_BUCKET).download_file(file_name, output)

    return output