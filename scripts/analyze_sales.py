from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_PATH = Path("data/orders.csv")
REPORTS_DIR = Path("reports")


def save_report(frame: pd.DataFrame, filename: str) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(REPORTS_DIR / filename, index=False)


def save_bar_chart(
    frame: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    filename: str,
    color: str,
) -> None:
    plt.figure(figsize=(10, 5))
    plt.bar(frame[x_column], frame[y_column], color=color)
    plt.title(title)
    plt.xlabel(x_column.replace("_", " ").title())
    plt.ylabel(y_column.replace("_", " ").title())
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / filename, dpi=160)
    plt.close()


def save_line_chart(
    frame: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    filename: str,
    color: str,
) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(frame[x_column], frame[y_column], marker="o", color=color, linewidth=2)
    plt.title(title)
    plt.xlabel(x_column.replace("_", " ").title())
    plt.ylabel(y_column.replace("_", " ").title())
    plt.xticks(rotation=35, ha="right")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / filename, dpi=160)
    plt.close()


def main() -> None:
    orders = pd.read_csv(DATA_PATH, parse_dates=["order_date"])

    monthly_sales = (
        orders.assign(month=orders["order_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .agg(
            orders=("order_id", "count"),
            customers=("customer_id", "nunique"),
            net_revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
        )
    )
    monthly_sales["profit_margin_pct"] = (
        monthly_sales["profit"] / monthly_sales["net_revenue"] * 100
    ).round(2)

    category_performance = (
        orders.groupby("category", as_index=False)
        .agg(
            orders=("order_id", "count"),
            units_sold=("quantity", "sum"),
            net_revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
            avg_discount_pct=("discount_pct", "mean"),
        )
        .sort_values("net_revenue", ascending=False)
    )
    category_performance["profit_margin_pct"] = (
        category_performance["profit"] / category_performance["net_revenue"] * 100
    ).round(2)
    category_performance["avg_discount_pct"] = category_performance[
        "avg_discount_pct"
    ].round(2)

    channel_performance = (
        orders.groupby("sales_channel", as_index=False)
        .agg(
            orders=("order_id", "count"),
            customers=("customer_id", "nunique"),
            net_revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values("net_revenue", ascending=False)
    )
    channel_performance["revenue_per_order"] = (
        channel_performance["net_revenue"] / channel_performance["orders"]
    ).round(2)

    customer_summary = (
        orders.groupby("customer_id", as_index=False)
        .agg(
            orders=("order_id", "count"),
            first_order=("order_date", "min"),
            last_order=("order_date", "max"),
            net_revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values("net_revenue", ascending=False)
    )
    customer_summary["customer_type"] = customer_summary["orders"].apply(
        lambda value: "Returning" if value > 1 else "One-time"
    )

    kpi_summary = pd.DataFrame(
        [
            {
                "total_orders": orders["order_id"].nunique(),
                "total_customers": orders["customer_id"].nunique(),
                "total_net_revenue": round(orders["net_revenue"].sum(), 2),
                "total_profit": round(orders["profit"].sum(), 2),
                "average_order_value": round(orders["net_revenue"].mean(), 2),
                "returning_customer_share_pct": round(
                    (
                        customer_summary["customer_type"].eq("Returning").mean()
                        * 100
                    ),
                    2,
                ),
            }
        ]
    )

    save_report(kpi_summary, "kpi_summary.csv")
    save_report(monthly_sales, "monthly_sales.csv")
    save_report(category_performance, "category_performance.csv")
    save_report(channel_performance, "channel_performance.csv")
    save_report(customer_summary.head(20), "top_customers.csv")

    save_line_chart(
        monthly_sales,
        "month",
        "net_revenue",
        "Monthly Net Revenue",
        "monthly_revenue.png",
        "#2f6f73",
    )
    save_bar_chart(
        category_performance,
        "category",
        "profit",
        "Profit by Category",
        "profit_by_category.png",
        "#d08c60",
    )
    save_bar_chart(
        channel_performance,
        "sales_channel",
        "net_revenue",
        "Revenue by Sales Channel",
        "revenue_by_channel.png",
        "#4f6d7a",
    )

    print("Analysis complete. Reports saved to reports/")


if __name__ == "__main__":
    main()
