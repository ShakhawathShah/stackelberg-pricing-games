from abc import abstractmethod
import rpyc
import sys
from rpyc.utils.server import ThreadedServer


class Leader(rpyc.Service):
    def __init__(self, name):
        self.conn = None
        self.name = name
        if len(sys.argv) > 1:
            self.server = ThreadedServer(self, port=sys.argv[1])
        else:
            self.server = ThreadedServer(self, port=18812)
        self.server.start()

    def exposed_new_price(self, date):
        """

        :param date: (int) date of the current day
        :return: price to send on this day
        """
        return self.new_price(date)

    # sends the new price whenever
    @abstractmethod
    def new_price(self, date):
        pass

    def get_price_from_date(self, date: int) -> (float, float):
        """

        :param date: (int) date to get the price from
        :return: a tuple (leader_price, follower_price)
        """
        return self.conn.root.get_price(date)

    def on_connect(self, conn):
        self.conn = conn

    def log(self, text):
        self.conn.root.log(text)

    def exposed_start_simulation(self):
        return self.start_simulation()

    def exposed_end_simulation(self):
        return self.end_simulation()

    def start_simulation(self):
        print("Nothing implemented!")

    def end_simulation(self):
        print("Nothing implemented!")

    def exposed_get_name(self):
        return self.name
