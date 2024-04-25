"""
A simple leader for the Stackelberg game.
"""
from base_leader import Leader
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error


class MK1SimpleLeader(Leader):
    data_set_X = np.array([])
    data_set_Y = np.array([])
    reg_poly = None
    reg_linear = None
    date = 100

    def __init__(self, name):
        self.reg_poly = PolynomialFeatures(degree=2)
        self.reg_linear = LinearRegression()
        self.data_set_X = np.array([])
        self.data_set_Y = np.array([])
        super().__init__(name)

    def new_price(self, date: int) -> float:
        self.log(date)
        self.update_model(date)

        # Fit linear regression
        self.reg_linear.fit(self.data_set_X.reshape(-1, 1), self.data_set_Y)
        pred_linear = self.reg_linear.predict(self.data_set_X[-1].reshape(-1, 1))
        error_linear = mean_squared_error(self.data_set_Y, self.reg_linear.predict(self.data_set_X.reshape(-1, 1)))

        # Transform features for polynomial regression
        transformed_X_poly = self.reg_poly.fit_transform(self.data_set_X.reshape(-1, 1))
        
        # Fit polynomial regression
        self.reg_linear.fit(transformed_X_poly, self.data_set_Y)
        pred_poly = self.reg_linear.predict(transformed_X_poly[-1].reshape(1, -1))
        error_poly = mean_squared_error(self.data_set_Y, self.reg_linear.predict(transformed_X_poly))

        if error_poly < error_linear:
            return float(pred_poly)
        
        return float(pred_linear)


    def start_simulation(self):
        self.log("Start of simulation")

        leader_prices = []
        follower_prices = []
        for i in range(1, 101):
            leader, follower = self.get_price_from_date(i)
            leader_prices.append(leader)
            follower_prices.append(follower)

        self.data_set_X = np.array(leader_prices)
        self.data_set_Y = np.array(follower_prices)

        changed_X = self.profit(self.data_set_X, self.data_set_Y)
        
        # Transform features for polynomial regression
        transformed_X_poly = self.reg_poly.fit_transform(changed_X.reshape(-1, 1))

        # Fit polynomial regression
        self.reg_linear.fit(transformed_X_poly, self.data_set_Y)

    def end_simulation(self):
        """
        A function run at the end of the simulation.
        """
        self.log("End of simulation")

    def update_model(self, date):
        yesterday = date - 1
        yesterday_prices = self.get_price_from_date(yesterday)
        self.data_set_X = np.append(self.data_set_X, yesterday_prices[0])
        self.data_set_Y = np.append(self.data_set_Y, yesterday_prices[1])

    def profit(self, ul, uf):
        return (2 - ul + 0.3 * uf) * (ul - 1)


if __name__ == '__main__':
    # Make sure you set this to your group number!
    MK1SimpleLeader('12')
