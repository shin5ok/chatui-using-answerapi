from google.cloud import storage
import datetime

# You need a service account file, cannot use ADC auth flow
def get_authenticated_url(gcs_path, expiration=60):

    path_parts = gcs_path.replace("gs://", "").split("/", 1)
    bucket_name = path_parts[0]
    object_name = path_parts[1] if len(path_parts) > 1 else ""

    storage_client = storage.Client()

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(seconds=expiration),
            method="GET"
        )

        return url

    except Exception as e:
        print(e)
        return ""

if __name__ == "__main__":
    import sys
    gcs_path = sys.argv[1]
    url = get_authenticated_url(gcs_path)
    print(url)
