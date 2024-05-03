import numpy as np
from scipy.optimize import minimize_scalar, minimize
from base_leader import Leader
from sklearn.linear_model import Ridge



__author__ = "Rokas"

class SimpleLeaderMK1(Leader):

    def __init__(self, name):
        self.data_size = 100
        self.model_weight = np.array([])
        self.leader_data = np.array([])
        self.follower_data = np.array([])
        alpha = 0.01
        self.reg = Ridge(alpha=alpha)
        # If you want to initialize something here, do it before the super() call.
        super().__init__(name)


    def load_historical_data(self):
        self.leader_data = np.array([self.get_price_from_date(i)[0] for i in range(1, 101)])
        self.follower_data = np.array([self.get_price_from_date(i)[1] for i in range(1, 101)])

    def start_simulation(self):
        """
        A function run at the beginning of the simulation.
        """
        self.log("Start of simulation")

        self.load_historical_data()

        # Fit Ridge regression model with regularization
        self.reg.fit(self.profit(self.leader_data, self.follower_data).reshape(-1, 1), self.follower_data)

    def end_simulation(self):
        """
        A function run at the end of the simulation.
        """
        self.log("End of simulation")

    def profit(self, ul, uf):
        return (2-ul+0.3*uf) * (ul - 1)

    def update_prediction(self, date):
        previous_data = self.get_price_from_date(date - 1)
        previous_leader_data = previous_data[0]
        previous_follower_data = previous_data[1]

        self.leader_data = np.append(self.leader_data, previous_leader_data)
        self.follower_data = np.append(self.follower_data, previous_follower_data)

        sample_weight = np.array([self.window(i) for i in range(1, date+1)])

        self.reg.fit(self.profit(self.leader_data, self.follower_data).reshape(-1, 1), self.follower_data, sample_weight=sample_weight)

    def window(self, date):
        res = minimize_scalar(lambda weight: self.window_o(weight,date))
        return res.x

    def window_o(self, weight, date):
        window_size = 11
        if date < 11:
            window_size = date
        weights = np.array([1, weight])
        sum = 0
        for i in range (window_size):
            follower_in_window = np.array([self.follower_data[len(self.follower_data) - window_size - i]])
            follower_in_window = np.insert(follower_in_window, 0, 1)
            part1 = self.leader_data[np.size(self.leader_data)-window_size-i] - (np.matmul(follower_in_window, weights))
            sum += part1**2
        return sum

    def new_price(self, date: int) -> float:
        """
        A function for setting the new price of each day.

        :param date: date of the day to be updated
        :return: (float) price for the day
        """
        self.log(date)

        self.update_prediction(date)

        # Fit Ridge regression model with regularization
        self.reg.fit(self.profit(self.leader_data, self.follower_data).reshape(-1, 1), self.follower_data)

        A = self.reg.coef_[0]
        B = self.reg.intercept_

        def profit_ul(x):
            part1 = (-A*x**2)+(3*A*x)-(2*A)+B
            part2 = 1 - 0.3*A*x + 0.3*A
            part3 = part1/part2
            part4 = 2 - x + 0.3 * part3
            return ((x - 1) * part4)
        
        # Define the profit function to be minimized
        def neg_profit(x):
            return -profit_ul(x)

        # Use Nelder-Mead method for optimization
        result = minimize(neg_profit, x0=1.4, method='Nelder-Mead', bounds=[(1, 2)])

        price = result.x[0]

        self.date = date

        return float(price)


if __name__ == '__main__':
    # Make sure you set this to your group number!
    SimpleLeaderMK1('12')