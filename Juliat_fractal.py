# -*- coding: utf-8 -*-
from PIL import Image
import os
import multiprocessing
from multiprocessing import Process, Lock
import threading
import shutil

if(os.cpu_count() is not None):
    CPU_COUNT = os.cpu_count()
else:
    CPU_COUNT = 1

#shutil.rmtree('<путь к папке>')

def parameters(file_path: str = r'C:\Users\Computer_G\PycharmProjects\Juliat\f_parameters.txt'):

    params = []

    with open(file_path, mode='r', encoding='utf-8') as f:

        params = list(par for par in f.readlines())

    # Формат возврата: [(cX, cY),(cX, cY),(cX, cY)]
    return list(tuple(float(it) for it in par.rstrip('\n').split(', ')) for par in params)

def fractal_builder(start_points, l):

    for point in start_points:

        cX = point[0]
        cY = point[1]

        w, h, zoom = 1920, 1080, 1

        bitmap = Image.new('RGB', (w, h), 'white')
        pix = bitmap.load()

        moveX, moveY = 0.0, 0.0
        maxIter = 255

        for x in range(w):

            for y in range(h):
                zx = 1.5 * (x - w / 2) / (0.5 * zoom * w) + moveX
                zy = 1.0 * (y - h / 2) / (0.5 * zoom * h) + moveY
                i = maxIter

                while zx * zx + zy * zy < 4 and i > 1:
                    tmp = zx * zx - zy * zy + cX
                    zy, zx = 2.0 * zx * zy + cY, tmp
                    i -= 1

                # RGB
                pix[x, y] = (i << 21) + (i << 10) + i * 8

        # bitmap.show()
        file_name = str(cX) + '_' + str(cY)
        bitmap.save(fr'C:\Users\Computer_G\PycharmProjects\Juliat\fractals_juliat\{file_name}.bmp')

        l.acquire()

        try:
            print(f'{file_name} построен.')
        finally:
            l.release()

if __name__ == '__main__':

    lock = Lock()

    params = parameters()

    #Создать задачи для процессов Python [[(),(),()], [(),()], [()]]
    py_proc = []
    for i in range(CPU_COUNT): py_proc.append([])

    for i in range(len(params)):
        py_proc[i%len(py_proc)].append(params[i])

    for job in py_proc:

        proc_ = []

        for i in range(len(params)):
            proc_.append(multiprocessing.Process(target=fractal_builder, args=(job, lock, )))

        [p.start() for p in proc_]
        [p.join() for p in proc_]