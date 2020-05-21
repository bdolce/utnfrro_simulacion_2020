
x = 1.00

class Generator:
    

    def lcg(self, m, a, c):
        global x

        xf = (a * x + c) % m
        x = xf 

        return xf/m


rng = Generator()

obs = []

for i in range(10):
    a = rng.lcg(m=2**32, a=1103515245, c=12345)
    obs.append(a)

print(obs)




# def rng(m=2**32, a=1103515245, c=12345):
#     rng.current = (a*rng.current + c) % m
#     return rng.current/m

# # setting the seed
# rng.current = 1
# obs = []

# for i in range(10):
#     obs.append(rng())

# print(obs)
