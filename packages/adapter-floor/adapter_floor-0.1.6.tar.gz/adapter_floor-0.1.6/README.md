# Adaptive Floor

A Python library for precise number flooring with adaptive decimal precision.
It ensures accurate results without floating-point errors.

## 🚀 Features

- **Floor to Fixed Precision**: Floors a number to a specific number of decimal places.
- **Adaptive Precision**: Dynamically determines the required decimal places based on fractional magnitude.
- **Avoids Precision Loss**: Uses `decimal.Decimal` for high accuracy.

## 📌 Installation

Clone the repository:

```sh
git clone https://github.com/tnam0x/adaptive_floor.git
```

or install via pip:

```sh
pip install adaptive-floor
```

## 📖 Usage

```python
from adaptive_floor import adaptive_floor

# Floor a number to 3 decimal places
print(adaptive_floor(12.34567, 3))  # Output: 12.3456

# Adaptive flooring based on fractional part
print(adaptive_floor(0.004567))  # Output: 0.00456 (auto-determined decimals)
```

## 📜 License

This project is licensed under the GNU General Public License v3.0 (GPLv3).
See the [LICENSE](https://github.com/tnam0x/adaptive_floor/blob/main/LICENSE) file for details.
