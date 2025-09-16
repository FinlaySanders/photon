import client.photon_client as photon
import random
from itertools import product

photon.init()

for epoch in range(10):
    loss = random.random()
    photon.log(step=epoch, loss=loss, accuracy=1-loss)