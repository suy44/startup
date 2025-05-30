from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Middleman is running!"

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()
    filename = data.get("filename", "log.txt")
    content = data.get("content", "")

    # Save content to file
    with open(filename, "w") as f:
        f.write(content)

    # Put file to SFTP via lftp
    sftp_user = os.environ.get("SFTP_USER")
    sftp_pass = os.environ.get("SFTP_PASS")
    sftp_host = os.environ.get("SFTP_HOST")

    sftp_command = f"""
    echo 'put {filename}' | lftp -u {sftp_user},{sftp_pass} sftp://{sftp_host}
    """
    result = os.system(sftp_command)
    if result != 0:
        return "❌ Failed to upload via SFTP.", 500

    return "✅ File uploaded successfully!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT variable
    app.run(host="0.0.0.0", port=port)
