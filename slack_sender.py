from typing import List, Any, Dict
from collections import defaultdict
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def build_slack_block(investments: List[Dict[str, str]]) -> List[Dict]:
    """
    Builds a styled Slack block message format grouped by date

    Args:
        investments: List of investment dictionaries

    Returns:
        List of Slack blocks formatted according to Slack's Block Kit
    """
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":cool-doge: 어제와 오늘의 투자 유치 소식!",
                "emoji": True
            }
        },
        {"type": "divider"}
    ]

    grouped = defaultdict(list)
    for inv in investments:
        grouped[inv['date']].append(inv)

    for date in sorted(grouped.keys()):
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*\ud83d\uddd3\ufe0f {date}*\n━━━━━━━━━━━━━━"
            }
        })

        for inv in grouped[date]:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f":deal-with-it: *{inv['name']}*\n"
                        f"> {inv['domain']}\n"
                        f":moneybag: {inv['amount']} | :take_my_money: {inv['stage']}\n"
                        f"\ud83c\udfe2 {inv['houses']}"
                    )
                }
            })

        blocks.append({"type": "divider"})

    return blocks

def send_to_slack(token: str, channel: str, blocks: List[Dict[str, Any]]) -> bool:
    """
    Send formatted blocks to Slack channel.
    """
    client = WebClient(token=token)

    try:
        client.chat_postMessage(
            channel=channel,
            blocks=blocks
        )
        return True
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")
        return False
