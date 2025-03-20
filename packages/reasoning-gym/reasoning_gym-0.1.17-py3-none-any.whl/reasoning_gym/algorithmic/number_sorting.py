"""Number sorting task generator"""

from dataclasses import dataclass
from random import Random
from typing import Optional

from ..coaching import BaseCurriculum, RangeAttributeDefinition
from ..factory import ProceduralDataset, register_dataset


@dataclass
class NumberSortingConfig:
    """Configuration for number sorting task generation"""

    min_numbers: int = 3  # Minimum numbers to sort
    max_numbers: int = 10  # Maximum numbers to sort
    min_decimals: int = 0  # Minimum decimal places
    max_decimals: int = 2  # Maximum decimal places
    min_value: float = -100.0  # Minimum value
    max_value: float = 100.0  # Maximum value
    seed: Optional[int] = None
    size: int = 500  # Virtual dataset size

    def validate(self) -> None:
        """Validate configuration parameters"""
        assert self.min_numbers > 0, "min_numbers must be positive"
        assert self.min_numbers <= self.max_numbers, "max_numbers must be >= min_numbers"
        assert self.min_decimals >= 0, "min_decimals must be non-negative"
        assert self.min_decimals <= self.max_decimals, "max_decimals must be >= min_decimals"
        assert self.min_value < self.max_value, "max_value must be > min_value"


class NumberSortingDataset(ProceduralDataset):
    """Generates number sorting tasks"""

    def __init__(self, config: NumberSortingConfig):
        super().__init__(config=config, seed=config.seed, size=config.size)
        self.added_instruction = """
Please follow the instruction below:
## 1. Let all your answers be a list of numbers. Instead of reporting your answer as -69, -13, 1, 7, 11, 43, 59, 61, use ['-69', '-13', '1', '7', '11', '43', '59', '61'] instead
## 2. Convert all numbers in the square brackets as strings. For example, ['-69', '-13', '1', '7', '11', '43', '59', '61']
"""

    def _format_number(self, num: float, decimals: int) -> str:
        """Format number with specified decimal places"""
        formatted = f"{num:.{decimals}f}"
        # Reparse to ensure exact decimal representation
        return f"{float(formatted):.{decimals}f}"

    def _generate_numbers(self, rng: Random, count: int) -> tuple[list[float], list[str]]:
        """Generate list of numbers and their string representations"""
        numbers = []
        number_strs = []

        for _ in range(count):
            num = rng.uniform(self.config.min_value, self.config.max_value)
            decimals = rng.randint(self.config.min_decimals, self.config.max_decimals)
            num_str = self._format_number(num, decimals)
            # Reparse to ensure exact value
            num = float(num_str)
            numbers.append(num)
            number_strs.append(num_str)

        return numbers, number_strs

    def __getitem__(self, idx: int) -> dict:
        """Generate a single sorting task"""
        rng = Random(self.seed + idx)

        count = rng.randint(self.config.min_numbers, self.config.max_numbers)
        numbers, number_strs = self._generate_numbers(rng, count)

        # Generate both ascending and descending answers
        asc_numbers = sorted(numbers)
        desc_numbers = sorted(numbers, reverse=True)

        # Format answers as string lists
        decimals = len(number_strs[0].split(".")[-1]) if "." in number_strs[0] else 0
        asc_answer = [self._format_number(n, decimals) for n in asc_numbers]
        desc_answer = [self._format_number(n, decimals) for n in desc_numbers]

        # Randomly choose ascending or descending
        is_ascending = rng.choice([True, False])
        direction = "ascending" if is_ascending else "descending"
        answer = asc_answer if is_ascending else desc_answer
        question = f"Sort these numbers in {direction} order: {', '.join(number_strs)}" + self.added_instruction

        return {
            "question": question,
            "answer": str(answer),
            "metadata": {
                "original_numbers": number_strs,
                "direction": direction,
                "sorted_numbers": answer,
                "difficulty": {
                    "numbers": count,
                    "decimals": (self.config.min_decimals, self.config.max_decimals),
                    "value": (self.config.min_value, self.config.max_value),
                },
            },
        }


class NumberSortingCurriculum(BaseCurriculum):
    def __init__(self):
        super().__init__(NumberSortingCurriculum.__name__, NumberSortingConfig)

        # Define attributes
        self._define_attributes(
            RangeAttributeDefinition(
                name="numbers",
                levels=[10, 100, 500, 1000],
                description="How many numbers to sort",
                lower_field_name="min_numbers",
                upper_field_name="max_numbers",
                ensure_interval=True,
            ),
            RangeAttributeDefinition(
                name="decimals",
                levels=[0, 2, 4, 6],
                description="Number of decimal places",
                lower_field_name="min_decimals",
                upper_field_name="max_decimals",
                ensure_interval=True,
            ),
            RangeAttributeDefinition(
                name="value",
                levels=[-10_000, 10_000],
                description="Range of numbers to sort",
                lower_field_name="min_value",
                upper_field_name="max_value",
                ensure_interval=True,
            ),
        )


register_dataset("number_sorting", NumberSortingDataset, NumberSortingConfig, NumberSortingCurriculum)
