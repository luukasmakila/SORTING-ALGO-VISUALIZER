import pygame, random, math
pygame.init()

#colors
black = 0,0,0
blue = 30,144,255
red = 255,0,0
bg_color = black
pinks = [(255,192,203), (255,20,147), (255,105,180)]

#side padding sizes
side_pad = 100
top_pad = 150

#determines the size of the screen
width = 800
height = 600

#number of blocks and their heights
n = 100
min_val = 1
max_val = 100

#calculates the height and the width of the blocks on screen
block_width = round((width - side_pad) / n)
block_height = math.floor((height - top_pad) / (max_val - min_val))
start_x = side_pad // 2 #determines where we start drawing blocks 

font = pygame.font.SysFont('comicsans', 30)
window = pygame.display.set_mode((width, height))

def generate_list(n, min_val, max_val):
    lst = []
    for i in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def draw(algo_name, lst):
    window.fill(bg_color)
    title = font.render(f"{algo_name}", 1, blue)
    window.blit(title, (width/2 - title.get_width()/2 , 5))

    controls = font.render("R - Reset List | SPACE - Start Sorting", 1, pinks[0])
    window.blit(controls, (width/2 - controls.get_width()/2 , 45))

    sorting = font.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | Z - Shell Sort", 1, pinks[0])
    window.blit(sorting, (width/2 - sorting.get_width()/2 , 75))

    draw_list(lst)
    pygame.display.update()

def draw_list(lst, colors={}, clear_bg=False):
    if clear_bg:
        clear_rect = (side_pad//2, top_pad, 
                        width - side_pad, height - side_pad)
        pygame.draw.rect(window, bg_color, clear_rect)
    
    for i, val in enumerate(lst):
        x = start_x + i * block_width
        y = height - (val - min_val) * block_height

        color = pinks[i % 3] #how we get the neighbouring blocks to be different shades from one another

        if i in colors:
            color = colors[i]
        pygame.draw.rect(window, color, (x, y, block_width, height))

    if clear_bg:
        pygame.display.update()

def bubble_sort(lst):
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if num1 > num2:
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(lst, {j: blue, j+1: red}, True)
                yield True
    return lst

def insertion_sort(lst):
    for i in range(1, len(lst)):
        curr = lst[i]
        while True:
            asc = i > 0 and lst[i-1] > curr
            if not asc:
                break
            lst[i] = lst[i-1]
            i = i-1
            lst[i] = curr
            draw_list(lst, {i-1: blue, i: red}, True)
            yield True
    return lst

def selection_sort(lst):
    for i in range(len(lst)):
        min_idx = i
        for j in range(i+1, len(lst)):
            if lst[min_idx] > lst[j]:
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(lst, {min_idx: red, i: blue}, True)
        yield True
    return lst

def shell_sort(lst):
    gap = math.floor(n/2)
    while gap > 0:
        for i in range(gap, n):
            temp = lst[i]
            j = i
            while j >= gap and lst[j-gap] > temp:
                lst[j] = lst[j-gap]
                j -= gap
            lst[j] = temp
            draw_list(lst, {lst[i]: red, lst[j]: blue}, True)
            yield True
        gap = math.floor(gap/2)
    return lst

def main():
    run = True

    clock = pygame.time.Clock()

    lst = generate_list(n, min_val, max_val)

    sorting = False

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None #stores the generator object when sorting

    while run:
        clock.tick(60)
        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw(sorting_algo_name, lst)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_list(n, min_val, max_val)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algo_generator = sorting_algo(lst)
            elif event.key == pygame.K_b:
                sorting_algo = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_i:
                sorting_algo = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_s:
                sorting_algo = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_z:
                sorting_algo = shell_sort
                sorting_algo_name = "Shell Sort"

    pygame.quit()

if __name__ == "__main__":
    main()