from flask import Flask, request
import os
import paramiko

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Middleman is running!"

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()
    filename = data.get("filename", "log.txt")
    content = data.get("content", "")

    # Save content to local file
    with open(filename, "w") as f:
        f.write(content)

    try:
        # Connect to SFTP using paramiko
        host = os.environ.get("SFTP_HOST")
        port = 22
        username = os.environ.get("SFTP_USER")
        password = os.environ.get("SFTP_PASS")

        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Upload file to SFTP server
        remote_path = f"./{filename}"  # or use absolute if required
        sftp.put(filename, remote_path)

        sftp.close()
        transport.close()
        return "✅ File uploaded successfully!"
    except Exception as e:
        return f"❌ Failed to upload via SFTP.\n{str(e)}", 500

if __name__ == "__main__":
    import socket
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
