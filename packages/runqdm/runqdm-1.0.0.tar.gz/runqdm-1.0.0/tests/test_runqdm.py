from runqdm import runqdm
import time

for i in runqdm(range(100)):
    sum(x ** 2 for x in range(1, 10**7))  


# print('done')
