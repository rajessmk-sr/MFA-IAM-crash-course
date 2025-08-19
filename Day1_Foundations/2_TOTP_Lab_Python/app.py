from flask import Flask, request, render_template_string
import pyotp, qrcode, io, base64

app = Flask(__name__)
# Create a new secret for the user
totp = pyotp.TOTP(pyotp.random_base32())

@app.route("/")
def index():
    # Generate provisioning URI for authenticator apps
    uri = totp.provisioning_uri("user@example.com", issuer_name="IAM-MFA-Lab")
    qr = qrcode.make(uri)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode()
    return render_template_string("""
        <h2>Scan QR in Google Authenticator</h2>
        <img src="data:image/png;base64,{{qr_b64}}" /><br>
        <form method="POST" action="/verify">
          <input name="otp" placeholder="Enter OTP" />
          <button type="submit">Verify</button>
        </form>
    """, qr_b64=qr_b64)

@app.route("/verify", methods=["POST"])
def verify():
    otp = request.form["otp"]
    return "✅ Success!" if totp.verify(otp) else "❌ Invalid OTP"

if __name__ == "__main__":
    app.run(debug=True)
