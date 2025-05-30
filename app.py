from flask import Flask, request
import os
import paramiko

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_to_sftp():
    try:
        message = request.form.get("message", "Empty message")

        # Save to a temporary local file
        local_path = "/tmp/uploaded_message.txt"
        with open(local_path, "w") as f:
            f.write(message)

        # SFTP connection
        host = os.environ.get("SFTP_HOST")
        port = 22
        username = os.environ.get("SFTP_USER")
        password = os.environ.get("SFTP_PASS")

        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Normalize path and upload
        remote_home = sftp.normalize(".")
        remote_path = f"{remote_home}/message.txt"
        sftp.put(local_path, remote_path)

        sftp.close()
        transport.close()

        return "✅ Message uploaded successfully via SFTP."

    except Exception as e:
        return f"❌ Failed to upload via SFTP.<br>[Error] {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
