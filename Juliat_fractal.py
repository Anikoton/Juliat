from PIL import Image

def parameters(file_path: str = r'C:\Users\Nikolayev_AA_\PycharmProjects\Juliat\venv\f_parameters.txt'):

    params = []

    with open(file_path, mode='r', encoding='utf-8') as f:

        params = list(par for par in f.readlines())

    # Формат возврата: [(cX, cY),(cX, cY),(cX, cY)]
    return list(tuple(float(it) for it in par.rstrip('\n').split(', ')) for par in params)

if __name__ == '__main__':

    for par in parameters():

        cX = par[0]
        cY = par[1]

        #width, height, zoom
        #w, h, zoom = 7680, 4320, 1
        #w, h, zoom = 1920, 1080, 1
        w, h, zoom = 1920, 1080, 1
        #w, h, zoom = 640, 480, 1

        bitmap = Image.new('RGB', (w, h), 'white')

        pix = bitmap.load()

        #cX, cY = -0.7, 0.26465
        #cX, cY = -0.7, 0.31057
        #cX, cY = -0.7, 0.27015
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

                # convert byte to RGB (3 bytes)
                pix[x, y] = (i << 21) + (i << 10) + i * 8

        #bitmap.show()
        file_name = str(cX) + '_' + str(cY)
        bitmap.save(f'C:\\Users\\Nikolayev_AA_\\PycharmProjects\\Juliat\\venv\\fractals_juliat\\{file_name}.bmp')
        print(f'{file_name} построен.')