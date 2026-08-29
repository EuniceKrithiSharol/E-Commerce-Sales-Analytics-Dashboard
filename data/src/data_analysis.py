import pandas as pd
import numpy as np


def generate_sample_data():

    np.random.seed(42)

    dates = pd.date_range(
        start="2023-01-01",
        end="2024-12-31",
        freq="D"
    )

    categories = [
        "Electronics",
        "Furniture",
        "Clothing",
        "Home Appliances",
        "Sports"
    ]

    regions = [
        "North",
        "South",
        "East",
        "West"
    ]

    products = [
        "Laptop",
        "Smartphone",
        "Office Chair",
        "Table",
        "T-Shirt",
        "Shoes",
        "Washing Machine",
        "Refrigerator",
        "Football",
        "Treadmill"
    ]

    n = 2000

    df = pd.DataFrame({
        "Order_ID": range(1001, 1001 + n),
        "Order_Date": np.random.choice(dates, n),
        "Category": np.random.choice(categories, n),
        "Region": np.random.choice(regions, n),
        "Product": np.random.choice(products, n),
        "Sales": np.random.randint(100, 5000, n),
        "Quantity": np.random.randint(1, 10, n)
    })

    df["Profit"] = (
        df["Sales"] *
        np.random.uniform(0.05, 0.30, n)
    ).round(2)

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"]
    )

    return df


def calculate_summary(df):

    summary = {
        "total_sales": df["Sales"].sum(),
        "total_profit": df["Profit"].sum(),
        "total_orders": df["Order_ID"].nunique(),
        "total_quantity": df["Quantity"].sum()
    }

    return summary


if __name__ == "__main__":

    data = generate_sample_data()

    print("Dataset Generated Successfully")
    print()

    print("Dataset Shape:")
    print(data.shape)

    print()

    print("Summary:")
    print(calculate_summary(data))
