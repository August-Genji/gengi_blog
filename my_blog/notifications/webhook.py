import requests

def notify_webhook(payload: dict, url: str):
    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"[Webhook] Sent with status {response.status_code}")
    except Exception as e:
        print(f"[Webhook ERROR] {e}")

