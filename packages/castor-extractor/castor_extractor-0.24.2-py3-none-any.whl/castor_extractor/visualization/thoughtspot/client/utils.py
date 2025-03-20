import csv
import re
from collections.abc import Iterator
from io import StringIO

_END_OF_GENERATED_TEXT = r'^""$'


def usage_liveboard_reader(usage_liveboard_csv: str) -> Iterator[dict]:
    """
    Converts a CSV string into an iterator of dictionaries after
    ignoring the generated text that preceeds the actual CSV header row.
    The generated block ends with a row containing only two double quotes.
    Here is an example:

        "Data extract produced by Castor on 09/19/2024 06:54"
        "Filters applied on data :"
        "User Action IN [pinboard_embed_view,pinboard_tspublic_no_runtime_filter,pinboard_tspublic_runtime_filter,pinboard_view]"
        "Pinboard NOT IN [mlm - availability pinboard,null]"
        "Timestamp >= 20240820 00:00:00 < 20240919 00:00:00"
        "Timestamp >= 20240919 00:00:00 < 20240920 00:00:00"
        ""

    """
    csv_file = StringIO(usage_liveboard_csv)

    line = next(csv_file)
    while not re.match(_END_OF_GENERATED_TEXT, line.strip()):
        line = next(csv_file)

    yield from csv.DictReader(csv_file)
