# scoreapp/servicenow_client.py
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

def create_error_record(payload: dict):
    """
    payload: dict with keys matching your table fields:
      u_user_name, u_user_email, u_where_error, u_description, u_page_url, u_severity
    """
    base = settings.SERVICE_NOW_INSTANCE.rstrip("/")
    table = settings.SERVICE_NOW_TABLE
    url = f"{base}/api/now/table/{table}"

    auth = HTTPBasicAuth(settings.SERVICE_NOW_USER, settings.SERVICE_NOW_PASS)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    try:
        resp = requests.post(url, auth=auth, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        return {"ok": True, "response": resp.json()}
    except requests.RequestException as e:
        # return structured error back to caller
        return {"ok": False, "error": str(e), "status_code": getattr(e.response, "status_code", None)}
