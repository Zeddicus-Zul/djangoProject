from storages.backends.gcloud import GoogleCloudStorage

class StaticGCSStorage(GoogleCloudStorage):
    location = "static"