from datetime import datetime, timedelta, timezone


class DateDelayGenerator:

    def get_date_plus_days(self, days: int) -> datetime:
        return datetime.now(timezone.utc) + timedelta(days=days)

    def get_date_plus_hours(self, hours: int) -> datetime:
        return datetime.now(timezone.utc) + timedelta(hours=hours)

    def get_current_utc_time(self) -> datetime:
        return datetime.now(timezone.utc)
