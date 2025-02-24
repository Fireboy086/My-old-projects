inventory = {
    "Дерево": 10,
    "Камінь": 5,
    "Залізо": 3,
    "Тканина": 2
}

recipes = {
    "Лук": {"Дерево": 3, "Тканина": 1},
    "Меч": {"Дерево": 2, "Залізо": 2}, 
    "Щит": {"Дерево": 5, "Камінь": 2},
    "Сумка": {"Тканина": 2, "Камінь": 1}
}

def can_craft(item):
    if item not in recipes:
        return False
    for resource, amount in recipes[item].items():
        if resource not in inventory or inventory[resource] < amount:
            return False
    return True

def craft(item):
    if not can_craft(item):
        print(f"Не вистачає ресурсів для створення {item}")
        return
    for resource, amount in recipes[item].items():
        inventory[resource] -= amount
    if item not in inventory:
        inventory[item] = 1
    else:
        inventory[item] += 1
    print(f"Створено: {item}")

def show_inventory():
    print("Інвентар:")
    for resource, amount in inventory.items():
        print(f"- {resource}: {amount}")

def play():
    while True:
        print("\nДоступні дії:")
        print("1. Створити предмет")
        print("2. Показати інвентар") 
        print("3. Вийти")
        
        choice = input("Введіть номер дії: ")
        
        if choice == "1":
            print("\nДоступні предмети для створення:")
            skip_counter = 0 
            for item in recipes:
                if can_craft(item):
                    print(f"- {item} потребує {recipes[item]}")
                else: skip_counter += 1
            if skip_counter == len(recipes):
                print("Немає ресурсів для створення. Спробуйте потім.")
                continue
            while True:
                item = input("Введіть назву предмета: ")
                if item in recipes:
                    if can_craft(item):
                        craft(item)
                        break
                    else:
                        print("Немає ресурсів для створення. Спробуйте ще раз.")
                else:
                    print("Невірний вибір. Спробуйте ще раз.")
        elif choice == "2":
            show_inventory()
        elif choice == "3":
            print("До зустрічі!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

play()