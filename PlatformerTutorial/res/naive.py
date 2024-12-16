from PIL import Image, ImageDraw
import random

# 1. Tạo ảnh mới với kích thước ngẫu nhiên và màu nền cụ thể
def create_background():
    # Chọn ngẫu nhiên chiều rộng w trong khoảng [50, 100]
    # w = random.randint(40, 100)
    w = 60
    h = 14

    # Tạo một ảnh mới với kích thước w x h và màu nền cho sẵn
    img = Image.new(mode="RGB", size=(w, h), color=background_color)
    return img

def draw_water(img):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    water_height = random.randint(1, 3)

    
    # Vẽ hình chữ nhật
    draw.rectangle([0, 14-water_height, w, 14], fill=water_color)
    return img

# 2. Vẽ một hình chữ nhật ngẫu nhiên trên ảnh
def draw_platform_above(img, top_left_x, bottom_right_x):
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # Định nghĩa kích thước hình chữ nhật
    # Chiều rộng hình chữ nhật được chọn ngẫu nhiên
    rect_width = random.randint(3, w//2)  # Đảm bảo hình chữ nhật không quá rộng

    # Chiều cao hình chữ nhật được chọn ngẫu nhiên từ 1 đến h
    rect_height = random.randint(0, h//3-1)  # Ít nhất bao phủ dòng y=0

    # Chọn vị trí ngẫu nhiên cho góc trên bên trái của hình chữ nhật
    # Vì phải bao phủ y=0, nên top_left_y = 0
    
    # top_left_x = random.randint(0, max(w - rect_width, 0))
    top_left_y = 0  # Bao phủ dòng y=0
    # bottom_right_x = top_left_x + rect_width
    bottom_right_y = top_left_y + rect_height
    
    # Đảm bảo hình chữ nhật không vượt ra ngoài ảnh
    bottom_right_x = min(bottom_right_x, w)
    bottom_right_y = min(bottom_right_y, h)

    # Vẽ hình chữ nhật    
    draw.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y], fill = floor_color)
    draw.rectangle([top_left_x, bottom_right_y, bottom_right_x, bottom_right_y], fill = stone_color)
    island_above_y.append(bottom_right_y)
    return img

def draw_platform_below(img, top_left_x, bottom_right_x):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # Định nghĩa kích thước hình chữ nhật
    rect_width = random.randint(3, w//2)  # Đảm bảo hình chữ nhật không quá rộng
    rect_height = random.randint(3, h//2-2)  # Chiều cao hình chữ nhật tối đa bằng nửa chiều cao ảnh

    # Chọn vị trí ngẫu nhiên cho góc trên bên trái của hình chữ nhật
    
    # top_left_x = random.randint(0, max(w - rect_width, 0))
    top_left_y = h - rect_height  # Bao phủ dòng y=13
    # bottom_right_x = top_left_x + rect_width
    bottom_right_y = top_left_y + rect_height
    
    # Đảm bảo hình chữ nhật không vượt ra ngoài ảnh
    bottom_right_x = min(bottom_right_x, w)
    bottom_right_y = min(bottom_right_y, h)

    # Vẽ hình chữ nhật
    draw.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y], fill=floor_color)
    draw.rectangle([top_left_x, top_left_y, bottom_right_x, top_left_y], fill=grass_color)
    
    draw.rectangle([top_left_x, top_left_y, top_left_x, bottom_right_y], fill = left_edge_color)
    draw.rectangle([bottom_right_x, top_left_y, bottom_right_x, bottom_right_y], fill = right_edge_color)
    
    draw.rectangle([top_left_x, top_left_y, top_left_x, top_left_y], fill = left_square_color)
    draw.rectangle([bottom_right_x, top_left_y, bottom_right_x, top_left_y], fill = right_square_color)
    island_below_x.append(top_left_x)
    island_below_y.append(top_left_y)
    return img

