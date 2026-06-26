from datetime import datetime, timedelta, timezone


class DateDelayGenerator:
    @staticmethod
    def get_date_plus_days(days: int) -> datetime:
        return datetime.now(timezone.utc) + timedelta(days=days)
