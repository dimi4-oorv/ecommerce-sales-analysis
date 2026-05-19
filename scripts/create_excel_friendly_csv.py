import csv
from pathlib import Path


INPUT_PATH = Path("data/orders.csv")
OUTPUT_PATH = Path("data/orders_excel_ru.csv")

DECIMAL_COLUMNS = {
    "unit_price",
    "unit_cost",
    "shipping_fee",
    "gross_revenue",
    "discount_amount",
    "net_revenue",
    "profit",
}


def main() -> None:
    with INPUT_PATH.open("r", newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        rows = list(reader)

    for row in rows:
        for column in DECIMAL_COLUMNS:
            row[column] = row[column].replace(".", ",")

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8-sig") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
