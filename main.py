from net.NetParser import NetParser

NET_FILE_NAME = "input_files/net12_1.txt"

if __name__ == "__main__":
    net_parser = NetParser()
    net = net_parser.parse_file(NET_FILE_NAME)
