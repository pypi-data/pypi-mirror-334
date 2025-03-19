# MSV Properties

**MSV Properties** is a Python package designed to simplify managing and processing property-related data with a focus on auction and surplus leads. The package provides a streamlined interface for configuring environments, managing authentication, and processing property leads.

---

## Features

- **Environment Configuration**: Easily set paths for environment files and logs.
- **Flexible Data Handling**: A unified data model for working with diverse property-related datasets.
- **Authentication Management**: Securely manage user credentials for various services.
- **Integrated APIs**: Support for third-party services like Zillow, Propstream, and Tracers.
- **Lead Processing**: Simplifies workflows by automating lead generation and management.

---

## Installation

Install the package via pip:  

```bash
pip install msvproperties
```

---

## Environment File
To use this package, you need to provide a .env file with the necessary environment variables. The .env file should include configuration details such as API credentials and other required settings.

---

## Example Usage
To use this package, you need to provide a .env file with the necessary environment variables. The .env file should include configuration details such as API credentials and other required settings :

- **General Settings**
  - `TOKEN_TIME` = "Enter the token expiration time" (e.g., 3600 for 1 hour)"
  - `BASE_URL` = "Enter app url endpoint"
  - `QUEUE_BASE_URL` = "Enter queue url endpoint"

- **Zillow**
  - `ZILLOW_USERNAME` = "Enter zillow username"
  - `ZILLOW_PASSWORD` = "Enter zillow password"
  - `ZILLOW_BASE_URL` = "Enter zillow base url"

- **Propstream**
  - `PROPSTREAM_USERNAME` = "Enter propstream username"
  - `PROPSTREAM_PASSWORD` = "Enter propstream password"
  - `PROPSTREAM_BASE_URL` = "Enter propstream base url"
  - `PROPSTREAM_LOGIN_URL` = "Enter propstream login url"

- **Tracers**
  - `TRACERS_USERNAME` = "Enter tracers username"
  - `TRACERS_PASSWORD` = "Enter tracers password"
  - `TRACERS_BASE_URL` = "Enter tracers base url"
---

Once the .env file is created, provide its path using the save_configs function, you can call save_configs function only **one time** and if you want to change the path call it again :

```python
from msvproperties import save_configs, Data, AuthManager, Lead

# Configure environment and log paths 
save_configs(
    env_path="/path/to/directory",  # Use "." if the .env file is in the current directory
    log_path="/path/to/directory",  # Path for log file to log failed leads
)

# Authenticate user
session = AuthManager("username", "password")

# Define property data
data = Data(
    session = session,
    is_auction=True,
    is_obit=False,
    source_name="Auction.com",
    full_address="123 Main S Lodi, NJ 12345",  # Include all available columns; leave others blank if not available
)

# Start lead inserting
Lead(session).insert(data)
```

---

## Detailed Explanations

### `save_configs(env_path: str, log_path: str)`
- **Purpose**: Configures the paths for environment variables and log files.
- **Parameters**:
  - `env_path`: Path to the `.env` file or its parent directory.
  - `log_path`: Path to the directory where logs will be saved.

---

### `Data`
- **Purpose**: Represents property-related data with attributes for auctions and surplus leads.
- **Attributes**:
  - `address` (str): address of the property.
  - `is_auction` (bool): Indicates if the property is part of an auction.
  - `is_obit` (bool): If the lead is obit or not.
  - `source_name` (str): Name of the source where the property information is obtained.
  - `opening_bid` (float, optional): Opening bid amount for the auction.
  - `max_debt` (float, optional): Maximum amount of debt associated with the property.
  - `auction_value` (float, optional): Highest bid at the auction.
  - `auction_date` (str, optional): Date of the auction.
  - `property_type` (str, optional): Type of the property (e.g., residential, commercial).
  - `link` (str, optional): Link to the property listing or auction details.
  - `occupancy` (str, optional): Occupancy status of the property.
  - `trustee_name` (str, optional): Name of the trustee handling the auction.
  - `trustee_phone` (str, optional): Phone number of the trustee.
  - `trustee_sale_number` (str, optional): Sale number associated with the trustee.
  - `sold_date` (str, optional): Date the property was sold.
  - `sold_value` (float, optional): Value for which the property was sold.
  - `final_judgment` (float, optional): Final judgment amount.
  - `plaintiff` (str, optional): Plaintiff in the case associated with the property.
  - `attorney_name` (str, optional): Name of the attorney handling the case.
  - `attorney_phone` (str, optional): Phone number of the attorney.
  - `attorney_bar_no` (str, optional): Bar number of the attorney.
  - `attorney_firm` (str, optional): Firm the attorney is associated with.
  - `defendants` (str, optional): Defendants in the case associated with the property.
  - `sales_status` (str, optional): Sales status of the property.
  - `nos_amount` (float, optional): Notice of Sale (NOS) amount.
  - `total_amount_owed` (float, optional): Total amount owed on the property.
  - `document_name` (str, optional): Name of the document related to the property.
  - `case_number` (str, optional): Case number associated with the property.
  - `case_type` (str, optional): Type of the case (e.g., foreclosure, probate).
  - `date_of_filing` (str, optional): Date the case was filed.
  - `probate_case_number` (str, optional): Probate case number (if applicable).

---

### `AuthManager`
- **Purpose**: Handles authentication for API interactions.
- **Parameters**:
  - `username` (str): API username.
  - `password` (str): API password.

---

### `Lead`
- **Purpose**: Manages lead processing based on the provided data and session.
- **Methods**:
  - `insert(data: Data)`: Initiates the lead processing workflow.

---

## Logging and Error Handling

- **Logs**: All failed leads are logged to the specified `log_path` for debugging and reprocessing.
- **Error Handling**: The package includes built-in mechanisms to handle common API errors and invalid data.

---

## Contributing

We welcome contributions from the community! Whether it's fixing bugs, adding new features, or improving documentation, feel free to open a pull request or an issue on our [GitHub repository](https://github.com/alireza-msvproperties/msvproperties/).
