# Day 1 - API Customer Analysis

## Approach
I download the customer list from the JSONPlaceholder API (`https://jsonplaceholder.typicode.com/users`) with `requests`, then work through it in small steps:

1. `get_customers` fetches the data with a 10-second timeout, checks the status code is 200, and prints a clear message (no traceback) if anything fails.
2. `explore` walks one customer and prints every key with its type, going deeper each time it finds a dictionary.
3. `extract_attributes` turns each customer into one flat dictionary (latitude and longitude converted to floats).
4. `unique_cities` uses a set comprehension to find the different cities.
5. `city_counts` (a loop) and `email_domain_counts` (a dict comprehension) count customers, printed from most to least common.
6. `to_dataframe` builds a pandas table; I check that `value_counts()` gives the same numbers as my hand-written counts.
7. The results are saved to CSV files, and two bar charts are saved as PNG files.

## How to run
```bash
git clone <your-repo-url>
cd day1-api-analysis
python -m venv demoenv
source demoenv/Scripts/activate      # Git Bash on Windows

Results appear in the `output/` folder: `customers.csv`, `city_counts.csv`, `customer_distribution.png` and `email_domain_distribution.png`.

## Nested attributes
- `address` is a dictionary holding `street`, `suite`, `city`, `zipcode` and `geo`.
- `geo` is a dictionary inside `address` holding `lat` and `lng`.
- `company` is a dictionary holding `name`, `catchPhrase` and `bs`.

The deepest values are latitude and longitude, reached with `customer["address"]["geo"]["lat"]` (and `["lng"]`).

## Findings
1. The API returns 10 customers, and there are 10 unique cities. Every customer lives in a different city, so there is no city with a group of customers. For marketing, city-based campaigns would reach only one customer each, so other groupings work better.
2. Email endings are more varied than I expected: `biz` and `org` are the most common (2 customers each), and six other endings (`tv`, `net`, `ca`, `info`, `me`, `io`) appear once each.
3. My hand-written counts match pandas `value_counts()` exactly, which shows the counting code is correct.

## Which chart is more useful?
The email-domain chart (`email_domain_distribution.png`) is more useful. The city chart is flat because every city appears exactly once, so it shows no pattern. The email-domain chart has bars of different heights, so you can actually compare groups.

## Assumptions
- "Email domain" means the ending of the email address (for example `biz` in `Sincere@april.biz`).
- `city_counts.csv` has the columns `city` and `customer_count`.
- The API always returns the same fields for every customer.
- Cities are compared exactly as written (same spelling and capital letters).
