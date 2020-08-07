
import pickle

def binary_write(data):
    pickled_out = open("bin1", "wb")
    pickle.dump(data, pickled_out)
    pickled_out.close()


def binary_read(fileName):
    pickled_in = open("bin1", "rb")
    data = pickle.load(pickled_in)
    print("PICKLE SUCCESS")
    return data





