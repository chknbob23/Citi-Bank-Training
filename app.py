from flask import Flask
from controllers.bank_controller import bank_blueprint

app = Flask(__name__)

# Register MVC Controller Routes
app.register_blueprint(bank_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
