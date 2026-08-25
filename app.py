from flask import Flask, render_template, send_file
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import io

app = Flask(__name__)

# Azure Blob Storage configuration
STORAGE_ACCOUNT_NAME = "projectblobstorage123"

account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"

credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
    account_url=account_url,
    credential=credential
)

container_client = blob_service_client.get_container_client("images")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")


# Get image from Azure Blob Storage
@app.route("/product-image")
def product_image():

    blob_client = container_client.get_blob_client("product.jpg")

    image_data = blob_client.download_blob().readall()

    return send_file(
        io.BytesIO(image_data),
        mimetype="image/jpeg"
    )


if __name__ == "__main__":
    app.run()
