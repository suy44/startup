from flask import Flask
import os
import paramiko

app = Flask(__name__)

@app.route("/test-sftp")
def test_sftp():
    try:
        host = os.environ.get("SFTP_HOST")
        port = 22
        username = os.environ.get("SFTP_USER")
        password = os.environ.get("SFTP_PASS")

        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        current_dir = sftp.getcwd()

        sftp.close()
        transport.close()

        return f"✅ Connected to SFTP. Current directory: {current_dir}"

    except Exception as e:
        return f"❌ Failed to connect to SFTP.\n{str(e)}", 500

if __name__ == "__main__":
    import socket
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
