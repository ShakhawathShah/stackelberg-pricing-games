# stackelberg-pricing-games

Stackelberg pricing games

# Random Profit

- MK1: 17.5863496878102
- MK2: 18.2783504129443
- MK3: 12.1200475408081

# Base Profits (simple_leader.py)

- MK1: 17.5952557888825
- MK2: 18.4993660039686
- MK3: 12.2606605197795

# Our Best Profits

- MK1: 17.6308351938507

  - File: simple_leader_MK1.py
  - Method: Linear + Window + Nelder-Mead Optimisation + Regularisation
  - Parameters: window=11, x0=1.4, alpha=0.01

- MK2: 18.5801916811233

  - File: simple_leader_MK2.py
  - Method: HuberRegressor + Window + Nelder-Mead Optimisation
  - Parameters: epsilon=1, window=15, x0=1.41

- MK3: 12.268894324174

  - File: simple_leader_MK3.py
  - Method: Linear + Window + Bounded Optimisation + Regularisation
  - Parameters: window=8,

# Other Group Profit

- MK1: 17.6257822150468
- MK2: 18.5928142778606
- MK3: 12.2688225571899

# Other Test File Profits

- MK1: 17.6274169867196
  - File: simple_leader_MK1_atif.py
  - Method: Polynomial + Nelder-Mead Optimisation + Regularisation
  - Parameters: x0=1.4, alpha=0.01
