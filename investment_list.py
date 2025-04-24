import requests
from bs4 import BeautifulSoup
import datetime

def get_recent_investments(reference_date: datetime.date):
    url = "https://startuprecipe.co.kr/invest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"id": "example"})
    rows = table.find("tbody").find_all("tr")

    yesterday = reference_date - datetime.timedelta(days=1)
    today = reference_date
    target_dates = {yesterday, today}

    investments = []

    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 6:
            continue

        date_text = tds[0].text.strip()
        try:
            date = datetime.datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            continue

        if date not in target_dates:
            continue

        investment = {
            "date": date_text,
            "name": tds[1].text.strip(),
            "domain": tds[2].text.strip(),
            "amount": tds[3].text.strip(),
            "stage": tds[4].text.strip(),
            "houses": tds[5].text.strip(),
        }
        investments.append(investment)

    return investments