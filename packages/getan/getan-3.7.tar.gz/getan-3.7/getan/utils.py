# -*- coding: utf-8 -*-
#
# (c) 2008, 2009, 2010, 2024 by Intevation GmbH <https://intevation.de>
#   Sascha L. Teichmann <sascha.teichmann@intevation.de>
#   Ingo Weinzierl <ingo.weinzierl@intevation.de>
#
# This is Free Software licensed under the terms of GPLv3 or later.
# For details see LICENSE coming with the source of 'getan'.
#

from decimal import Decimal
import locale
import logging

global DATETIME_FORMAT, TIME_FORMAT
DATETIME_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

logger = logging.getLogger()


def human_time(seconds):
    if seconds is None or seconds == 0:
        return "--:--:--"
    s = seconds % 60
    seconds /= 60
    m = seconds % 60
    seconds /= 60
    out = "%02d:%02d:%02d" % (seconds, m, s)
    return out

def decimal_hours(seconds: int) -> str:
    """Return hours as decimal with max 1 place after locale's decimal_point."""
    if seconds is None:
        return "0"

    hours = Decimal(seconds)/3600

    rounded_to_int = hours.to_integral_value()
    rounded_to_one_place =  hours.quantize(Decimal("0.1"))

    # do not return with a trailing ".0"
    if rounded_to_int == rounded_to_one_place:
        return str(rounded_to_int)
    else:
        d = locale.localeconv()['decimal_point']
        return str(rounded_to_one_place)[0:-2] + d \
             + str(rounded_to_one_place)[-1:]


def safe_int(s, default=0):
    try:
        return int(s)
    except ValueError:
        return default


def short_time(seconds):
    if seconds is None:
        logger.warn(
            "short_time(): No seconds given to format to 'short_time'.")
        return "0:00h"
    seconds /= 60
    m = seconds % 60
    seconds /= 60
    return "%d:%02dh" % (seconds, m)


def format_datetime(datetime):
    return datetime.strftime(DATETIME_FORMAT)


def format_time(datetime):
    return datetime.strftime(TIME_FORMAT)