# 3. Lưu và hiển thị ảnh
def save_image(img, filename):
    path = r"C:\Users\baolo\Desktop\Lab AIOT\[Project DCGAN] Generative Image\generated_images\{}.png"
    img.save(r"C:\Users\baolo\Desktop\Lab AIOT\[Project DCGAN] Generative Image\generated_images\{}.png".format(filename))

def draw_platforms(img):
    w, h = img.size
    if 40 <= w < 60:
        split = w//2
    elif 60 <= w < 80:
        split = w//3
    else:
        split = w//4
    for x in range(5, w-5, split):
        img = draw_platform_above(img, x+random.randint(-4, 4), x+random.randint(split-7, split))
        img = draw_platform_below(img, x+random.randint(0, 3), x+random.randint(split-6, split))

def valid_pos(img, top_left_x, top_left_y, color):
    pixels = img.load()
    colors = []
    for dy in range(2):
        for dx in range(3):
            x = top_left_x + dx
            y = top_left_y + dy
            # Kiểm tra xem x, y có nằm trong phạm vi ảnh không
            if x < img.width and y < img.height:
                colors.append(pixels[x, y])
            else:
                colors.append(None)  # Nếu ngoài phạm vi, thêm None
    x, y = top_left_x, top_left_y
    if colors[0] == background_color and colors[1] == background_color and colors[2] == background_color\
        and colors[3] == grass_color and colors[4] == grass_color and colors[5] == grass_color:
            pixels[x, y] = color
            return True
    else:
        return False
    
def spawn_player(img):
    w, h = img.size
    bool_spawn_point = False
    for x in range(w):
        for y in range(h):
            bool_spawn_point = valid_pos(img, x, y, player_color)
            if (bool_spawn_point):
                break
        if (bool_spawn_point):
            break

def spawn_enemy(img):
    w, h = img.size
    for x in range(w):
        for y in range(h):
            chance = random.randint(0, 100)
            if chance <= 20:
                monster_type = random.randint(0, 100)
                if monster_type <= 30:
                    valid_pos(img, x, y, star_fish_color)
                elif 30 < monster_type <= 60:
                    valid_pos(img, x, y, shark_color)
                else:
                    valid_pos(img, x, y, crab_color)
            else:
                pass
            
def pos_furniture(img, top_left_x, top_left_y, color):
    pixels = img.load()
    colors = []
    
    for dy in range(2):
        for dx in range(2):
            x = top_left_x + dx
            y = top_left_y + dy
            # Kiểm tra xem x, y có nằm trong phạm vi ảnh không
            if x < img.width and y < img.height:
                colors.append(pixels[x, y])
            else:
                colors.append(None)  # Nếu ngoài phạm vi, thêm None
    
    x, y = top_left_x, top_left_y
    if colors[0] == background_color and colors[1] == background_color and colors[2] == grass_color\
        and colors[3] == grass_color:
            pixels[x, y] = color
            return True
    else:
        return False
    
