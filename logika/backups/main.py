import pygame as PG



DBUEG = False


PG.init()
PG.display.init()
PG.font.init()
questions = [
    "1. What is the capital of France?",
    "2. Which planet is known as the Red Planet?",
    "3. What is the largest mammal in the world?",
    "4. Who wrote 'Romeo and Juliet'?",
    "5. What is the smallest prime number?",
    "6. Which element has the chemical symbol 'O'?",
    "7. Who painted the Mona Lisa?",
    "8. What is the boiling point of water at sea level in degrees Celsius?",
    "9. In which continent is the Sahara Desert located?",
    "10. Who is known as the father of computers?",
    "11. What is the largest planet in our solar system?",
    "12. Which language is predominantly spoken in Brazil?",
    "13. What is the process by which plants make their food called?",
    "14. Who discovered penicillin?",
    "15. What is the hardest natural substance on Earth?",
    "16. Which organ purifies our blood?",
    "17. Who wrote '1984' and 'Animal Farm'?",
    "18. What is the currency of Japan?",
    "19. Which gas do plants absorb from the atmosphere?",
    "20. Who was the first person to walk on the moon?",
    "21. What is the chemical formula for water?",
    "22. Which country gifted the Statue of Liberty to the USA?",
    "23. What is the largest ocean on Earth?",
    "24. Who developed the theory of relativity?",
    "25. What is the main language spoken in Canada?",
    "26. Which planet is known for its rings?",
    "27. Who is the author of the 'Harry Potter' series?",
    "28. What is the tallest mountain in the world?",
    "29. What is the hardest known mineral?",
    "30. Who painted the ceiling of the Sistine Chapel?",
    "31. What is the smallest country in the world?",
    "32. Which gas is most abundant in Earth's atmosphere?",
    "33. Who is known as the 'Maid of Orléans'?",
    "34. What is the largest bone in the human body?",
    "35. Which planet is closest to the Sun?",
    "36. What is the capital city of Australia?",
    "37. Who composed 'The Four Seasons'?",
    "38. Which blood type is known as the universal donor?",
    "39. What is the primary source of energy for Earth's climate system?",
    "40. Who is the Greek god of the sea?",
    "41. What is the most spoken language in the world?",
    "42. What is the process of cell division in somatic cells called?",
    "43. Who is the CEO of Tesla as of 2021?",
    "44. Which element has the highest atomic number?",
    "45. What is the capital of South Korea?",
    "46. Who wrote 'Pride and Prejudice'?",
    "47. What is the largest artery in the human body?",
    "48. What is the main ingredient in sushi?",
    "49. Which country hosted the 2016 Summer Olympics?",
    "50. What is the term for animals that eat both plants and meat?"
]
answers = [
    ["A) Berlin", "B) Madrid", "C) Paris", "D) Rome"],
    ["A) Earth", "B) Mars", "C) Jupiter", "D) Venus"],
    ["A) Elephant", "B) Blue Whale", "C) Giraffe", "D) Great White Shark"],
    ["A) Charles Dickens", "B) William Shakespeare", "C) Mark Twain", "D) Jane Austen"],
    ["A) 1", "B) 2", "C) 3", "D) 5"],
    ["A) Gold", "B) Oxygen", "C) Hydrogen", "D) Carbon"],
    ["A) Vincent van Gogh", "B) Pablo Picasso", "C) Leonardo da Vinci", "D) Michelangelo"],
    ["A) 50°C", "B) 100°C", "C) 150°C", "D) 200°C"],
    ["A) Asia", "B) Africa", "C) South America", "D) Australia"],
    ["A) Steve Jobs", "B) Bill Gates", "C) Charles Babbage", "D) Alan Turing"],
    ["A) Earth", "B) Mars", "C) Jupiter", "D) Saturn"],
    ["A) Spanish", "B) Portuguese", "C) French", "D) English"],
    ["A) Photosynthesis", "B) Respiration", "C) Transpiration", "D) Digestion"],
    ["A) Alexander Fleming", "B) Marie Curie", "C) Louis Pasteur", "D) Isaac Newton"],
    ["A) Gold", "B) Diamond", "C) Iron", "D) Platinum"],
    ["A) Heart", "B) Kidney", "C) Liver", "D) Lungs"],
    ["A) George Orwell", "B) J.R.R. Tolkien", "C) Ernest Hemingway", "D) F. Scott Fitzgerald"],
    ["A) Yen", "B) Dollar", "C) Euro", "D) Won"],
    ["A) Oxygen", "B) Carbon Dioxide", "C) Nitrogen", "D) Hydrogen"],
    ["A) Yuri Gagarin", "B) Neil Armstrong", "C) Buzz Aldrin", "D) Michael Collins"],
    ["A) H2O", "B) CO2", "C) O2", "D) NaCl"],
    ["A) Spain", "B) France", "C) Italy", "D) Germany"],
    ["A) Atlantic Ocean", "B) Indian Ocean", "C) Pacific Ocean", "D) Arctic Ocean"],
    ["A) Isaac Newton", "B) Nikola Tesla", "C) Albert Einstein", "D) Galileo Galilei"],
    ["A) English", "B) French", "C) Spanish", "D) Chinese"],
    ["A) Earth", "B) Mars", "C) Saturn", "D) Uranus"],
    ["A) J.K. Rowling", "B) Stephen King", "C) J.R.R. Tolkien", "D) C.S. Lewis"],
    ["A) K2", "B) Mount Everest", "C) Kangchenjunga", "D) Lhotse"],
    ["A) Quartz", "B) Corundum", "C) Diamond", "D) Topaz"],
    ["A) Raphael", "B) Michelangelo", "C) Donatello", "D) Leonardo da Vinci"],
    ["A) Monaco", "B) Vatican City", "C) San Marino", "D) Liechtenstein"],
    ["A) Oxygen", "B) Nitrogen", "C) Carbon Dioxide", "D) Hydrogen"],
    ["A) Joan of Arc", "B) Florence Nightingale", "C) Marie Curie", "D) Cleopatra"],
    ["A) Femur", "B) Tibia", "C) Fibula", "D) Humerus"],
    ["A) Mercury", "B) Venus", "C) Earth", "D) Mars"],
    ["A) Sydney", "B) Melbourne", "C) Canberra", "D) Brisbane"],
    ["A) Mozart", "B) Vivaldi", "C) Beethoven", "D) Bach"],
    ["A) O+", "B) O-", "C) AB+", "D) AB-"],
    ["A) The Sun", "B) The Moon", "C) Earth's Core", "D) Volcanoes"],
    ["A) Zeus", "B) Poseidon", "C) Hades", "D) Apollo"],
    ["A) English", "B) Mandarin Chinese", "C) Spanish", "D) Hindi"],
    ["A) Mitosis", "B) Meiosis", "C) Fusion", "D) Fission"],
    ["A) Jeff Bezos", "B) Elon Musk", "C) Tim Cook", "D) Sundar Pichai"],
    ["A) Uranium", "B) Plutonium", "C) Oganesson", "D) Iron"],
    ["A) Seoul", "B) Tokyo", "C) Beijing", "D) Bangkok"],
    ["A) Emily Brontë", "B) Jane Austen", "C) Charlotte Brontë", "D) Louisa May Alcott"],
    ["A) Aorta", "B) Vena Cava", "C) Pulmonary Artery", "D) Femoral Artery"],
    ["A) Rice", "B) Bread", "C) Pasta", "D) Potatoes"],
    ["A) China", "B) Brazil", "C) Russia", "D) United Kingdom"],
    ["A) Herbivores", "B) Carnivores", "C) Omnivores", "D) Detritivores"]
]
correct_answers = [
    2,  # C) Paris
    1,  # B) Mars
    1,  # B) Blue Whale
    1,  # B) William Shakespeare
    1,  # B) 2
    1,  # B) Oxygen
    2,  # C) Leonardo da Vinci
    1,  # B) 100°C
    1,  # B) Africa
    2,  # C) Charles Babbage
    2,  # C) Jupiter
    1,  # B) Portuguese
    0,  # A) Photosynthesis
    0,  # A) Alexander Fleming
    1,  # B) Diamond
    1,  # B) Kidney
    0,  # A) George Orwell
    0,  # A) Yen
    1,  # B) Carbon Dioxide
    1,  # B) Neil Armstrong
    0,  # A) H2O
    1,  # B) France
    2,  # C) Pacific Ocean
    2,  # C) Albert Einstein
    1,  # B) French
    2,  # C) Saturn
    0,  # A) J.K. Rowling
    1,  # B) Mount Everest
    2,  # C) Diamond
    1,  # B) Michelangelo
    1,  # B) Vatican City
    1,  # B) Nitrogen
    0,  # A) Joan of Arc
    0,  # A) Femur
    0,  # A) Mercury
    2,  # C) Canberra
    1,  # B) Vivaldi
    1,  # B) O-
    0,  # A) The Sun
    1,  # B) Poseidon
    1,  # B) Mandarin Chinese
    0,  # A) Mitosis
    1,  # B) Elon Musk
    2,  # C) Oganesson
    0,  # A) Seoul
    1,  # B) Jane Austen
    0,  # A) Aorta
    0,  # A) Rice
    1,  # B) Brazil
    2   # C) Omnivores
]
debug_questions = ["lakjshrlgkjhadsiulfghuiaehgvjkldznavuivhwpaowiuyed;lfkjvhsaiugfyahw;leuifhasdkjg;asdifohguwoue;rhg;asflkgh∑´®ß∂†ƒ©¥˙¨∆ç≈∂ƒ©√∫∆˜˚¬ˆ˙¨¥©†ƒ˙√∫˜∆¬ˆ˚ø∆¨∆¥","©ƒ®∂†¥¨ç∆˚†©ˆ¨…¬©†√¥ƒˆ®†øˆ¨¥√†øˆ¨¥˚†","al;kiufhrgpaeiurhgpaieurhgear","LAKDJFHGPULOERHLVAZDFKUJGHPEAIURFGHNHEDI"]
debug_answers = [["Fuck You","Fuck You","Fuck You","Fuck You"],["Fuck You","Fuck You","Fuck You","Fuck You"],["Fuck You","Fuck You","Fuck You","Fuck You"],["Fuck You","Fuck You","Fuck You","Fuck You"]]
debug_correct_answers = [0,0,0,0]

BG_path = "WWTBAM.png"
font_path = "Arial Rounded Bold.ttf"
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
    question_text = debug_questions[current_question] if DBUEG else questions[current_question]
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
    possible_answers = debug_answers[current_question] if DBUEG else answers[current_question]
    
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
                    if DBUEG:
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
