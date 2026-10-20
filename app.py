from flask import Flask, render_template, request

from cipher.PlayFair import encrypt_text, decrypt_text

app = Flask(__name__)

DEFAULT_KEY = "JEDOLSOMJEDLO"


@app.route("/", methods=["GET", "POST"])
def index():
    encrypt_result = None
    decrypt_result = None

    input_text = ""
    key = DEFAULT_KEY
    error = ""

    if request.method == "POST":
        input_text = request.form.get("text", "")
        key = request.form.get("key", DEFAULT_KEY)
        action = request.form.get("action")

        if not input_text.strip():
            error = "Please enter some text."
        elif not key.strip():
            error = "Please enter a key."
        else:
            try:
                if action == "encrypt":
                    encrypt_result = encrypt_text(input_text, key)


                elif action == "decrypt":
                    decrypt_result = decrypt_text(input_text, key)


                else:
                    error = "Unknown action."

            except ValueError as e:
                error = str(e)

    return render_template(
        "index.html",
        encrypt_result=encrypt_result,
        decrypt_result=decrypt_result,
        input_text=input_text,
        key=key,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)