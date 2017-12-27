from fundManager import *
from dataManager import *
from dataWrangler import *
from dataAnalyst import *
from time import sleep
import spade

def initialize():
	"""Create agents and start running MAS"""

	agents = [
		DataWrangler("data_wrangler@127.0.0.1", "secret"),
		DataManager("data_manager@127.0.0.1", "secret"),
		NnDataAnalyst("data_analyst_nn@127.0.0.1", "secret"),
		SvrDataAnalyst("data_analyst_svr@127.0.0.1", "secret"),
		FundManager("fund_manager@127.0.0.1", "secret")
	]
	map(lambda x:x.start(), agents)

if __name__ == "__main__":
	initialize()
