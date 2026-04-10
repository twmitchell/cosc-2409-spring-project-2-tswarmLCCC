import re

def extract_log_data(line):
    match = re.search(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - "
        r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - "
        r"\"GET (.+) HTTP/1.1\" (\d+)",
        line
    )

    if match:
        return match.groups()
    return None


def analyze_log_file(filename="access.log"):

    try:
        with open(filename, "r") as f:
            log_lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Log file '{filename}' not found.")
        return

    error_count = 0
    unique_ips = set()
    url_counts = {}

    for line in log_lines:
        data = extract_log_data(line)

        if data:
            timestamp, ip, url, status_code = data

            unique_ips.add(ip)

            url_counts[url] = url_counts.get(url, 0) + 1

            if int(status_code) >= 400:
                error_count += 1

    print("\nTotal Errors (4xx and 5xx):", error_count)
    print("Unique IP Addresses:", len(unique_ips))
    print("URL Access Counts:")

    for url, count in sorted(url_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    {url}: {count}")


# Run analysis
analyze_log_file()
