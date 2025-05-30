from flask import Flask, request
import os
import paramiko

app = Flask(__name__)

@app.route("/upload", methods=["GET"])
def upload_to_sftp():
    try:
        message = request.args.get("message", "Empty message")

        # Save to a temporary local file on the Render server
        local_path = "/tmp/uploaded_message.txt"
        with open(local_path, "w") as f:
            f.write(message)

        # SFTP connection details
        host = os.environ.get("SFTP_HOST")
        port = 22
        username = os.environ.get("SFTP_USER")
        password = os.environ.get("SFTP_PASS")

        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Change directory explicitly to "home"
        sftp.chdir("home")

        # Upload file in current remote directory ("home")
        remote_path = "message.txt"
        sftp.put(local_path, remote_path)

        sftp.close()
        transport.close()

        return f"✅ File uploaded inside /home with message: {message}"

    except Exception as e:
        return f"❌ Failed to upload file. Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
