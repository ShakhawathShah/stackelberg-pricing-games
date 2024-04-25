import numpy as np
import random
from scipy.optimize import minimize_scalar
from sklearn.ensemble import RandomForestRegressor
from base_leader import Leader

class SimpleLeader(Leader):
    def __init__(self, name):
        self.data_size = 100
        self.model_weight = np.array([])
        self.leader_data = np.array([])
        self.follower_data = np.array([])
        self.reg = RandomForestRegressor()  # Using RandomForestRegressor instead of LinearRegression
        super().__init__(name)

    def load_historical_data(self):
        self.leader_data = np.array([self.get_price_from_date(i)[0] for i in range(1, 101)])
        self.follower_data = np.array([self.get_price_from_date(i)[1] for i in range(1, 101)])

    def start_simulation(self):
        self.log("Start of simulation")
        self.load_historical_data()
        self.reg.fit(self.profit(self.leader_data, self.follower_data).reshape(-1, 1), self.follower_data)

    def end_simulation(self):
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
        window_size = 10
        if date < 10:
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
        self.log(date)
        self.update_prediction(date)
        A = self.reg.estimators_[0].feature_importances_[0]  # Extracting feature importance from one of the trees
        B = np.mean(self.reg.estimators_[0].predict([0]))  # Using the mean prediction as intercept
        def profit_ul(x):
            part1 = (-A*x**2)+(3*A*x)-(2*A)+B
            part2 = 1 - 0.3*A*x + 0.3*A
            part3 = part1/part2
            part4 = 2 - x + 0.3 * part3
            return ((x - 1) * part4)
        price = minimize_scalar(lambda x: -profit_ul(x), method="Bounded", bounds=(1, 2)).x
        self.date = date
        return float(price)

if __name__ == '__main__':
    SimpleLeader('12')