def pos_stair(img, top_left_x, top_left_y):
    pixels = img.load()
    colors = []
    cnt = 0
    for dy in range(6):
        for dx in range(6):
            x = top_left_x + dx
            y = top_left_y + dy
            # Kiểm tra xem x, y có nằm trong phạm vi ảnh không
            if x < img.width and y < img.height:
                colors.append(pixels[x, y])
                if pixels[x, y] == background_color:
                    cnt += 1
            else:
                colors.append(None)  # Nếu ngoài phạm vi, thêm None
    
    x, y = top_left_x, top_left_y
    valid_height = False
    for i in range(3):
        if pixels[x+4+i, y] == grass_color or pixels[x+4+i, y+2] == grass_color:
            valid_height = True
            break
    
    if cnt == 36:
        chance = random.randint(0,100)
        length = random.randint(3,5)
        enemy_chance = random.randint(0,100)
        box_chance = random.randint(0,100)
        tree_chance = random.randint(0,100)
        t_pos = random.randint(1, length - 1)
        if 0 <= chance < 25:
            # 1
            pixels[x+1, y+4] = (39, 145, 154)
            pixels[x+3, y+2] = (39, 145, 154) 
            
            for i in range(length):
                pixels[x+5+i, y+1] = (37, 122, 154)
            pixels[x+5, y+1] = (36, 240, 154)
            pixels[x+5+length, y+1] = (38, 122, 154)
            
            if enemy_chance <= 30:
                chance = random.randint(0, 100)
                if chance <= 20:
                    monster_type = star_fish_color
                elif 20 < chance <= 60:
                    monster_type = shark_color
                else:
                    monster_type = crab_color
                pixels[x+5+t_pos, y] = monster_type
            if box_chance <= 30:
                pixels[x+5+t_pos+1, y] = box_color
            if tree_chance <= 30:
                pixels[x+5+t_pos-1, y] = tree_color
                
        elif 25 <= chance < 50:
            # 2
            pixels[x, y+4] = (36, 122, 154)
            pixels[x+1, y+4] = (38, 122, 154)
            
            pixels[x+2, y+2] = (36, 122, 154)
            pixels[x+3, y+2] = (38, 122, 154)
            
            for i in range(length):
                pixels[x+5+i, y+1] = (37, 122, 154)
                
            pixels[x+5, y+1] = (36, 240, 154)
            pixels[x+5+length, y+1] = (38, 122, 154)
            
            if enemy_chance <= 30:
                chance = random.randint(0, 100)
                if chance <= 20:
                    monster_type = star_fish_color
                elif 20 < chance <= 60:
                    monster_type = shark_color
                else:
                    monster_type = crab_color
                pixels[x+5+t_pos, y] = monster_type
            if box_chance <= 30:
                pixels[x+5+t_pos+1, y] = box_color
            if tree_chance <= 30:
                pixels[x+5+t_pos-1, y] = tree_color
               
        elif 50 <= chance < 75:
            # 2
            pixels[x+1, y+4] = (3, 122, 154)
            pixels[x+1, y+5] = (27, 122, 154)
            
            pixels[x+3, y+2] = (3, 122, 154)
            pixels[x+3, y+3] = (27, 122, 154)
            
            for i in range(length):
                pixels[x+5+i, y+1] = (37, 122, 154)
            pixels[x+5, y+1] = (36, 240, 154)
            pixels[x+5+length, y+1] = (38, 122, 154)
            
            if enemy_chance <= 30:
                chance = random.randint(0, 100)
                if chance <= 20:
                    monster_type = star_fish_color
                elif 20 < chance <= 60:
                    monster_type = shark_color
                else:
                    monster_type = crab_color
                pixels[x+5+t_pos, y] = monster_type
            if box_chance <= 30:
                pixels[x+5+t_pos+1, y] = box_color
            if tree_chance <= 30:
                pixels[x+5+t_pos-1, y] = tree_color
        else:
            # 3
            pixels[x, y+4] = (36, 122, 154)
            pixels[x+1, y+4] = (2, 122, 154)
            pixels[x+1, y+5] = (27, 122, 154)
            
            pixels[x+2, y+2] = (36, 122, 154)
            pixels[x+3, y+2] = (2, 122, 154)
            pixels[x+3, y+3] = (27, 122, 154)
            
            for i in range(length):
                pixels[x+5+i, y+1] = (37, 122, 154)
            pixels[x+5, y+1] = (36, 240, 154)
            pixels[x+5+length, y+1] = (38, 122, 154)
            
            if enemy_chance <= 30:
                chance = random.randint(0, 100)
                if chance <= 20:
                    monster_type = star_fish_color
                elif 20 < chance <= 60:
                    monster_type = shark_color
                else:
                    monster_type = crab_color
                pixels[x+5+t_pos, y] = monster_type
            if box_chance <= 30:
                pixels[x+5+t_pos+1, y] = box_color
            if tree_chance <= 30:
                pixels[x+5+t_pos-1, y] = tree_color

        return True
    else:
        return False


