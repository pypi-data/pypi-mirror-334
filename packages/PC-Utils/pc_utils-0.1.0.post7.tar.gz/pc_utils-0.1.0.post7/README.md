# PC\_Utils

A collection of essential utilities for Productivity & Collaboration (P&C) services management, maintenance, and optimization of operational tasks. While applicable to services like Slack, these utilities are designed for broader P&C tasks.

## Features

- **Datetime Utility:** Provides a `Datetime` class with a `date_to_epoch` method that converts a date string to an epoch timestamp.
- **File Management:**
  - `FileManagement.py`: Contains a `FileMgmt` class for file searching and moving. It also includes methods for reading CSV files into a list of Python dictionaries and creating a CSV file from a list of Python dictionaries.&#x20;
  - `FileManagement_w_Azure.py`: Similar to `FileManagement.py`, intended for Azure storage (currently under development and pending testing before production use).
- **Email Extraction:**
  - `ObtainEmails.py`: Contains `get_email_addresses`, a function that extracts unique email addresses from a given string.
- **Runtime Tracking:**
  - `Runtime.py`: Provides a `Runtime` class for calculating and displaying runtime information.

## Installation

Install the package via pip:

```powershell
pip install pc-utils
```

## Usage

Import the relevant classes into your Python code:

```python
from pc_utils.Datetime import Datetime
from pc_utils.FileManagement import FileMgmt
from pc_utils.FileManagement_w_Azure import FileMgmt as AzureFileMgmt
from pc_utils.ObtainEmails import get_email_addresses
from pc_utils.Runtime import Runtime
```

### Example Usage

- **Datetime Conversion:**
  ```python
  from pc_utils.Datetime import Datetime
  dt = Datetime()
  epoch_time = dt.date_to_epoch("2025-03-11")
  print(epoch_time)
  ```
- **File Management:**
  ```python
  from pc_utils.FileManagement import FileMgmt
  fm = FileMgmt()
  fm..createOutputCSVfileFromListOfDictionaries(user_channels, fileName, start_msg = "> Writing results to file... ", no_file_created_msg = "> No channels found. No output file was created.")
  ```
- **Email Extraction:**
  ```python
  from pc_utils.ObtainEmails import get_email_addresses
  emails = get_email_addresses("Contact us at info@example.com and support@example.org.")
  print(emails)
  ```
- **Runtime Tracking:**
  ```python
  from pc_utils.Runtime import Runtime
  rt = Runtime()
  rt.print_time("\n> Start time:")
  <some code here>
  rt.print_time("\n> End time:")
  rt.print_runtime("> Total time:")
  ```

## Contributing

Contributions are welcome! Feel free to submit pull requests with improvements, new features, or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For issues, feature requests, or questions, please open an issue in the repository.

