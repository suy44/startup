from flask import Flask, request
import os
import paramiko

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Middleman is running!"

@app.route("/upload", methods=["POST"])
def upload():
    try:
        data = request.get_json()
        filename = data.get("filename", "log.txt")
        content = data.get("content", "")

        # Save content to a local file temporarily
        with open(filename, "w") as f:
            f.write(content)

        # Get SFTP credentials from environment variables
        host = os.environ.get("SFTP_HOST")
        port = 22
        username = os.environ.get("SFTP_USER")
        password = os.environ.get("SFTP_PASS")

        # Connect to the SFTP server
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Get the correct default folder (your SFTP home folder)
        remote_home = sftp.normalize(".")
        remote_path = f"{remote_home}/{filename}"

        # Upload the file
        sftp.put(filename, remote_path)

        # Close the connection
        sftp.close()
        transport.close()

        return "✅ File uploaded successfully!"
    
    except Exception as e:
        return f"❌ Failed to upload via SFTP.\n{str(e)}", 500

if __name__ == "__main__":
    import socket
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
