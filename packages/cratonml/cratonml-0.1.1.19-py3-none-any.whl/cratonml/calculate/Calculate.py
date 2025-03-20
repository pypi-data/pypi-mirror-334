import numpy as np
from abc import ABC, abstractmethod


class Calculate(ABC):
    @staticmethod
    @abstractmethod
    def calculate(values):
        pass


class Average(Calculate):
    @staticmethod
    def calculate(values):
        return np.mean(values)


class Min(Calculate):
    @staticmethod
    def calculate(values):
        return np.min(values)


class Max(Calculate):
    @staticmethod
    def calculate(values):
        return np.max(values)


class Median(Calculate):
    @staticmethod
    def calculate(values):
        sorted_values = sorted(values)
        idx = int(len(sorted_values) // 2)
        return sorted_values[idx]


class Top(Calculate):
    @staticmethod
    def calculate(values):
        return values[0]
