
import timeit
from random import randint
from devjoni.hosguibase.imagefuncs import hex2rgb

dim = 1080

def main():
    global image
    image = []
    for i_row in range(dim):
        a = randint(0,255) 
        b = randint(0,255)
        c = randint(0,255)
        row = [f'#{a:02x}{b:02x}{c:02x}' for i in range(dim)]
        image.append(row)
    
    print('Parallel 2')
    print(timeit.timeit('hex2rgb(image, N_jobs=2)', globals=globals(), number=10)/10)

    print('Parallel 0')
    print(timeit.timeit('hex2rgb(image, N_jobs=0)', globals=globals(), number=10)/10)
if __name__ == "__main__":
    main()
