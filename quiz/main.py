from question_file import *
import os
import pygame as PG

DEBUG = False

def debug_render():
    global cur_time, a, b
    debug_frames = debug_font.render(f"frames since start: {b}", True, LBBG, None)
    debug_timer = debug_font.render(f"seconds since start: {a}", True, LBBG, None)

    if PG.time.get_ticks() - cur_time >= 1000:
        cur_time += 1000
        a += 1
        debug_timer = debug_font.render(f"seconds since start: {a}", True, LBBG, None)

    screen.blit(debug_timer, (0, 0))
    screen.blit(debug_frames, (0, 20))

PG.init()

base_dir = os.path.dirname(os.path.abspath(__file__))
BG_path = os.path.join(base_dir, "WWTBAM.png")
font_file_name = "Arial Rounded Bold.ttf"
font_path = os.path.join(base_dir, font_file_name)

if not os.path.isfile(font_path):
    print(f"Font file '{font_file_name}' not found in the current directory.")
else:
    print("Font Path:", font_path)

debug_font = PG.font.Font(font_path, 20)
screen = PG.display.set_mode((720, 540))
LBBG = (143, 180, 204)
BGImage = PG.image.load(BG_path)

a = 0
b = 0
FPS = 120
cur_time = 0
buttons = {
    "A": PG.rect.Rect(50, 415, 300, 45),
    "B": PG.rect.Rect(370, 415, 300, 45),
    "C": PG.rect.Rect(50, 470, 300, 45),
    "D": PG.rect.Rect(370, 470, 300, 45)
 }
debug_mode = False

clock = PG.time.Clock()
game = True

ABCD = ["A", "B", "C", "D"]
QLen = len(questions)
answered_correctly = 0
UserAnswer = None
current_question = 0

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    if current_line:
        lines.append(current_line)

    return lines

def display_question():
    global debug_font
    question_text = debug_questions[current_question] if DEBUG else questions[current_question]
    font_size = 70
    debug_font = PG.font.Font(font_path, font_size)
    text_box_rect = PG.rect.Rect(120, 320, 500, 65)
    wrapped_lines = wrap_text(question_text, debug_font, text_box_rect.width)

    while len(wrapped_lines) * debug_font.get_height() > text_box_rect.height:
        font_size -= 5
        if font_size <= 10:
            font_size = 10
            break
        debug_font = PG.font.Font(font_path, font_size)
        wrapped_lines = wrap_text(question_text, debug_font, text_box_rect.width)

    PG.draw.rect(screen, (3, 3, 117), text_box_rect)

    for i, line in enumerate(wrapped_lines):
        line_surface = debug_font.render(line, True, LBBG, None)
        screen.blit(line_surface, (text_box_rect.x + 10, text_box_rect.y + 10 + i * debug_font.get_height()))

def create_answer_buttons():
    answer_buttons = {}
    possible_answers = debug_answers[current_question] if DEBUG else answers[current_question]
    
    for i, answer in enumerate(possible_answers):
        button_label = f"{answer}"
        max_length = 30
        if len(button_label) > max_length:
            button_label = button_label[:max_length - 3] + "..."

        button_rect = PG.rect.Rect(50 + (i % 2) * 320, 406 + (i // 2) * 57, 300, 45)
        answer_buttons[ABCD[i]] = (button_rect, button_label)

    return answer_buttons

def correct():
    global answered_correctly
    answered_correctly += 1

def incorrect():
    pass

def render_button_text(button_label, button_rect):
    font_size = 30
    button_font = PG.font.Font(font_path, font_size)

    button_surface = button_font.render(button_label, True, (255, 255, 255))
    while button_surface.get_width() > button_rect.width - 20:
        font_size -= 2
        if font_size <= 10:
            font_size = 10
            break
        button_font = PG.font.Font(font_path, font_size)
        button_surface = button_font.render(button_label, True, (255, 255, 255))

    return button_surface

while current_question < QLen and game:
    b += 1
    screen.blit(BGImage, (0, 0))
    display_question()
    answer_buttons = create_answer_buttons()

    for event in PG.event.get():
        if event.type == PG.QUIT:
            game = False
        elif event.type == PG.MOUSEBUTTONDOWN:
            mouse_pos = PG.mouse.get_pos()
            for button_name, (button_rect, button_label) in answer_buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    UserAnswer = button_name
                    if DEBUG:
                        if UserAnswer.upper() == ABCD[debug_correct_answers[current_question]]:
                            correct()
                        else:
                            incorrect()
                    else:
                        if UserAnswer.upper() == ABCD[correct_answers[current_question]]:
                            correct()
                        else:
                            incorrect()
                    
                    current_question += 1
                    UserAnswer = None
                    break
        elif event.type == PG.KEYDOWN:
            if event.key == PG.K_d:
                debug_mode = not debug_mode
                
    if debug_mode:
        debug_render()

    for button_name, (button_rect, button_label) in answer_buttons.items():
        PG.draw.rect(screen, (0, 0, 0), button_rect, 2)
        button_surface = render_button_text(button_label, button_rect)
        text_x = button_rect.x + (button_rect.width - button_surface.get_width()) // 2
        text_y = button_rect.y + (button_rect.height - button_surface.get_height()) // 2
        screen.blit(button_surface, (text_x, text_y))

    PG.display.update()
    clock.tick(FPS)

print("\n" + f"Well done, you have completed the quiz. You got {answered_correctly}/{QLen} points")
