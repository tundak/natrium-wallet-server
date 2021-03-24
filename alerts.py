from datetime import datetime, timezone

HIGH_PRIORITY = "high"
LOW_PRIORITY = "low"

ACTIVE_ALERTS = [
    {
        "id": 6,
        "active": True,
        "priority": HIGH_PRIORITY,
        # yyyy, M,  D,  H,  M,  S, MS
        "timestamp": int((datetime(2021, 3, 24, 1, 0, 0, 0, tzinfo=timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1000),
        "en": {
            "title": "Test message",
            "short_description": "Due to ongoing issues with the Nano network, your transactions may be delayed.",
            "link": "https://appditto.com/blog/natrium-status-and-state-of-the-nano-network",
        },
        "es": {
            "title": "Spanish Test",
            "short_description": "Due to ongoing issues with the Nano network, your transactions may be delayed.",
            "link": "https://appditto.com/blog/natrium-status-and-state-of-the-nano-network",
        },        
    },
    {
        "id": 5,
        "active": True,
        "priority": LOW_PRIORITY,
        "en": {
            "title": "Just a title",
        }
    },
    {
        "id": 4,
        "active": True,
        "priority": LOW_PRIORITY,
        # yyyy, M,  D,  H,  M,  S, MS
        "timestamp": int((datetime(2020, 3, 24, 1, 0, 0, 0, tzinfo=timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1000),
        "en": {
            "title": "Test message 3",
            "long_description": "The Nano network is experiencing issues caused by a prolonged, ongoing period of spam transactions.\n\nTransactions may be significantly delayed, up to several days. We will keep our users updated with new information as the Nano team provides it.\n\nYou can read more by tapping \"Read more\" below.\n\nNatrium is not associated with Nano Foundation or its developers, so even though our service is working normally it still depends on the Nano network to behave normally. We appreciate your patience during this time. The Nano network is experiencing issues caused by a prolonged, ongoing period of spam transactions.\n\nTransactions may be significantly delayed, up to several days. We will keep our users updated with new information as the Nano team provides it.\n\nYou can read more by tapping \"Read more\" below.\n\nNatrium is not associated with Nano Foundation or its developers, so even though our service is working normally it still depends on the Nano network to behave normally. We appreciate your patience during this time. The Nano network is experiencing issues caused by a prolonged, ongoing period of spam transactions.\n\nTransactions may be significantly delayed, up to several days. We will keep our users updated with new information as the Nano team provides it.\n\nYou can read more by tapping \"Read more\" below.\n\nNatrium is not associated with Nano Foundation or its developers, so even though our service is working normally it still depends on the Nano network to behave normally. We appreciate your patience during this time.",
        }
    },
    {
        "id": 3,
        "active": True,
        "priority": LOW_PRIORITY,
        # yyyy, M,  D,  H,  M,  S, MS
        "timestamp": int((datetime(2020, 3, 24, 1, 0, 0, 0, tzinfo=timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1000),
        "en": {
            "title": "Test message 2",
            "long_description": "The Nano network is experiencing issues caused by a prolonged, ongoing period of spam transactions.\n\nTransactions may be significantly delayed, up to several days. We will keep our users updated with new information as the Nano team provides it.\n\nYou can read more by tapping \"Read more\" below.\n\nNatrium is not associated with Nano Foundation or its developers, so even though our service is working normally it still depends on the Nano network to behave normally. We appreciate your patience during this time. The Nano network is experiencing issues caused by a prolonged, ongoing period of spam transactions.\n\nTransactions may be significantly delayed, up to several days. We will keep our users updated with new information as the Nano team provides it.\n\nYou can read more by tapping \"Read more\" below.\n\nNatrium is not associated with Nano Foundation or its developers, so even though our service is working normally it still depends on the Nano network to behave normally. We appreciate your patience during this time. The Nano network is experiencing issues caused by a prolonged, ongoing period of spam transactions.\n\nTransactions may be significantly delayed, up to several days. We will keep our users updated with new information as the Nano team provides it.\n\nYou can read more by tapping \"Read more\" below.\n\nNatrium is not associated with Nano Foundation or its developers, so even though our service is working normally it still depends on the Nano network to behave normally. We appreciate your patience during this time.",
        }
    },
    {
        "id": 2,
        "active": True,
        "priority": HIGH_PRIORITY,
        # yyyy, M,  D,  H,  M,  S, MS
        "timestamp": int((datetime(2020, 3, 24, 1, 0, 0, 0, tzinfo=timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1000),
        "en": {
            "title": "Test message",
            "short_description": "Due to ongoing issues with the Nano network, your transactions may be delayed.",
            "long_description": "The Nano network is experiencing issues caused by a prolonged, ongoing period of spam transactions.\n\nTransactions may be significantly delayed, up to several days. We will keep our users updated with new information as the Nano team provides it.\n\nYou can read more by tapping \"Read more\" below.\n\nNatrium is not associated with Nano Foundation or its developers, so even though our service is working normally it still depends on the Nano network to behave normally. We appreciate your patience during this time.",
        }
    },
    {
        "id": 1,
        "active": True,
        "priority": HIGH_PRIORITY,
        # yyyy, M,  D,  H,  M,  S, MS
        "timestamp": int((datetime(2020, 3, 24, 1, 0, 0, 0, tzinfo=timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1000),
        "en": {
            "title": "Network Issues",
            "short_description": "Due to ongoing issues with the Nano network, your transactions may be delayed.",
            "long_description": "The Nano network is experiencing issues caused by a prolonged, ongoing period of spam transactions.\n\nTransactions may be significantly delayed, up to several days. We will keep our users updated with new information as the Nano team provides it.\n\nYou can read more by tapping \"Read more\" below.\n\nNatrium is not associated with Nano Foundation or its developers, so even though our service is working normally it still depends on the Nano network to behave normally. We appreciate your patience during this time.",
            "link": "https://appditto.com/blog/natrium-status-and-state-of-the-nano-network",
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
            for k, v in a[lang].items():
                retItem[k] = v
            ret.append(retItem)

    return ret
