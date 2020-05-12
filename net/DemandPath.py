class DemandPath:

    def __init__(self, data):
        self.path_id = data[0]
        self.links = data[1:]  # list of link ids that construct this path
