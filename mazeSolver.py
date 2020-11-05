from PIL import Image

class Pixel:
    black = (0,0,0,255)
    white = (255,255,255,255)
    pixels = []
    def __init__(self, position, image, index,is_maze=False):
        self.position = position
        self.image = image
        self.index = index
        self.color = image.getpixel(position)
        Pixel.pixels.append(self)
        if is_maze:
            if position not in Maze.Maze_pixels_positions:
                Maze.Maze_pixels_positions.append(position)
    @staticmethod
    def get_pixel(x,y):
        for pixel in Pixel.pixels:
            if pixel.position[1] == x and pixel.position[0] == y:
                return pixel
        return None


class Maze:
    Maze_pixels_positions = []
    Maze_pixels = []
    Maze_path = []

    @staticmethod
    def Check_Path(pixel, index=0):
        print(pixel.position, index)
        image = pixel.image
        x,y = image.size
        up = (pixel.position[0], pixel.position[1] - 1)
        down = (pixel.position[0], pixel.position[1] + 1)
        left = (pixel.position[0] - 1, pixel.position[1])
        right = (pixel.position[0] + 1, pixel.position[1])
        summed = False

        for move in [up, down, left, right]:
            if move[0] >= x or move[1] >= y or move[0] < -1 or move[1] < -1:
                continue

            if pixel.image.getpixel(move) == Pixel.white:
                if move in Maze.Maze_pixels_positions: #and move.index > pixel.index
                    #if Pixel.get_pixel(move[0],move[1]) == None:
                    #    continue
                    #if Pixel.get_pixel(move[0],move[1]).index > pixel.index:
                        continue
                if not summed:
                    index = index + 1
                    summed = True
                pix = Pixel(move, image, index, True)
                Maze.Maze_pixels.append(pix)
                Maze.Check_Path(pix, index)

    @staticmethod
    def Find_Start():
        for start in Maze.Maze_pixels:
            if start.position[1] == 0:
                return start

    @staticmethod
    def Find_End(image):
        x, y = image.size

        for pix_x in range(0, x):
            position = (pix_x, y - 1)
            target_pix = Pixel(position, image, 0)
            if target_pix.color == Pixel.white:
                Maze.Maze_pixels.append(target_pix)
                Maze.Maze_pixels_positions.append(target_pix.position)
                return target_pix

    @staticmethod
    def Get_Path(pixel):
        possible_pos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        surrounding_pixels = []
        surrounding_pixels_index = []
        Maze.Maze_path.append(pixel)

        for pix in Maze.Maze_pixels:
            if pix.index >= pixel.index:
                continue
            #if  pix.index - pixel.index = -1
            if (pix.position[0] - pixel.position[0], pix.position[1] - pixel.position[1]) in possible_pos:
                surrounding_pixels.append(pix)
                surrounding_pixels_index.append(pix.index)
                #Maze.Get_Path
                #return
        if len(surrounding_pixels) > 1:
            min_index = min(surrounding_pixels_index)
            for pix in surrounding_pixels:
                if pix.index == min_index:
                    Maze.Get_Path(pix)
                    return
        elif len(surrounding_pixels) == 1:
            Maze.Get_Path(surrounding_pixels[0])

    @staticmethod
    def Color_Maze(image):
        for pixel in Maze.Maze_path:
            image.putpixel(pixel.position, (255, 0, 0, 255))
        image.save("solved_maze.png")

    @staticmethod
    def Solve(image_name):
        # gets the image
        image = Image.open(image_name)
        # gets the end pixel
        end_pixel = Maze.Find_End(image)
        # indexes maze by whats closer to the end
        Maze.Check_Path(end_pixel)
        # gets the start pixel
        start_pixel = Maze.Find_Start()
        # gets the path pixel in array
        Maze.Get_Path(start_pixel)
        #fill maze path with red color
        Maze.Color_Maze(image)


Maze.Solve("maze.png")