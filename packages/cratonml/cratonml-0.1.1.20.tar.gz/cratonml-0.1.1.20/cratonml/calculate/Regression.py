import numpy as np
from sklearn import linear_model


class RANSACRegression:
    """ Класс для RANdom SAmple Consensus регрессии"""

    @staticmethod
    def get_model(x_train: np.ndarray, y_train: np.ndarray):
        """
        Возвращает модель обученную на тренировочных данных.

        Parameters
        ----------
        x_train: np.ndarray
            Массив значений размера (N, M). Где N - количество точек, M - количество атрибутов.
        y_train: np.ndarray
            Массив значений размера N.

        Returns
        -------
        RANSACRegressor
            Обученная модель.
        """
        assert x_train.ndim == 2, "x_train: Ожидался 2D массив"
        assert y_train.ndim == 1, "y_train: Ожидался 1D массив"
        assert x_train.shape[0] == y_train.shape[0], "Массив y_train имеет несоответствующую длину"

        model = linear_model.RANSACRegressor()
        model.fit(x_train, y_train)
        return model

    @staticmethod
    def predict(model: linear_model.RANSACRegressor, x_test: np.ndarray):
        """
         Прогнозирует значения для тестового набора данных.

        Parameters
        ----------
        model: RANSACRegressor
            Обученная модель.
        x_test: np.ndarray
            Массив значений размера (N, M). Где N - количество точек, M - количество размерностей.

        Returns
        -------
        np.ndarray
            Массив значений размера N.
        """

        assert x_test.ndim == 2, "x_test: Ожидался 2D массив"

        prediction = model.predict(x_test)
        return prediction

    @staticmethod
    def get_coeffs(model: linear_model.RANSACRegressor):
        """
         Получает коэффициенты линейной регрессии.

        Parameters
        ----------
        model: RANSACRegressor
            Обученная модель.

        Returns
        -------
        a: float
            Коэффициент, отвечающий за наклон.
        b: float
            Коэффициент, отвечающий за смещение.
        """

        a = model.estimator_.coef_
        b = model.estimator_.intercept_
        return a, b


class LinearRegression:
    """ Класс для линейной регрессии"""

    @staticmethod
    def get_model(x_train: np.ndarray, y_train: np.ndarray):
        """
        Возвращает модель обученную на тренировочных данных.

        Parameters
        ----------
        x_train: np.ndarray
            Массив значений размера (N, M). Где N - количество точек, M - количество размерностей.
        y_train: np.ndarray
            Массив значений размера N.

        Returns
        -------
        LinearRegression
            Обученная модель.
        """
        assert x_train.ndim == 2, "x_train: Ожидался 2D массив"
        assert y_train.ndim == 1, "y_train: Ожидался 1D массив"
        assert x_train.shape[0] == y_train.shape[0], "Массив y_train имеет несоответствующую длину"

        model = linear_model.LinearRegression()
        model.fit(x_train, y_train)
        return model

    @staticmethod
    def predict(model: linear_model.LinearRegression, x_test: np.ndarray):
        """
         Прогнозирует значения для тестового набора данных.

        Parameters
        ----------
        model: RANSACRegressor
            Обученная модель.
        x_test: np.ndarray
            Массив значений размера (N, M). Где N - количество точек, M - количество размерностей.

        Returns
        -------
        np.ndarray
            Массив значений размера N.
        """

        assert x_test.ndim == 2, "x_test: Ожидался 2D массив"

        prediction = model.predict(x_test)
        return prediction

    @staticmethod
    def get_coeffs(model: linear_model.LinearRegression):
        """
         Получает коэффициенты линейной регрессии.

        Parameters
        ----------
        model: LinearRegression
            Обученная модель.

        Returns
        -------
        a: float
            Коэффициент, отвечающий за наклон.
        b: float
            Коэффициент, отвечающий за смещение.
        """

        a = model.coef_
        b = model.intercept_
        return a, b
