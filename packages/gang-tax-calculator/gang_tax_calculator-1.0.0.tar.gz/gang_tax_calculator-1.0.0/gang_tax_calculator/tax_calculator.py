def compute_cess(tax, income):
    """
    Compute the applicable cess based on income levels.
    """
    if income <= 5000000:
        cess_rate = 0.04
    elif income <= 10000000:
        cess_rate = 0.10
    elif income <= 20000000:
        cess_rate = 0.15
    elif income <= 50000000:
        cess_rate = 0.25
    else:
        cess_rate = 0.37

    return tax * cess_rate


def compute_income_tax(taxable_income):
    """
    Compute tax based on income slabs.
    """
    if taxable_income <= 1200000:
        return 0  # No tax if taxable income is ₹12 lakh or below

    tax = 0
    slabs = [
        (400000, 0.00),   # Up to ₹4,00,000 - No tax
        (400000, 0.05),   # ₹4,00,001 to ₹8,00,000 - 5%
        (400000, 0.10),   # ₹8,00,001 to ₹12,00,000 - 10%
        (400000, 0.15),   # ₹12,00,001 to ₹16,00,000 - 15%
        (400000, 0.20),   # ₹16,00,001 to ₹20,00,000 - 20%
        (400000, 0.25),   # ₹20,00,001 to ₹24,00,000 - 25%
        (float('inf'), 0.30)  # Above ₹24,00,000 - 30%
    ]

    remaining_income = taxable_income

    for limit, rate in slabs:
        if remaining_income <= 0:
            break
        taxable_amount = min(remaining_income, limit)
        tax += taxable_amount * rate
        remaining_income -= taxable_amount

    return tax


class NewTaxRegimeCalculator:
    """
    A class to calculate income tax under the new Indian tax regime for FY 2024-2025.
    """

    def __init__(self, default_pf=21600, standard_deduction=75000):
        """
        Initialize default PF amount and standard deduction.
        """
        self.default_pf = default_pf
        self.standard_deduction = standard_deduction

    def get_taxable_income(self, income, pf=None, extra_deductions=0):
        """
        Calculate taxable income after deducting standard deduction and PF.
        Uses PF if provided; otherwise, uses the default value.
        """
        pf_amount = pf if pf is not None else self.default_pf
        taxable_income = income - pf_amount - extra_deductions - self.standard_deduction
        return max(0, taxable_income)

    def calculate_total_tax(self, income, pf=None, extra_deductions=0):
        """
        Compute total tax under the new tax regime.
        Uses PF if provided; otherwise, uses the default PF value.
        """
        taxable_income = self.get_taxable_income(income, pf, extra_deductions)
        tax = compute_income_tax(taxable_income)
        cess = compute_cess(tax, income)
        total_tax = tax + cess
        return round(total_tax, 2)

