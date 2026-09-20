class Employee:
    def __init__(self, name: str, title: str, base_salary: float):
        self.name = name
        self.title = title
        self.base_salary = base_salary

    @property
    def base_salary(self) -> float:
        return self._base_salary

    @base_salary.setter
    def base_salary(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Base salary must be greater than 0.")
        self._base_salary = value

    def calculate_salary(self) -> float:
        """Return the base salary of the employee.

        subclasses add bonuses or commissions on top
        """
        return self.base_salary

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"title={self.title}, "
            f"salary=${self.calculate_salary():,.1f})"
        )


class Manager(Employee):
    """Manager with fixed bonus added to the base salary."""

    def __init__(self, name: str, title: str, base_salary: float, bonus: float):
        super().__init__(name, title, base_salary)
        self.bonus = bonus

    def calculate_salary(self) -> float:
        """Return the total salary of the manager, including bonus."""

        return self.base_salary + self.bonus


class CommissionEmployee(Employee):
    """Employee that receives a base salary and a commission based on sales."""

    def __init__(
        self,
        name: str,
        title: str,
        base_salary: float,
        sales: float,
        commission_rate: float,
    ):
        super().__init__(name, title, base_salary)
        self.sales = sales
        self.commission_rate = commission_rate

    def calculate_salary(self) -> float:
        """Return the total salary of the employee, including commission."""

        return self.base_salary + (self.sales * (self.commission_rate * 0.01))
