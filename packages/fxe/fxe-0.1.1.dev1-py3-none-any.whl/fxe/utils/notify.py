import pandas as pd
import requests
from finlab.core.report import Report as ReportPyx


def tg_notify(
    self: ReportPyx,
    telegram_token: str = "",
    chat_id: str = "",
    parse_mode: str = "Markdown",
):
    if not isinstance(self, ReportPyx):
        raise Exception("Please provide a valid backtest report.")
    hold = []
    enter = []
    exit = []
    for i, p in self.position_info().items():
        if isinstance(p, dict):
            if i[:4].isdigit():
                if p["status"] in ["exit"] and pd.isnull(
                    self.current_trades.loc[i].exit_date
                ):
                    hold.append(f"{i}: {p['entry_date'][:10]}, {str(p['entry_price'])}")
                if p["status"] in ["hold", "sl", "tp"]:
                    hold.append(f"{i}: {p['entry_date'][:10]}, {str(p['entry_price'])}")
                if p["status"] in ["enter"]:
                    enter.append(f"{i}: {p['entry_date'][:10]}的下個交易日進場")
                if p["status"] in ["exit", "sl", "tp"]:
                    exit.append(f"{i}: {p['exit_date'][:10]}的下個交易日出場")
    message_lines = ["目前策略清單 進場日及進場價格："]
    message_lines.extend(hold)
    message_lines.append("------------------------------")
    message_lines.append("近期操作：")
    message_lines.append("-策略新增")
    if len(enter) > 0:
        message_lines.extend(enter)
    else:
        message_lines.append("尚無")
    message_lines.append("-策略移除")
    if len(exit) > 0:
        message_lines.extend(exit)
    else:
        message_lines.append("尚無")
    message = "\n".join(message_lines)

    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": parse_mode}
    response = requests.post(url, json=payload)
    print(response.json())


def extend_finlab() -> None:
    ReportPyx.tg_notify = tg_notify
