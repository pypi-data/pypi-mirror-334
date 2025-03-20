
import timeit
from random import randint
from devjoni.hosguibase.imagefuncs import rgb2hex

dim = 1080

def main():
    global image
    image = []
    for i_row in range(dim):
        row = [(randint(0, 255),randint(0, 255),
                randint(0, 255)) for i in range(dim)]
        image.append(row)
    
    print('Parallel 2')
    print(timeit.timeit('rgb2hex(image, N_jobs=2)', globals=globals(), number=10)/10)

    print('Parallel 1')
    print(timeit.timeit('rgb2hex(image, N_jobs=0)', globals=globals(), number=10)/10)
if __name__ == "__main__":
    main()
