def json2table(json_data: list) -> str:
    """
    Convert JSON data to a Markdown table.

    Args:
        json_data (list): List of dictionaries representing JSON data.

    Returns:
        str: A string representation of the Markdown table.
    """
    if not json_data:
        return "No data available"

    # 获取所有字段名作为表头
    headers = json_data[0].keys()

    # 构建表格行
    rows = []
    for item in json_data:
        row = [str(item.get(header, "")) for header in headers]
        rows.append(row)

    # 构建 Markdown 表格
    markdown_table = []

    # 添加表头
    markdown_table.append(" | ".join(headers))

    # 添加分隔线
    markdown_table.append(" | ".join(["---"] * len(headers)))

    # 添加数据行
    for row in rows:
        markdown_table.append(" | ".join(row))

    return "\n".join(markdown_table)
