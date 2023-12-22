from flask import Flask, render_template, request
from mundobibble import create_app

app = create_app()

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)