from flask import Flask, request

app = Flask(__name__)

@app.route('/currency', methods=['GET'])
def currency():
    # отримуємо параметри з URL: http://127.0.0.1:8000/currency?today&key=value
    today = request.args.get('today')
    key = request.args.get('key')

    print(f"Отримано параметри: today={today}, key={key}")

    return "USD - 41.5"

if __name__ == '__main__':
    app.run(port=8000)

