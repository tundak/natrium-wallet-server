from datetime import datetime, timezone

HIGH_PRIORITY = "high"
LOW_PRIORITY = "low"

ACTIVE_ALERTS = [
    {
        "id": 1,
        "active": True,
        "priority": HIGH_PRIORITY,
        # yyyy, M,  D,  H,  M,  S, MS
        "timestamp": int((datetime(2020, 3, 24, 1, 0, 0, 0, tzinfo=timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1000),
        "link": "https://appditto.com/blog/natrium-status-and-state-of-the-nano-network",
        "en": {
            "title": "Network Issues",
            "short_description": "Due to ongoing issues with the Nano network, many transactions are delayed.",
            "long_description": "The Nano network is experiencing issues caused by a prolonged, ongoing period of spam transactions.\n\nSome transactions may be significantly delayed, up to several days. We will keep our users updated with new information as the Nano team provides it.\n\nYou can read more by tapping \"Read More\" below.\n\nAll issues in regards to transaction delays are due to the Nano network issues, not Natrium. We are not associated with the Nano Foundation or its developers.\n\nWe appreciate your patience during this time."
        }
    }
]


def get_active_alert(lang: str):
    ret = []
    for a in ACTIVE_ALERTS:
        active = a["active"]
        if active:
            if lang not in a:
                lang = 'en'
            retItem = {
                "id": a["id"],
                "priority": a["priority"],
                "active": a["active"],
            }
            if "timestamp" in a:
                retItem["timestamp"] = a["timestamp"]
            if "link" in a:
                retItem["link"] = a["link"]
            for k, v in a[lang].items():
                retItem[k] = v
            ret.append(retItem)

    return ret
