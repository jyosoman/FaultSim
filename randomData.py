import random
def randInt():
   rnum= random.uniform(0,1)
   return rnum*(2<<32)
for i in range(1000000):
    print long(randInt()),long(randInt())
