from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def show_ip():
    # Get the IP address of the request
    ip = request.remote_addr

    # Return a response with the IP address
    return f'Your IP address is: {ip}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')