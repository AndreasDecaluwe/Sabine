from codeSabine import * 
from flask import Flask

app = Flask(__name__)

@app.route('/')
def callMain():
    main()


if __name__ == "__main__":
    app.run(debug=True)