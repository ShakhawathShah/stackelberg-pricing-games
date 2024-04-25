This is an application for playing the Stackelberg game for COMP34612.
This file explains how to use it.

First of all, there are dependencies you must install. All of them are installable via pip:
    * tk=8.6.12
    * tk-tools=0.14.0
    * rpyc=5.1.0
    * openpyxl=3.0.9
    * tksheet=5.4.1
    * numpy=1.22.3
These may also be downloaded alongside the game if you prefer that. The game uses Python 3.9.10 and can be ran either on Linux or Windows. You might also need Tkinter. It is provided with most Python installs, but if that is not the case for your installation,
you must check how to install it for your specific OS.


The game platform is separate from the leader program. While the game platform code is not for you to use,
there is a base leader class in base_leader.py which has the functionalities you might require (and you should not
change this file), as well as simple_leader.py, which shows a basic
implementation of a leader, which chooses its price at random.

The game platform connects with the leader platform as such:
    * You can run either program first, and they are ran as simple python programs (python main.py,
    python simple_leader.py etc.). If you launch the leader and then the platform, it should connect
    automatically (as indicated by the green "Connected" text). If you run the platform first, it will show
    "Disconnected" in red. You must then launch the leader program and press the "Connect" button, which should
    then connect in the same way as before.
    * The programs communicate over a port. The default port is 18812. If this is unavailable or you want to
    use a different one, you must provide it as an argument to both programs.

There are several things concerning leaders:
    * Your leader should implement the base class Leader from base_leader.py. DO NOT change the base class, as your
    changes will not be used when running the code.
    * Your leader MUST have a function called new_price(), which takes a date as an integer and returns a float,
    which is the leader's price for that particular date. This is the only function you MUST implement.
    * Your leader has a name. It is defined during initialization as such: SimpleLeader('0'). You MUST set this
    to the number of your group.
    * If you want to initialize anything when the leader is created, you should do that before the super() call in
    the init (which MUST be kept in the init). This is because the super starts a server for
    communication with the game platform, and no other code (from the leader's side) is executed after that.
    * The leader has a few methods:
        ** get_price_from_date(date): this is likely the most important method for you. It returns the prices as a tuple
        (leader_price, follower_price) on a particular date. Note that you can use it mid-run i.e. if you started
        on day 100, you can get the prices on 105 if you have passed that day already. It will raise an error
        if you either try to get a date <1 or a date that has not happened yet.
        ** start_simulation(): this is called at the beginning of each 30-day run. You can do any sort of
        initialization you want here.
        ** end_simulation(): this is called after all of the days are done. You can gather data or clean up here.
        ** log(text): this prints out the text into the log in the GUI of the game platform.
    * You are free to write any other methods as you see fit.

The game is ran by setting the follower you want to play against, the
date you want to start at and how many days you want to run for. After the game is
run, you can extract both the 30-day performance (Export Data) and the log (Export Log). You can set the data to be
exported automatically (Auto Exp.) and you can clear the log (Clear Log).