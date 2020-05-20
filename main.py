from net.NetParser import NetParser
from algorithms import BruteForceAlgorithm

NET_FILE_NAME = "input_files/net4.txt"

if __name__ == "__main__":
    net_parser = NetParser()
    net = net_parser.parse_file(NET_FILE_NAME)

    solutions = BruteForceAlgorithm.compute(net, problem="DDAP")
