import pytest

from workshop.ex03_employee import CommissionEmployee, Employee, Manager


@pytest.fixture
def employee() -> Employee:
    return Employee("John Doe", "Software Engineer", 50000)


@pytest.fixture
def manager() -> Manager:
    return Manager("Jane Smith", "Project Manager", 70000, 10000)


@pytest.fixture
def commission_employee() -> CommissionEmployee:
    return CommissionEmployee("Alice Johnson", "Sales Representative", 40000, 200000, 5)


@pytest.fixture
def team(employee, manager, commission_employee) -> list[Employee]:
    return [employee, manager, commission_employee]


class TestEmployee:
    def test_calculate_employee_salary(self, employee) -> None:
        assert employee.calculate_salary() == 50000

    def test_negative_base_salary(self) -> None:
        with pytest.raises(ValueError, match="greater than 0"):
            Employee("John Doe", "Software Engineer", -50000)

    def test_set_negative_base_salary(self, employee) -> None:
        with pytest.raises(ValueError, match="greater than 0"):
            employee.base_salary = -10000

    def test_zero_base_salary(self) -> None:
        with pytest.raises(ValueError, match="greater than 0"):
            Employee("John Doe", "Software Engineer", 0)

    def test_repr_employee(self, employee) -> None:
        expected_repr = (
            "Employee(name=John Doe, title=Software Engineer, salary=$50,000.0)"
        )
        assert repr(employee) == expected_repr


class TestManager:
    def test_calculate_manager_salary(self, manager) -> None:
        assert manager.calculate_salary() == 80000  # 70000 base + 10000 bonus


class TestCommissionEmployee:
    def test_calculate_commission_employee_salary(self, commission_employee) -> None:
        # 40000 base + (200000 * 5%) commission
        assert commission_employee.calculate_salary() == 50_000

    @pytest.mark.parametrize(
        ("sales", "rate", "expected"),
        [
            (0, 5, 30_000),
            (100_000, 0, 30_000),
            (100_000, 5, 35_000),
            (200_000, 2.5, 35_000),
        ],
    )
    def test_commission_scales_with_sales_and_rate(self, sales, rate, expected) -> None:
        e = CommissionEmployee(
            "Ana", "Sales", 30_000, sales=sales, commission_rate=rate
        )
        assert e.calculate_salary() == pytest.approx(expected)


class TestPolymorphismEmployee:
    def test_polymorphic_salary_calculation(self, team) -> None:
        salaries = [employee.calculate_salary() for employee in team]
        # Employee, Manager, CommissionEmployee
        expected_salaries = [50000, 80000, 50000]
        assert salaries == expected_salaries
