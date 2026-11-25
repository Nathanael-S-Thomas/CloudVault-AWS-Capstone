import os, boto3
from botocore.exceptions import ClientError
from datetime import datetime
from werkzeug.utils import secure_filename

class Storage:
    def __init__(self):
        self.bucket=os.getenv("AWS_BUCKET_NAME")
        self.region=os.getenv("AWS_REGION","ap-south-1")
        self.mode="s3" if self.bucket else "local"
        self.local_dir=os.getenv("LOCAL_UPLOAD_DIR","uploads")
        os.makedirs(self.local_dir,exist_ok=True)
        self.client=boto3.client("s3",region_name=self.region) if self.mode=="s3" else None

    def list_files(self):
        if self.mode=="local":
            rows=[]
            for name in os.listdir(self.local_dir):
                path=os.path.join(self.local_dir,name)
                if os.path.isfile(path):
                    rows.append({"key":name,"name":name.split("_",1)[-1],"size":os.path.getsize(path),"modified":datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")})
            return sorted(rows,key=lambda x:x["modified"],reverse=True)
        try:
            res=self.client.list_objects_v2(Bucket=self.bucket)
            rows=[]
            for o in res.get("Contents",[]):
                rows.append({"key":o["Key"],"name":o["Key"].split("_",1)[-1],"size":o["Size"],"modified":o["LastModified"].strftime("%Y-%m-%d %H:%M")})
            return sorted(rows,key=lambda x:x["modified"],reverse=True)
        except ClientError:
            return []

    def upload(self, file, key, original):
        try:
            if self.mode=="local":
                file.save(os.path.join(self.local_dir,key))
            else:
                self.client.upload_fileobj(file,self.bucket,key,ExtraArgs={"ContentType":file.content_type or "application/octet-stream"})
            return True, f"{original} uploaded successfully."
        except Exception as e:
            return False, f"Upload failed: {e}"

    def download(self,key):
        if self.mode=="local": return key if os.path.exists(os.path.join(self.local_dir,key)) else None
        try:
            return self.client.generate_presigned_url("get_object",Params={"Bucket":self.bucket,"Key":key},ExpiresIn=300)
        except ClientError: return None

    def delete(self,key):
        try:
            if self.mode=="local":
                path=os.path.join(self.local_dir,key)
                if not os.path.exists(path): return False,"File not found."
                os.remove(path)
            else: self.client.delete_object(Bucket=self.bucket,Key=key)
            return True,"File deleted."
        except Exception as e: return False,f"Delete failed: {e}"
