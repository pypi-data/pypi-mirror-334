# bpdb

## Overview
The `bpdb` is a Python module designed for reading and interacting with smart meters through an HTTP API. It provides a simple interface for retrieving consumer details and last recharge data.

## Installation

```bash
pip install bpdb
```

## CLI Usage

### Send OTP

```ini
$ bpdb-cli send-otp 01710123456
OTP sent to 01710123456
```

### Login

```ini
$ bpdb-cli login 01710123456 123456
Logged in with phone number 01710123456
```

### Recharge Info

```ini
$ bpdb-cli recharge-info 01710123456 0120100112233
+---------------------+--------------+-------------+--------------------------+
|        Date         | Gross Amount | Energy Cost |          Tokens          |
+---------------------+--------------+-------------+--------------------------+
| 2024-05-01 16:15:04 |     5000     |   4662.19   | 1111-2222-3333-4444-5555 |
| 2024-10-01 17:47:27 |     5000     |   4281.47   | 1111-2222-3333-4444-5555 |
| 2025-01-01 23:41:46 |     5000     |   4785.47   | 1111-2222-3333-4444-5555 |
+---------------------+--------------+-------------+--------------------------+
```

### Consumer Info

```ini
$ bpdb-cli consumer-info                         
+------------------+--------------------+
|     Division     |      Mymensingh    |
|    Meter Type    |          1P        |
|   Account Type   |   Active (Prepaid) |
|   S&D Division   |   S&D Kishoreganj  |
|  Sanction Load   |          4         |
|  Customer Name   | MD. ABDUL HANNAN   |
| Customer Address |      BOTTIRISH     |
| Tariff Category  |    Tariff : LT-A   |
+------------------+--------------------+
```

## Contributing
Contributions are welcome! If you have suggestions for improvements or find bugs, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.