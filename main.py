import datetime
from investment_list import get_recent_investments
from slack_sender import build_slack_block, send_to_slack
import os

SLACK_TOKEN = os.getenv("SLACK_TOKEN")

def run_bot():
    today = datetime.date.today()  # ✅ 여기 쉼표 없이!
    investments = get_recent_investments(today)

    if investments:
        blocks = build_slack_block(investments)
        send_to_slack(token=SLACK_TOKEN, channel="#투자유치소식", blocks=blocks)
    else:
        print("어제 투자 유치 정보 없음")

if __name__ == "__main__":
    run_bot()