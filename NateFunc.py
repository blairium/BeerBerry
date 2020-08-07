
import pickle

def binary_write(data):
    pickled_out = open("bin1", "wb")
    pickle.dump(data, pickled_out)
    pickling().close()


def binary_read():
    pickled_in = open("bin1", "rb")
    data = pickle.load(pickled_in)
    print("PICKLE SUCCESS")






