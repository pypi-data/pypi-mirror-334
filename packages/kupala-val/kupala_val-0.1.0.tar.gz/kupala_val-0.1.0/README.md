# Kupala Val

Kupala Val is a Python package that serves as an API wrapper around [Kupala-Nich.com](https://kupala-nich.com). It provides easy-to-use interfaces for obtaining valuations, cashflows, and bucketed DV01 (dollar value of a basis point) for portfolios of both listed and derivative financial products.

## Features

- Portfolio valuation for listed and derivative products
- Cashflow analysis and projections
- Bucketed DV01 sensitivity analysis
- Support for both CSV files and pandas DataFrames
- Simple API with comprehensive documentation

## Installation

```bash
pip install kupala_val
```

## Getting Started

### Prerequisites

To use this library, you need:

1. A free account on [Kupala-Nich.com](https://kupala-nich.com)
2. An API key (available in the settings menu in the top right corner after login)

### Setting up your API key

```python
import kupala_val

# Set your API key
kupala_val.set_api_key("your_api_key_here")
```

## Usage Examples

### Working with CSV files

```python
import kupala_val

# Load portfolio from CSV and get valuation
valuation = kupala_val.get_valuation(csv_path="path/to/portfolio.csv")

# Get cashflows
cashflows = kupala_val.get_cashflows(csv_path="path/to/portfolio.csv")

# Get bucketed DV01
dv01 = kupala_val.get_bucketed_dv01(csv_path="path/to/portfolio.csv")
```

### Working with pandas DataFrames

```python
import pandas as pd
import kupala_val

# Load your portfolio data into a DataFrame
df = pd.read_csv("path/to/portfolio.csv")

# Get valuation
valuation = kupala_val.get_valuation(dataframe=df)

# Get cashflows
cashflows = kupala_val.get_cashflows(dataframe=df)

# Get bucketed DV01
dv01 = kupala_val.get_bucketed_dv01(dataframe=df)
```

## Sample Data

The package includes sample portfolio data to help you get started:

```python
# Get sample data as a DataFrame
sample_df = kupala_val.get_sample(format="df")

# Save sample data as a CSV file
sample_csv_path = kupala_val.get_sample(format="csv")
```

## API Documentation

For detailed API documentation, please visit [Kupala-Nich.com/docs](https://kupala-nich.com/docs) or refer to the docstrings in the code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

