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
pip install adaptive_floor
```

## 📖 Usage

```python
from precisionfloor import floor_to_precision, adaptive_floor

# Floor a number to 3 decimal places
print(floor_to_precision(12.34567, 3))  # Output: 12.345

# Adaptive flooring based on fractional part
print(adaptive_floor(0.004567))  # Output: 0.00457 (auto-determined decimals)
```

## 📜 License

This project is licensed under the MIT License.
