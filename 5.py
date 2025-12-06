from flask import Flask, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)


def get_usd_rate_for_date(dt: datetime) -> tuple[float, str]:

    base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    date_str = dt.strftime("%Y%m%d")

    params = {
        "date": date_str,
        "json": ""
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    data = response.json()

    usd_record = next((item for item in data if item.get("cc") == "USD"), None)
    if not usd_record:
        raise ValueError("Не знайдено курс USD у відповіді НБУ")

    return usd_record["rate"], usd_record["exchangedate"]


@app.route("/usd-rate", methods=["GET"])
def usd_rate():

    param = request.args.get("param")

    if param not in ("today", "yesterday", "week"):
        return (
            "Помилка: параметр 'param' повинен мати значення "
            "'today', 'yesterday' або 'week', "
            "наприклад: /usd-rate?param=today"
        ), 400

    today = datetime.now().date()

    # ---- today ----
    if param == "today":
        target_date = today
        try:
            rate, exchangedate = get_usd_rate_for_date(
                datetime.combine(target_date, datetime.min.time())
            )
        except Exception as e:
            return f"Сталася помилка при запиті до API НБУ: {e}", 500

        return f"Курс USD на {exchangedate}: {rate} грн"

    # ---- yesterday ----
    if param == "yesterday":
        target_date = today - timedelta(days=1)
        try:
            rate, exchangedate = get_usd_rate_for_date(
                datetime.combine(target_date, datetime.min.time())
            )
        except Exception as e:
            return f"Сталася помилка при запиті до API НБУ: {e}", 500

        return f"Курс USD на {exchangedate}: {rate} грн"

    # ---- week ----
    if param == "week":
        lines = []
        # останні 7 днів: сьогодні і ще 6 назад
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            try:
                rate, exchangedate = get_usd_rate_for_date(
                    datetime.combine(day, datetime.min.time())
                )
                lines.append(f"{exchangedate}: {rate} грн")
            except Exception as e:
                lines.append(f"{day.strftime('%d.%m.%Y')}: помилка ({e})")
        return "\n".join(lines)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)