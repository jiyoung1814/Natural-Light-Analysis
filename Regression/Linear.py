import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def reformat_poly_x_y(x, y, degree):
    x = np.array(x).reshape(-1, 1)
    y = np.array(y)

    poly_features = PolynomialFeatures(degree=degree)
    x_poly = poly_features.fit_transform(x)

    return x_poly, y

def polynomial_linear_regression(x, y, degree=1, intercept=True):
    '''
    다항선형회귀식 생성
    :param x:
    :param y:
    :param degree: 차수
    :param intercept: 절편 유무
    :return:
    '''
    x_poly, y = reformat_poly_x_y(x,y, degree)

    model = LinearRegression(fit_intercept=intercept)
    model.fit(x_poly, y)

    # # Print coefficients
    # print("Coefficients (cubic regression):", model.coef_)
    # print("Intercept (cubic regression):", model.intercept_)

    return model


def polynomial_equation(model):
    coef = model.coef_
    intercept = model.intercept_
    equation = f"y = {intercept}"
    for i in range(1, len(coef)):
        equation += f" + {coef[i]}x^{i}"
    return equation


def polynomial_regression_line_data(x, model):
    x_values = np.linspace(min(x), max(x), 100).reshape(-1, 1)

    poly_features = PolynomialFeatures(degree=len(model.coef_) - 1)
    x_poly = poly_features.fit_transform(x_values)

    y_predict = model.predict(x_poly)

    equation = polynomial_equation(model)

    return [x[0] for x in x_values], y_predict, equation


def predict_regression(x, model):
    x_values = np.array(x).reshape(-1, 1)
    poly_features = PolynomialFeatures(degree=len(model.coef_) - 1)
    x_poly = poly_features.fit_transform(x_values)
    y_predict = model.predict(x_poly)

    return y_predict


def evaluation_model(y, y_predict, evaluation_type='RMSE'):
    '''

    :param y:
    :param y_predict:
    :param evaluation_type: MAE, MSE, RMSE, R2
    :return:
    '''

    evaluation_value = 0

    if evaluation_type == 'R2':
        evaluation_value = r2_score(y, y_predict)
    elif evaluation_type == 'MAE':
        evaluation_value = mean_absolute_error(y, y_predict)

    # mae = mean_absolute_error(test_targets, predictions)
    # mse = mean_squared_error(test_targets, predictions)
    # rmse = mean_squared_error(test_targets, predictions, squared=False)

    return evaluation_value


def best_polynomial_linear_regression_model(x, y, degrees=[2,3,4,5], intercept=True):
    best_model = None
    best_r2_score = 0
    for degree in degrees:
        x_poly, y = reformat_poly_x_y(x,y,degree)

        model = LinearRegression(fit_intercept=intercept)
        model.fit(x_poly, y)

        r2_score = model.score(x_poly, y)
        # print(f'{degree}_degree_r2_score: {r2_score}')
        if r2_score > best_r2_score:
            best_model = model

    return best_model
