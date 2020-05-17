from net.NetParser import NetParser
import BruteForceAlgorithm

NET_FILE_NAME = "input_files/net4.txt"

if __name__ == "__main__":
    net_parser = NetParser()
    net = net_parser.parse_file(NET_FILE_NAME)


    demand1 = net.get_demand(1)

    #combinations = BruteForceAlgorithm.get_all_combinations_for_demand(demand1)
    solutions = BruteForceAlgorithm.get_solutions(net)
    print("hello")

