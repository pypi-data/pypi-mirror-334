"""
===========================================
Tax Calculator - New Tax Regime (FY 2024-25)
===========================================
This package helps calculate income tax under India's new tax regime.

📌 **Features**:
✔ Automatically applies **standard deductions**
✔ Handles **Provident Fund (PF) deductions** (or uses default ₹21,600)
✔ Supports **extra deductions** (if provided)
✔ Uses correct **income tax slabs** for FY 2024-25
✔ Calculates **cess based on income**

============================================
🔹 **How to Use**
============================================

```python
from gang_tax_calculator import NewTaxRegimeCalculator

# ✅ Initialize the calculator
calculator = NewTaxRegimeCalculator()

# ✅ Use case 1: No PF, No Extra Deductions (Defaults Used)
print(calculator.calculate_new_tax(2500000))

# ✅ Use case 2: With PF (User provides ₹30,000 PF, no extra deductions)
print(calculator.calculate_new_tax(2500000, pf=30000))

# ✅ Use case 3: With Extra Deductions (₹1,00,000 extra deductions, default PF ₹21,600)
print(calculator.calculate_new_tax(2500000, extra_deductions=100000))

# ✅ Use case 4: With Both PF & Extra Deductions (User provides ₹30,000 PF and ₹1,00,000 extra deductions)
print(calculator.calculate_new_tax(2500000, pf=30000, extra_deductions=100000))

"""

from .tax_calculator import NewTaxRegimeCalculator

__all__ = ["NewTaxRegimeCalculator"]
