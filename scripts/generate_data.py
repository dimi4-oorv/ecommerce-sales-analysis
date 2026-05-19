import csv
import random
from datetime import date, timedelta
from pathlib import Path


RANDOM_SEED = 42
OUTPUT_PATH = Path("data/orders.csv")


PRODUCTS = [
    ("Wireless Mouse", "Electronics", 24.90, 10.50),
    ("Mechanical Keyboard", "Electronics", 79.90, 38.00),
    ("USB-C Cable", "Electronics", 9.90, 3.20),
    ("Laptop Stand", "Office", 34.90, 14.00),
    ("Notebook Set", "Office", 12.50, 4.10),
    ("Desk Lamp", "Home", 29.90, 11.80),
    ("Coffee Mug", "Home", 11.90, 3.90),
    ("Yoga Mat", "Sports", 26.90, 9.70),
    ("Resistance Bands", "Sports", 18.90, 6.20),
    ("Water Bottle", "Sports", 15.90, 4.80),
]


CITIES = ["Almaty", "Astana", "Shymkent", "Karaganda", "Aktobe", "Atyrau"]
CHANNELS = ["Organic", "Paid Search", "Social Media", "Email", "Referral"]


def random_order_date(start: date, end: date) -> date:
    days_between = (end - start).days
    return start + timedelta(days=random.randint(0, days_between))


def main() -> None:
    random.seed(RANDOM_SEED)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    start_date = date(2025, 1, 1)
    end_date = date(2025, 12, 31)
    customer_ids = [f"C{number:04d}" for number in range(1, 351)]

    rows = []
    for order_number in range(1, 1201):
        product_name, category, unit_price, unit_cost = random.choice(PRODUCTS)
        quantity = random.choices([1, 2, 3, 4, 5], weights=[48, 27, 14, 7, 4])[0]
        discount_pct = random.choices([0, 5, 10, 15, 20], weights=[50, 18, 15, 10, 7])[0]
        shipping_fee = random.choice([0, 2.99, 4.99, 6.99])

        gross_revenue = unit_price * quantity
        discount_amount = gross_revenue * discount_pct / 100
        net_revenue = gross_revenue - discount_amount + shipping_fee
        total_cost = unit_cost * quantity
        profit = net_revenue - total_cost

        rows.append(
            {
                "order_id": f"O{order_number:05d}",
                "order_date": random_order_date(start_date, end_date).isoformat(),
                "customer_id": random.choice(customer_ids),
                "city": random.choice(CITIES),
                "sales_channel": random.choice(CHANNELS),
                "product_name": product_name,
                "category": category,
                "quantity": quantity,
                "unit_price": round(unit_price, 2),
                "unit_cost": round(unit_cost, 2),
                "discount_pct": discount_pct,
                "shipping_fee": shipping_fee,
                "gross_revenue": round(gross_revenue, 2),
                "discount_amount": round(discount_amount, 2),
                "net_revenue": round(net_revenue, 2),
                "profit": round(profit, 2),
            }
        )

    rows.sort(key=lambda row: row["order_date"])

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {OUTPUT_PATH} with {len(rows)} rows")


if __name__ == "__main__":
    main()
