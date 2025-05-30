from flask import Flask, request
import os
import paramiko

app = Flask(__name__)

@app.route("/upload", methods=["GET"])
def upload_to_sftp():
    try:
        message = request.args.get("message", "Empty message")

        # Save message to a temporary local file
        local_path = "/tmp/uploaded_message.txt"
        with open(local_path, "w") as f:
            f.write(message)

        # SFTP connection details from environment variables
        host = os.environ.get("SFTP_HOST")
        port = 22
        username = os.environ.get("SFTP_USER")
        password = os.environ.get("SFTP_PASS")

        # Connect to SFTP
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Normalize remote home directory path
        remote_home = sftp.normalize(".")
        remote_path = f"{remote_home}/message.txt"

        # Upload the local file to remote path
        sftp.put(local_path, remote_path)

        sftp.close()
        transport.close()

        return f"✅ File uploaded with message: {message}"

    except Exception as e:
        return f"❌ Failed to upload file. Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
