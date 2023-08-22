import os
import time
import boto3

def upload_files_to_s3(event, context):
    s3_client = boto3.client('s3')
    folder_path = 'C:/CSCI5410/A3/t'

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            time.sleep(0.1)  # Delay of 100 milliseconds

            try:
                s3_client.upload_file(file_path, 'sampledata-b00932103', filename)
                print(f"Uploaded {filename} to S3 bucket")
            except Exception as e:
                print(f"Failed to upload {filename}: {str(e)}")

    return 'Upload completed'

upload_files_to_s3(None, None)
