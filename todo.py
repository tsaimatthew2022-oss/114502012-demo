tasks = []

def add_task(name):
    tasks.append(name)

def show_tasks():
    print("=== Todo List ===")
    for i, t in enumerate(tasks, 1):
        print(f"{i}. {t}")

def main():
    add_task("Learn Git")
    show_tasks()

if __name__ == "__main__":
    main()
