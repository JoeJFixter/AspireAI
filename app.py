from flask import Flask, render_template
from api.openai_api import openai_blueprint

app = Flask(__name__)

# Register the OpenAI API blueprint
app.register_blueprint(openai_blueprint)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

