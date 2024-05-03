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

- MK2: 18.5801940140926

  - Window 12 18.5801940112758
  - Window 13 18.5801932489796
  - Window 15 18.5801916811233
  - Window 17 18.5801902489796

  - File: simple_leader_MK2.py
  - Method: HuberRegressor + Window + Nelder-Mead Optimisation
  - Parameters: epsilon=1, window=15, x0=1.413

- MK3: 12.269651221109

  - Window 7: 12.2688237804767
  - Window 9: 12.2688237804767
  - Window 8: 12.268894324174
  - Window 10: 12.2695201179103
  - Window 11: 12.2692680826705
  - Window 15: 12.269651221109
  - Window 20: 12.2692346528657

  - Huber: 11.8196864450257
  - Ridge: 12.269651221109
  - Linear: 12.2636605197795

  - Bounded: 12.269651221109
  - Nelder-mead: 12.0984153451731
  - Powell: 12.2692359877081

  - File: simple_leader_MK3.py
  - Method: Linear + Window + Bounded Optimisation + Regularisation
  - Parameters: window=15,

# Other Group Profit

- MK1: 17.6257822150468
- MK2: 18.5928142778606
- MK3: 12.2688225571899

# Other Test File Profits

- MK1: 17.6274169867196
  - File: simple_leader_MK1_atif.py
  - Method: Polynomial + Nelder-Mead Optimisation + Regularisation
  - Parameters: x0=1.4, alpha=0.01
