import time
import pygame
import random
import math

pygame.init()
width = 986
height = 800

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("                                                                                                                                  Shaolin Harmony Havens Slots")
logo = pygame.image.load('images/slot-machine (1).png')
pygame.display.set_icon(logo)

background_image = pygame.image.load("images/background.png")

icons_dict = {
    "monk": pygame.image.load("images/monk.png"),
    "temple": pygame.image.load("images/temple.png"),
    "power": pygame.image.load("images/power.png"),
    "meditate": pygame.image.load("images/meditate_eye.png"),
    "letter": pygame.image.load("images/letter-h.png"),
    "dragon": pygame.image.load("images/dragon.png"),
    "shuriken": pygame.image.load("images/shuriken.png")
}

sounds_dict = {
    "wheel": pygame.mixer.Sound("sounds/wheel.mp3"),
    "win": pygame.mixer.Sound("sounds/win_sound.mp3"),
    "cashier": pygame.mixer.Sound("sounds/casier.mp3"),
    "china_song": pygame.mixer.Sound("sounds/china_song.mp3")
}


def play_background_theme():
    pygame.mixer.music.load("sounds/china_song.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1) 


def stop_background_theme():
    pygame.mixer.music.stop()

cell_width = width // 3
cell_height = height // 3

font = pygame.font.Font(None, 36)
label_font = pygame.font.Font(None, 26)

input_box = pygame.Rect(width // 2 - 200, height - 115, 400, 40)
label_rect = pygame.Rect(width // 2 - 350, height - 145, 692, 30)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
text = ''
text_surface = font.render(text, True, color)
active = False

deposit_button_rect = pygame.Rect(width // 2 - 50, height - 72, 100, 30)
deposit_button_color = pygame.Color('green')
deposit_button_text = label_font.render("DEPOSIT", True, pygame.Color('white'))

bet_buttons = [
    {"rect": pygame.Rect(50, height - 40, 60, 30), "amount": 0.2},
    {"rect": pygame.Rect(120, height - 40, 60, 30), "amount": 0.5},
    {"rect": pygame.Rect(190, height - 40, 60, 30), "amount": 1.00},
    {"rect": pygame.Rect(260, height - 40, 60, 30), "amount": 2.00},
    {"rect": pygame.Rect(330, height - 40, 60, 30), "amount": 3.00},
    {"rect": pygame.Rect(400, height - 40, 60, 30), "amount": 5.00},
    {"rect": pygame.Rect(470, height - 40, 60, 30), "amount": 10.00},
    {"rect": pygame.Rect(540, height - 40, 60, 30), "amount": 25.00},
    {"rect": pygame.Rect(610, height - 40, 60, 30), "amount": 50.00},
    {"rect": pygame.Rect(680, height - 40, 60, 30), "amount": 100.00},
]

spin_button = False
reels = [random.choice(list(icons_dict.keys())) for _ in range(9)]
balance = 0
message_font = pygame.font.Font(None, 48)

shaking_icons = []
shaking_start_time = 0
shaking_duration = 100


def shake_winning_icons(winning_indices):
    global shaking_icons, shaking_start_time
    shaking_icons = [(row, col) for row in range(3) for col in range(3) if row * 3 + col in winning_indices]
    shaking_start_time = time.time()
    sounds_dict["win"].play()  


def draw_shaking_icons():
    global shaking_icons, shaking_start_time
    if shaking_icons and time.time() - shaking_start_time < shaking_duration:
        for row, col in shaking_icons:
            x = (width - 3 * cell_width) // 2 + col * cell_width
            y = (height - 3 * cell_height) // 2 + row * cell_height
            image_name = reels[row * 3 + col]
            image = icons_dict.get(image_name)
            if image:
                offset = random.randint(-5, 5)
                rotation_angle = random.randint(-5, 5)
                scale_factor = 1.0 + random.uniform(-0.1, 0.1)
                rotated_image = pygame.transform.rotate(image, rotation_angle)
                scaled_image = pygame.transform.scale(rotated_image, (int(image.get_width() * scale_factor),
                                                                      int(image.get_height() * scale_factor)))
                screen.blit(scaled_image, (x + offset, y + offset))
    else:
        shaking_icons = []


def check_winning_conditions(result_reels, bet_amount):
    global winnings
    if result_reels[0] == result_reels[1] == result_reels[2]:
        winnings += bet_amount * 12.43
        return True
    elif result_reels[3] == result_reels[4] == result_reels[5]:
        winnings += bet_amount * 12.33
        return True
    elif result_reels[1] == result_reels[4] == result_reels[5]:
        winnings += bet_amount * 1.22
        return True
    elif result_reels[1] == result_reels[4] == result_reels[5]:
        winnings += bet_amount * 1.22
        return True
    elif result_reels[5] == result_reels[6] == result_reels[4]:
        winnings += bet_amount * 1.42
        return True
    elif result_reels[3] == result_reels[6] == result_reels[7]:
        winnings += bet_amount * 1.42
        return True
    elif result_reels[4] == result_reels[7] == result_reels[8]:
        winnings += bet_amount * 1.34
        return True
    elif result_reels[3] == result_reels[4] == result_reels[8] == result_reels[2]:
        winnings += bet_amount * 5.55
        return True
    elif result_reels[2] == result_reels[4] == result_reels[5] == result_reels[6]:
        winnings += bet_amount * 10.55
        return True
    elif result_reels[2] == result_reels[3] == result_reels[4] == result_reels[6]:
        winnings += bet_amount * 10.55
        return True
    elif result_reels[3] == result_reels[4] == result_reels[6]:
        winnings += bet_amount * 1.4
        return True
    elif result_reels[0] == result_reels[1] == result_reels[4] == result_reels[5]:
        winnings += bet_amount * 6
        return True
    elif result_reels[2] == result_reels[1] == result_reels[4] == result_reels[5]:
        winnings += bet_amount * 6
        return True
    elif result_reels[0] == result_reels[1] == result_reels[3] == result_reels[4]:
        winnings += bet_amount * 6
        return True
    elif result_reels[3] == result_reels[4] == result_reels[6] == result_reels[7]:
        winnings += bet_amount * 6
        return True
    elif result_reels[4] == result_reels[5] == result_reels[7] == result_reels[8]:
        winnings += bet_amount * 6
        return True
    elif result_reels[6] == result_reels[7] == result_reels[8]:
        winnings += bet_amount * 9.23
        return True
    elif result_reels[0] == result_reels[1] == result_reels[2] and result_reels[3] == result_reels[4] == result_reels[
        5]:
        winnings += bet_amount * 230.45
        return True
    elif result_reels[6] == result_reels[7] == result_reels[8] and result_reels[0] == result_reels[1] == result_reels[
        2]:
        winnings += bet_amount * 230.54
        return True
    elif result_reels[3] == result_reels[4] == result_reels[5] == result_reels[6] == result_reels[7] == result_reels[8]:
        winnings += bet_amount * 30.53
        return True
    elif result_reels[3] == result_reels[4] == result_reels[6]:
        winnings += bet_amount * 2
        return True
    elif result_reels[1] == result_reels[3] == result_reels[4] == result_reels[5] == result_reels[7]:
        winnings += bet_amount * 11
        return True
    elif len(set(result_reels)) == 1:
        winnings += bet_amount * 100000
        return True
    elif len(set(result_reels)) == 2:
        winnings += bet_amount * 1500
        return True
    elif result_reels[1] == result_reels[3] == result_reels[5] == result_reels[7]:
        winnings += bet_amount * 17.6
        return True
    elif len(set(result_reels)) == 3:
        winnings += bet_amount * 20
        return True
    elif result_reels[0] == result_reels[4] == result_reels[8]:
        winnings += bet_amount * 6.2
        return True
    elif result_reels[2] == result_reels[5] == result_reels[8]:
        winnings += bet_amount * 5.45
        return True
    elif result_reels[1] == result_reels[4] == result_reels[7]:
        winnings += bet_amount * 3.5
        return True
    elif result_reels[0] == result_reels[3] == result_reels[6]:
        winnings += bet_amount * 2.15
        return True
    elif result_reels[2] == result_reels[4] == result_reels[6]:
        winnings += bet_amount * 6.2
        return True
    elif result_reels[2] == result_reels[4]:
        winnings += bet_amount * 1.2
        return True
    elif result_reels[1] == result_reels[3] == result_reels[4]:
        winnings += bet_amount * 1
        return True
    elif result_reels[1] == result_reels[3] == result_reels[4] == result_reels[5]:
        winnings += bet_amount * 5.2
        return True
    return False



def spin_reels():
    sounds_dict["wheel"].play()
    spinning_duration = 1000 
    acceleration_duration = 200  
    spin_speed = 0.1 
    max_spin_speed = 5.5 
    acceleration = (max_spin_speed - spin_speed) / acceleration_duration

    result_reels = [random.choice(list(icons_dict.keys())) for _ in range(9)]

    start_time = pygame.time.get_ticks()
    elapsed_time = 0

    while elapsed_time < spinning_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        elapsed_time = pygame.time.get_ticks() - start_time
        progress = elapsed_time / spinning_duration

        if elapsed_time < acceleration_duration:
            spin_speed += acceleration
            offset = int(progress * spin_speed)
        else:
            offset = int(ease_out_cubic(progress) * max_spin_speed)

        for row in range(3):
            for col in range(3):
                x = (width - 3 * cell_width) // 2 + col * cell_width
                y = (height - 3 * cell_height) // 2 + row * cell_height
                index = row * 3 + col
                image_name = random.choice(list(icons_dict.keys()))
                image = icons_dict.get(image_name)
                if image:
                    screen.blit(image, (x + offset, y + offset))

        pygame.display.flip()
        pygame.time.delay(8)  

 
    result_reels = [random.choice(list(icons_dict.keys())) for _ in range(9)]

    return result_reels


def ease_out_cubic(t):
    return 1 - math.pow(1 - t, 3)


def display_result(result_reels):
    start_time = pygame.time.get_ticks()
    spinning_duration = 2000  # 2 seconds

    while pygame.time.get_ticks() - start_time < spinning_duration:
        for row in range(3):
            for col in range(3):
                x = (width - 3 * cell_width) // 2 + col * cell_width
                y = (height - 3 * cell_height) // 2 + row * cell_height
                index = row * 3 + col
                image_name = random.choice(list(icons_dict.keys()))
                image = icons_dict.get(image_name)
                if image:
                    screen.blit(image, (x, y))

        pygame.display.flip()
        time.sleep(0.1)

    result_reels = spin_reels()

    for row in range(3):
        for col in range(3):
            x = (width - 3 * cell_width) // 2 + col * cell_width
            y = (height - 3 * cell_height) // 2 + row * cell_height
            index = row * 3 + col
            image_name = result_reels[index]
            image = icons_dict.get(image_name)
            if image:
                screen.blit(image, (x, y))

    pygame.display.flip()

    return result_reels



play_background_theme()

message = None
run = True
while run:
    winnings = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            elif deposit_button_rect.collidepoint(event.pos) and not active:
                try:
                    balance = int(text)
                    print("Balance set to:", balance)
                    deposit_button_rect = pygame.Rect(0, 0, 0, 0)

                    sounds_dict["cashier"].play()

                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            for button in bet_buttons:
                if button["rect"].collidepoint(event.pos) and balance is not None:
                    if balance >= button["amount"]:
                        balance -= button["amount"]
                        print(f"Player bet {button['amount']} dollars.")
                        reels = display_result(reels)
                        print(f"Remaining balance: {balance:.2f}")

                        if check_winning_conditions(reels, button["amount"]):
                            balance += winnings
                            message = f"WON {winnings:.2f} $$$"
                            print(f"WON {winnings:.2f} $$$")
                            sounds_dict["win"].play()
                            winning_indices = [i for i, symbol in enumerate(reels) if reels.count(symbol) >= 3]
                            shake_winning_icons(winning_indices)  # Start shaking only the winning icons
                        else:
                            print("No win this round.")
                    else:
                        print("Insufficient balance.")


        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    try:
                        balance = int(text)
                        print("Balance set to:", balance)
                        active = False
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                text_surface = font.render(text, True, color)

    screen.blit(background_image, (0, 0))

    if deposit_button_rect.width > 0:
        label_text = "Enter a valid number between 20 and 150,000 and press Enter, then Deposit to start"
        label_surface = label_font.render(label_text, True, pygame.Color('white'))
        pygame.draw.rect(screen, pygame.Color('black'), label_rect)
        screen.blit(label_surface, (label_rect.x + 5, label_rect.y + 5))

        pygame.draw.rect(screen, color, input_box, 2)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        pygame.draw.rect(screen, deposit_button_color, deposit_button_rect)
        screen.blit(deposit_button_text, (deposit_button_rect.x + 10, deposit_button_rect.y + 5))

    for button in bet_buttons:
        pygame.draw.rect(screen, pygame.Color('black'), button["rect"])
        button_text = label_font.render(f"{button['amount']:.2f}", True, pygame.Color('white'))
        screen.blit(button_text, (button["rect"].x + 10, button["rect"].y + 5))

    for row in range(3):
        for col in range(3):
            x = (width - 3 * cell_width) // 2 + col * cell_width
            y = (height - 3 * cell_height) // 2 + row * cell_height
            index = row * 3 + col
            image_name = reels[index]
            image = icons_dict.get(image_name)
            if image:
                screen.blit(image, (x, y))

    draw_shaking_icons() 

    if message:
        message_text = message_font.render(message, True, pygame.Color('yellow'))
        screen.blit(message_text, (width // 2 - 150, height // 2))

    pygame.display.flip()

stop_background_theme()

pygame.quit()
quit()
