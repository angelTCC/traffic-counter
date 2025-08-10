import csv
import os
from datetime import datetime

# -------- SETTINGS -------------------------------------------
CSV_FOLDER = "./data/output/reports"
os.makedirs(CSV_FOLDER, exist_ok=True)

# -------- CSV LOGGING FUNCTION ------------------------------
def write_counts_to_csv(in_count, out_count):

    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(CSV_FOLDER, f"counts_{today_str}.csv")
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "in_count", "out_count", "total"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), in_count, out_count, in_count + out_count])
