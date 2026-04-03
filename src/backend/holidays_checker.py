"""
Basel holiday service using OpenHolidays API.

Provides two main functions:

1. get_basel_holidays(year) -> list[Holiday]
   Returns all Basel non-weekend public holidays for the given year.
   Output: list of Holiday objects with fields (name, date, scope).

2. is_day_a_holiday(day) -> dict
   Checks if a given date is a holiday.

   Logic:
   - First checks if the date is a weekend
   - If weekend → treated as holiday
   - Otherwise checks Basel public holidays (cached per year)

   Output format (dict):
   {"holiday": bool, "name": str | null, "date": "YYYY-MM-DD", "scope": "National" | "Basel" | null}

Dependencies:
    pip install requests

Errors:
- HolidayAPIError: raised if the OpenHolidays API is unavailable
  or returns invalid data after retries
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime
from functools import lru_cache
from typing import Any
import time

import requests

BASE_URL = "https://openholidaysapi.org/PublicHolidays"
BASEL_CODE = "CH-BS"

MAX_RETRIES = 3
BACKOFF_SECONDS = 2


class HolidayAPIError(Exception):
    """
    Raised when OpenHolidays API cannot be reached
    or returns invalid data after retries.
    """


@dataclass(frozen=True)
class Holiday:
    name: str
    date: date
    scope: str  # "National" or "Basel"


def fetch_holidays_ch(year: int) -> list[dict[str, Any]]:
    """
    Fetch all holiday records for Switzerland (CH) for a given year.
    Retries on temporary API/network errors with simple backoff.
    """
    params = {
        "countryIsoCode": "CH",
        "languageIsoCode": "EN",
        "validFrom": f"{year}-01-01",
        "validTo": f"{year}-12-31",
    }

    max_retries =MAX_RETRIES

    for attempt in range(max_retries):
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if not isinstance(data, list):
                raise HolidayAPIError(
                    f"OpenHolidays API returned unexpected response format for year {year}"
                )

            return data

        except requests.exceptions.RequestException as exc:
            if attempt == max_retries - 1:
                raise HolidayAPIError(
                    f"Failed to fetch holidays from OpenHolidays API for year {year}"
                ) from exc
            time.sleep(BACKOFF_SECONDS * (attempt + 1))

        except ValueError as exc:
            raise HolidayAPIError(
                f"OpenHolidays API returned invalid JSON for year {year}"
            ) from exc

    raise HolidayAPIError(f"Unexpected error while fetching holidays for year {year}")


def parse_iso_date(date_str: str | None) -> date | None:
    """
    Safely parse YYYY-MM-DD into a date object.
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
    holiday_date = parse_iso_date(item.get("startDate"))

    return Holiday(
        name=extract_english_name(item.get("name")),
        date=holiday_date,
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


@lru_cache(maxsize=2)
def get_basel_holidays(year: int) -> list[Holiday]:
    """
    Fetch, validate, filter, deduplicate, and sort Basel holidays.
    Results are cached by year.
    """
    raw_holidays = fetch_holidays_ch(year)

    result: list[Holiday] = []
    seen: set[tuple[date, str]] = set()

    for item in raw_holidays:
        if not is_basel_non_working_holiday(item):
            continue

        found_holiday = to_holiday(item)
        unique_key = (found_holiday.date, found_holiday.name)

        if unique_key in seen:
            continue

        seen.add(unique_key)
        result.append(found_holiday)

    return sorted(result, key=lambda hol: hol.date)


def is_it_weekend(day: date) -> bool:
    """
    Check whether a given date is a weekend.
    Saturday = 5, Sunday = 6.
    """
    return day.weekday() >= 5


def is_it_holiday_in_basel(day: date) -> Holiday | None:
    """
    Return Basel holiday object for a given date if found.
    """
    year_holidays = get_basel_holidays(day.year)

    for hol in year_holidays:
        if hol.date == day:
            return hol
    return None


def is_day_a_holiday(day: date) -> dict[str, Any]:
    """
    Main holiday check pipeline:
    1. Check weekend first
    2. Check Basel holiday second
    3. Return JSON-like dict
    """
    if is_it_weekend(day):
        return {
            "holiday": True,
            "name": "Weekend",
            "date": day.isoformat(),
            "scope": "National",
        }

    hol = is_it_holiday_in_basel(day)

    if hol is not None:
        return {
            "holiday": True,
            "name": hol.name,
            "date": hol.date.isoformat(),
            "scope": hol.scope,
        }

    return {
        "holiday": False,
        "name": None,
        "date": day.isoformat(),
        "scope": None,
    }


if __name__ == "__main__":
    holidays = get_basel_holidays(2026)

    print("=== BASEL HOLIDAYS ===")
    for holiday in holidays:
        print(asdict(holiday))

    print("\n=== DAY CHECK ===")
    print(is_day_a_holiday(date(2026, 1, 1)))
    print(is_day_a_holiday(date(2026, 1, 3)))
    print(is_day_a_holiday(date(2026, 1, 7)))