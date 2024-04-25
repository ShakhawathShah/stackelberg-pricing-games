"""
A simple leader for the Stackelberg game.
"""
from base_leader import Leader
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
import numpy as np
from scipy.optimize import minimize_scalar, minimize

___author___ = "Rokas"


class SimpleLeader(Leader):
    data_set_X = np.array([])
    data_set_Y = np.array([])
    test_result = np.array([])
    weight = np.array([])
    reg = None
    date = 100

    def __init__(self, name):
        # If you want to initialize something here, do it before the super() call.
        super().__init__(name)

    def new_price(self, date: int) -> float:
        """
        A function for setting the new price of each day.
        :param date: date of the day to be updated
        :return: (float) price for the day
        """
        self.log(date)

        self.update_prediction(date)

        A = self.reg.coef_[0]
        B = self.reg.intercept_

        def profit_ul(x):
            part1 = (-A*x**2)+(3*A*x)-(2*A)+B
            part2 = 1 - 0.3*A*x + 0.3*A
            part3 = part1/part2
            part4 = 2 - x + 0.3 * part3
            return ((x - 1) * part4)

        # # find optimal solution
        price = minimize_scalar(
            lambda x: -profit_ul(x), method="Bounded", bounds=(1, 2)).x

        # self.reg.fit(self.data_set_X.reshape(-1, 1), self.data_set_Y)

        # price = minimize_scalar(
        #     lambda x: -self.profit(x, self.reg.predict([[x]])[0]), method="Bounded", bounds=(1, 2)).x

        # returns the leader price based on the predicted follower price
        self.date = date

        return float(price)

    def start_simulation(self):
        """
        A function run at the beginning of the simulation.
        """
        self.log("Start of simulation")
        self.test_result = np.array([])
        self.data_set_X = np.array([])
        self.data_set_Y = np.array([])
        self.reg = LinearRegression()

        x, y = [], []
        for i in range(1, 101):
            price = self.get_price_from_date(i)
            x.append(price[0])
            y.append(price[1])

        self.data_set_X = np.array(x)
        self.data_set_Y = np.array(y)

        transformed_X = self.profit(
            self.data_set_X, self.data_set_Y)
        self.reg.fit(transformed_X.reshape(-1, 1), self.data_set_Y)

    def end_simulation(self):
        """
        A function run at the end of the simulation.
        """
        self.log("End of simulation")
        # self.log(
        #     f"Mean percentage error: {mean_absolute_percentage_error(self.data_set_Y[-30:], self.test_result)*100}")

    def update_prediction(self, date):
        previous_leader, previous_follower = self.get_price_from_date(date - 1)

        self.data_set_X = np.append(self.data_set_X, previous_leader)

        self.data_set_Y = np.append(self.data_set_Y, previous_follower)
        sample_weight = np.asarray([])
        for i in range(1, date+1):
            # print (i)
            sample_weight = np.append(sample_weight, self.window(i))

        transformed_X = self.profit(self.data_set_X, self.data_set_Y)
        self.reg.fit(transformed_X.reshape(-1, 1),
                     self.data_set_Y, sample_weight=sample_weight)

    def profit(self, ul, uf):
        # ul = ul[:, 1]
        return (2-ul+0.3*uf) * (ul - 1)

    def reverse_profit(self, p, ul):
        if ul == 1:
            ul = 1+random.random()*0.1
        return (10*(ul**2 - 3*ul + p + 2)) / (3 * (ul - 1))

    def window(self, date):
        res = minimize_scalar(lambda weight: self.window_o(weight,date))
        # print(res.x)
        return res.x

    def window_o(self, weight, date):
        window_size = 10
        if date < 10:
            window_size = date
        weights = np.ones(1)
        weights = np.append(weights, weight)
        sum = 0
        for i in range (0, window_size):
            follower_in_window = np.array([self.data_set_Y[np.size(self.data_set_Y)-window_size-i]])
            follower_in_window = np.insert(follower_in_window, 0, 1)
            r = np.matmul(follower_in_window, weights)
            part1 = self.data_set_X[np.size(self.data_set_X)-window_size-i] - r
            sum += part1**2
        return sum

if __name__ == '__main__':
    # Make sure you set this to your group number!
    SimpleLeader('18')
