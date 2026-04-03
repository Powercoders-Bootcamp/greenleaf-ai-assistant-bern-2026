"""
Basel public holidays from OpenHolidays API.

What this script does:
1. Downloads Swiss public holidays for a given year
2. Keeps only non-working holidays for Basel (CH-BS)
3. Includes nationwide holidays
4. Excludes weekends
5. Returns clean, sorted results

Install dependency first:
    pip install requests

Run:
    python openholidays_basel.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, date
from typing import Any

import requests

BASE_URL = "https://openholidaysapi.org/PublicHolidays"
BASEL_CODE = "CH-BS"


@dataclass(frozen=True)
class Holiday:
    name: str
    date: str
    scope: str  # "National" or "Basel"


def fetch_holidays_ch(year: int) -> list[dict[str, Any]]:
    """
    Fetch all holiday records for Switzerland (CH) for a given year.
    """
    params = {
        "countryIsoCode": "CH",
        "languageIsoCode": "EN",
        "validFrom": f"{year}-01-01",
        "validTo": f"{year}-12-31",
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data if isinstance(data, list) else []


def parse_iso_date(date_str: str | None) -> date | None:
    """
    Safely parse YYYY-MM-DD into date object.
    """
    if not date_str or not isinstance(date_str, str):
        return None

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def is_valid_holiday_record(item: Any) -> bool:
    """
    Check whether a holiday record has minimum valid structure.
    """
    if not isinstance(item, dict):
        return False

    if parse_iso_date(item.get("startDate")) is None:
        return False

    names = item.get("name")
    if names is not None and not isinstance(names, list):
        return False

    subdivisions = item.get("subdivisions")
    if subdivisions is not None and not isinstance(subdivisions, list):
        return False

    return True


def is_public_holiday(item: dict[str, Any]) -> bool:
    return item.get("type") == "Public"


def is_full_day_holiday(item: dict[str, Any]) -> bool:
    return item.get("temporalScope") == "FullDay"


def is_weekday_holiday(item: dict[str, Any]) -> bool:
    holiday_date = parse_iso_date(item.get("startDate"))
    return holiday_date is not None and holiday_date.weekday() < 5


def applies_to_basel(item: dict[str, Any]) -> bool:
    """
    Holiday applies to Basel if it is nationwide
    or explicitly contains subdivision CH-BS.
    """
    if item.get("nationwide"):
        return True

    return any(
        isinstance(sub, dict) and sub.get("code") == BASEL_CODE
        for sub in item.get("subdivisions", [])
    )


def extract_english_name(names: list[dict[str, Any]] | None) -> str:
    """
    Extract English holiday name, fallback to first available text.
    """
    if not names:
        return "Unknown"

    for entry in names:
        if isinstance(entry, dict) and entry.get("language") == "EN" and entry.get("text"):
            return str(entry["text"])

    for entry in names:
        if isinstance(entry, dict) and entry.get("text"):
            return str(entry["text"])

    return "Unknown"


def to_holiday(item: dict[str, Any]) -> Holiday:
    """
    Convert raw API record to Holiday dataclass.
    """
    return Holiday(
        name=extract_english_name(item.get("name")),
        date=item.get("startDate", ""),
        scope="National" if item.get("nationwide") else "Basel",
    )


def is_basel_non_working_holiday(item: dict[str, Any]) -> bool:
    """
    Business rules:
    - valid record
    - public holiday
    - full day only
    - weekday only
    - applies to Basel
    """
    return (
        is_valid_holiday_record(item)
        and is_public_holiday(item)
        and is_full_day_holiday(item)
        and is_weekday_holiday(item)
        and applies_to_basel(item)
    )


def get_basel_holidays(year: int) -> list[Holiday]:
    """
    Fetch, validate, filter, deduplicate, and sort Basel holidays.
    """
    raw_holidays = fetch_holidays_ch(year)

    result: list[Holiday] = []
    seen: set[tuple[str, str]] = set()

    for item in raw_holidays:
        if not is_basel_non_working_holiday(item):
            continue

        holiday = to_holiday(item)
        unique_key = (holiday.date, holiday.name)

        if unique_key in seen:
            continue

        seen.add(unique_key)
        result.append(holiday)

    return sorted(result, key=lambda holiday: holiday.date)


if __name__ == "__main__":
    holidays = get_basel_holidays(2026)

    for holiday in holidays:
        print(asdict(holiday))