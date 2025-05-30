from flask import Flask
import os
import paramiko

app = Flask(__name__)

# Route to test SFTP connection
@app.route("/test-sftp")
def test_sftp():
    try:
        host = os.environ.get("SFTP_HOST")
        port = 22
        username = os.environ.get("SFTP_USER")
        password = os.environ.get("SFTP_PASS")

        # Connect to SFTP
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Use normalize instead of getcwd
        remote_home = sftp.normalize(".")

        sftp.close()
        transport.close()

        return f"✅ Connected to SFTP. Normalized home: {remote_home}"
    except Exception as e:
        return f"❌ Failed to connect to SFTP.\n{str(e)}", 500

# Route to list files in the SFTP directory
@app.route("/list-files")
def list_files():
    try:
        host = os.environ.get("SFTP_HOST")
        username = os.environ.get("SFTP_USER")
        password = os.environ.get("SFTP_PASS")

        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Get current directory path
        remote_home = sftp.normalize(".")
        files = sftp.listdir(remote_home)

        sftp.close()
        transport.close()

        return f"📁 Files in {remote_home}:<br>" + "<br>".join(files)

    except Exception as e:
        return f"❌ Failed to list files: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
