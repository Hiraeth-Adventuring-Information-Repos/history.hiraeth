import json
import os
import re
from decimal import Decimal, InvalidOperation

def parse_non_standard_date(date_str):
    """
    Parses non-standard chronological keywords into sortable numerical values.
    """
    date_str_lower = date_str.lower()
    if "before the beginning" in date_str_lower:
        return (-1000000000001, 0)
    if "the beginning" in date_str_lower:
        return (-1000000000000, 0)
    if "proto-history" in date_str_lower:
        return (-999999999999, 0)
    if "creation age" in date_str_lower:
        return (-999999999990, 0)
    if "early dragon's age" in date_str_lower:
        return (-100000000001, 0)
    if "dragon's age" in date_str_lower:
        return (-10000000001, 0)
    if "end of the ante-diluvian era" in date_str_lower:
        return (-9000000000, 0)
    return (None, None)

def parse_date(date_str):
    """
    Parses a date string into a tuple of two Decimals for sorting.
    """
    primary_ns, secondary_ns = parse_non_standard_date(date_str)
    if primary_ns is not None:
        return (Decimal(primary_ns), Decimal(secondary_ns))

    original_date_str = date_str
    date_str = date_str.strip()

    # --- FINAL REGEX ATTEMPT ---
    # Look for the first number, which might be negative.
    # This is much simpler and should be more robust.
    match = re.search(r'(-?[\d,]+)', date_str)

    if not match:
        # Fallback for dates without numbers after non-standard checks
        # Hash the string to get a consistent, but arbitrary, order
        return (Decimal(hash(date_str) % 100000), Decimal(0))

    num_str = match.group(1).replace(',', '')
    is_bec = 'bec' in date_str.lower()

    try:
        year = Decimal(num_str)
        if is_bec and year > 0:
            year = -year
    except (InvalidOperation, ValueError):
        print(f"Warning: Could not parse number from date: '{original_date_str}'")
        return (Decimal('9999999'), Decimal('9999999'))

    return (year, year)


def main():
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    all_events = []
    events_by_file = {filename: [] for filename in json_files}

    for filename in json_files:
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                for event in data:
                    event['_original_file'] = filename
                all_events.extend(data)
            except json.JSONDecodeError:
                print(f"Error reading {filename}. Skipping.")
                continue

    all_events.sort(key=lambda x: parse_date(x.get('date', '')))

    for i, event in enumerate(all_events):
        event['order_id'] = f"{i:05d}"

    for event in all_events:
        original_file = event.pop('_original_file')
        events_by_file[original_file].append(event)

    for filename, events in events_by_file.items():
        events.sort(key=lambda x: parse_date(x.get('date', '')), reverse=True)

    for filename, events in events_by_file.items():
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=4)
        print(f"Updated {filename} with new order_ids and chronological sorting.")

if __name__ == '__main__':
    main()
