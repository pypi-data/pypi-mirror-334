# vickycalulator

**vickycalulator** is a Python package that provides a handful of basic math operations—`add`, `subtract`, `multiply`, and `divide`. Perfect for simple arithmetic in your scripts or notebooks.

![Calculator Illustration](https://via.placeholder.com/500x150?text=Calculator+Image)

## Installation

You can install the latest release directly from [PyPI](https://pypi.org/) using `pip`:

```bash
pip install vickycalulator
```

## Usage

```python
import vickycalulator

print(vickycalulator.add(10, 5))       # 15
print(vickycalulator.subtract(10, 5))  # 5
print(vickycalulator.multiply(10, 5))  # 50
print(vickycalulator.divide(10, 5))    # 2.0
```

### Example
```python
import vickycalulator

a, b = 12, 3
sum_result      = vickycalulator.add(a, b)
difference      = vickycalulator.subtract(a, b)
product         = vickycalulator.multiply(a, b)
quotient        = vickycalulator.divide(a, b)

print(f"{a} + {b} = {sum_result}")
print(f"{a} - {b} = {difference}")
print(f"{a} x {b} = {product}")
print(f"{a} / {b} = {quotient}")
```