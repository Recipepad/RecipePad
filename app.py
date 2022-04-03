from flask import Flask
import os

from sqlalchemy import text

from sqlclient import SqlClient
from config import Config

app = Flask(__name__)
client = SqlClient(Config())

@app.route("/")
def hello():
    with client.get_conn() as conn:
        result = conn.execute(text("select VERSION()"))
        version = result.all()[0][0]

    return "Hello RecipePad in Cloud with MySQL" + str(version)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)