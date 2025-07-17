


def json2table(json_data: list) -> str:
    """
    Convert JSON data to a table format.

    Args:
        json_data (list): List of dictionaries representing JSON data.

    Returns:
        str: A string representation of the table.
    """
    if not json_data:
        return "No data available"

    headers = json_data[0].keys()
    table = [headers]

    for item in json_data:
        row = [str(item.get(header, "")) for header in headers]
        table.append(row)

    # Calculate column widths
    col_widths = [max(len(str(item)) for item in col) for col in zip(*table)]

    # Create formatted table
    formatted_table = []
    for row in table:
        formatted_row = " | ".join(f"{str(item).ljust(col_widths[i])}" for i, item in enumerate(row))
        formatted_table.append(formatted_row)

    return "\n".join(formatted_table)