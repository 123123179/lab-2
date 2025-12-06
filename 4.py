from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.route("/content-type-demo", methods=["GET"])
def content_type_demo():
    content_type = request.headers.get("Content-Type", "")

    data = {
        "message": "Приклад відповіді Content-Type",
        "status": "ok"
    }

    if content_type == "application/json":
        return jsonify(data)

    elif content_type == "application/xml":
        xml_body = f"""
        <response>
            <message>{data["message"]}</message>
            <status>{data["status"]}</status>
        </response>
        """.strip()

        response = make_response(xml_body)
        response.headers["Content-Type"] = "application/xml"
        return response

    else:
        return "Content-Type не задано або має невідоме значення. Отримано звичайний текст."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)