def pos_hole(img, top_left_x, top_left_y):
    pixels = img.load()
    positions = []
    others = []
    cnt = 0
    for dy in range(3):
        for dx in range(2):
            x = top_left_x + dx
            y = top_left_y + dy
            # Kiểm tra xem x, y có nằm trong phạm vi ảnh không
            if x < img.width and y < img.height:
                positions.append([x, y])
                if pixels[x, y] != background_color:
                    cnt += 1
            else:
                pass
    if cnt >= 4: 
        for each in (positions):
            pixels[each[0], each[1]] = background_color
        pixels[positions[-1][0], positions[-1][1]] = spike_color
        pixels[positions[-2][0], positions[-2][1]] = spike_color
        for t in range(3):
            if pixels[positions[-1][0]+1, positions[-1][1]-t] == floor_color:
                pixels[positions[-1][0]+1, positions[-1][1]-t] = left_edge_color
            if pixels[positions[-1][0]+1, positions[-1][1]-t] == grass_color:
                pixels[positions[-1][0]+1, positions[-1][1]-t] = left_square_color
            if pixels[positions[-1][0]-2, positions[-1][1]-t] == floor_color:
                pixels[positions[-1][0]-2, positions[-1][1]-t] = right_edge_color
            if pixels[positions[-1][0]-2, positions[-1][1]-t] == grass_color:
                pixels[positions[-1][0]-2, positions[-1][1]-t] = right_square_color
        return True
    else:
        return False

def spawn_hole(img):
    w, h = img.size
    for x in range(10,w-5,2):
        if x+1 not in island_below_x and x+2 not in island_below_x and x+3 not in island_below_x:
            chance = random.randint(0, 100)
            for y in range(3, h-4):
                
                if chance <= 10:
                    pos_hole(img, x, y)
                else:
                    pass

def spawn_tree(img):
    w, h = img.size
    for x in range(w):
        for y in range(h):
            chance = random.randint(0, 100)
            if chance <= 20:
                pos_furniture(img, x, y, tree_color)
            else:
                pass

def spawn_box_and_canon(img):
    w, h = img.size
    for x in range(w):
        for y in range(h):
            chance = random.randint(0, 100)
            if chance <= 15:
                if chance <= 3:
                    if chance % 2 == 0:
                        pos_furniture(img, x, y, left_canon)
                    else:
                        pos_furniture(img, x, y, right_canon)
                else:
                    pos_furniture(img, x, y, box_color)
            else:
                pass

def spawn_stair(img):
    w, h = img.size
    for x in range(min(island_below_x) + 5,w-10):
        for y in range(max(island_above_y)+2, min(island_below_y)+1):
            chance = random.randint(0, 100)
            if chance <= 20:
                
                pos_stair(img, x, y)
            else:
                pass



background_color = (11, 234, 154)
floor_color = (13, 13, 90)
player_color = (11, 100, 154)
crab_color = (11, 0, 154)
star_fish_color = (11, 1, 154)
shark_color = (11, 2, 154)
tree_color = (11, 234, 7)
grass_color = (1, 50, 81)
stone_color = (25, 13, 29)
water_color = (48, 50, 81)
box_color = (11, 234, 3)
left_edge_color = (12, 137, 142)
right_edge_color = (14, 137, 142)
left_square_color = (0, 137, 142)
right_square_color = (2, 216, 192)
left_canon = (11, 234, 6)
right_canon = (11, 25, 5)
spike_color = (11, 234, 4)

island_below_x = []
island_below_y = []
island_above_y = []

def main(n):
    # Tạo ảnh
    for x in range(1,n+1):
        img = create_background()
        
        img = draw_water(img)
        draw_platforms(img)
        spawn_hole(img)
        spawn_player(img)
        spawn_enemy(img)
        spawn_box_and_canon(img)
        spawn_tree(img)
        spawn_stair(img)
        spawn_box_and_canon(img)
        save_image(img, x)

if __name__ == "__main__":
    
    main(n = 1)
