"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


# ---------------------------------------------------------------
# STEP 1: Get the data from the internet
# ---------------------------------------------------------------
def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)  # give up after 10 seconds
    except requests.exceptions.RequestException as error:
        # No internet, slow server, bad address... print a friendly message
        print(f"Could not reach the API. Check your internet connection. Details: {error}")
        return []       # Sends back an empty list

    if response.status_code != 200:  # 200 means "OK", 404 means: not found
        print(f"The API answered with an error. Status code: {response.status_code}")
        return []

    try:
        return response.json()  # turn the text into a Python list
    except ValueError:
        print("The API answered, but the data was not valid JSON.")
        return []


# ---------------------------------------------------------------
# STEP 2: Look inside one customer (dictionaries inside dictionaries)
# ---------------------------------------------------------------
def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    for key, value in record.items():
        print("    " * indent + f"{key}: {type(value).__name__}")
        if isinstance(value, dict):
            explore(value, indent + 1)  # the function calls itself to go deeper


# ---------------------------------------------------------------
# STEP 3: Pick out the pieces we want and make them flat
# ---------------------------------------------------------------
def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = []
    for c in customers:
        email = c["email"]      # Look up the email label
        # "Sincere@april.biz" -> "april.biz" -> "biz"
        email_domain = email.split("@")[1].split(".")[-1]
        rows.append({
            "id": c["id"],
            "name": c["name"],
            "username": c["username"],
            "email": email,
            "email_domain": email_domain,
            "phone": c["phone"],
            "city": c["address"]["city"],
            "zipcode": c["address"]["zipcode"],
            "latitude": float(c["address"]["geo"]["lat"]),    # text -> float
            "longitude": float(c["address"]["geo"]["lng"]),   # text -> float
            "company": c["company"]["name"],
            "website": c["website"],
        })
    return rows


# ---------------------------------------------------------------
# STEP 4: Sets only keep one copy of each value
# ---------------------------------------------------------------
def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {c["address"]["city"] for c in customers}



# ---------------------------------------------------------------
# STEP 5: Count things by hand
# ---------------------------------------------------------------
def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop (no Counter, no pandas)."""
    counts = {}
    for c in customers:
        city = c["address"]["city"]
        if city in counts:
            counts[city] += 1   # seen this city before: add 1
        else:
            counts[city] = 1    # first time we see it: start at 1
    return counts


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    domains = [c["email"].split("@")[1].split(".")[-1] for c in customers]
    return {d: domains.count(d) for d in set(domains)}  # dict comprehension


# ---------------------------------------------------------------
# STEP 6: Put the data in a table (DataFrame)
# ---------------------------------------------------------------
def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)


# ---------------------------------------------------------------
# STEP 8: Draw a chart
# ---------------------------------------------------------------
def plot_distribution(counts: dict[str, int], path: Path, title: str = "Customer distribution") -> None:
    """Save a labelled chart of the distribution to path."""
    ordered = sorted(counts.items(), key=lambda item: item[1], reverse=True)    # Sorts by the numnber not the name
    labels = [name for name, _ in ordered]
    values = [number for _, number in ordered]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color="steelblue")
    plt.title(title)
    plt.xlabel("Category")
    plt.ylabel("Number of customers")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(range(0, max(values) + 1))  # whole numbers only
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def print_sorted(counts: dict[str, int]) -> None:
    """Print a dict from most common to least common."""
    for name, number in sorted(counts.items(), key=lambda item: item[1], reverse=True):
        print(f"  {name}: {number}")


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # STEP 1
    customers = get_customers()
    if not customers:   # If the list is empty then proram stop with message
        raise SystemExit("No data to analyse. Fix the problem above and run again.")
    print(f"Downloaded {len(customers)} customers.\n")

    # STEP 2
    print("--- Structure of one customer ---")
    explore(customers[0])

    # STEP 3
    rows = extract_attributes(customers)

    # STEP 4
    cities = unique_cities(customers)
    print(f"\n--- Unique cities ---")
    print(f"{len(cities)} unique cities for {len(customers)} customers.")
    if len(cities) == len(customers):
        print("Every customer lives in a different city, so no city has a cluster of customers.")
    else:
        print("Some customers share a city, so those cities are good places for local campaigns.")

    # STEP 5
    by_city = city_counts(customers)
    by_domain = email_domain_counts(customers)
    print("\n--- Customers per city (most to least) ---")
    print_sorted(by_city)
    print("\n--- Customers per email domain (most to least) ---")
    print_sorted(by_domain)

    # STEP 6
    df = to_dataframe(rows)
    print(f"\n--- DataFrame ---")
    print("Shape:", df.shape)
    print(df.dtypes)
    pandas_city = df["city"].value_counts().to_dict()
    pandas_domain = df["email_domain"].value_counts().to_dict()
    print("\nPandas city counts match my counts:", pandas_city == by_city)
    print("Pandas email domain counts match my counts:", pandas_domain == by_domain)

    # STEP 7
    df.to_csv(output_dir / "customers.csv", index=False)
    city_table = pd.DataFrame(
        sorted(by_city.items(), key=lambda item: item[1], reverse=True),
        columns=["city", "customer_count"],
    )
    city_table.to_csv(output_dir / "city_counts.csv", index=False)

    # STEP 8
    plot_distribution(by_city, output_dir / "customer_distribution.png",
                      "Customers per city")
    plot_distribution(by_domain, output_dir / "email_domain_distribution.png",
                      "Customers per email domain")

    print("\nDone! Files saved in the output/ folder.")
