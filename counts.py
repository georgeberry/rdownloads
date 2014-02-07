from flask import Flask, redirect, render_template

#flask globals

app = Flask(__name__)

#flask
@app.route('/')
def draw_counts():
    with open('counts.txt', 'rb') as f:
        counts = f.read()

    return "There have been {} downloads of Blaunet".format(counts)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)