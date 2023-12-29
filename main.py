import json
import hashlib
from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, messagebox

from checkers.game import Game
from checkers.constants import X_SIZE, Y_SIZE, cell_size

class UserManager:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.load_users()

    def register_user(self, username, password):
        #Регестрация пользователя
        if username not in self.users:
            hashed_password = self._hash_password(password)
            self.users[username] = {'password': hashed_password}
            print(f"Пользователь {username} успешно зарегистрирован.")
            self.save_users()
            return True
        else:
            print(f"Пользователь {username} уже существует. Выберите другое имя.")
            return False

    def login_user(self, username, password):
        #Проверка на имя пользователя и пароль
        if username in self.users and self._verify_password(password, self.users[username]['password']):
            print(f"Вход пользователя {username} выполнен успешно.")
            self.current_user = username
            return True
        else:
            print("Неверное имя пользователя или пароль.")
            return False

    def save_users(self):
        #Сохранение пользователей
        with open('users.json', 'w') as f:
            json.dump(self.users, f)
            print("Пользователи сохранены.")

    def load_users(self):
        #Загрузка пользователей
        try:
            with open('users.json', 'r') as f:
                self.users = json.load(f)
                print("Пользователи загружены.")
        except FileNotFoundError:
            print("Файл пользователей не найден. Создан новый.")

    def _hash_password(self, password):
        #Шифрование
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def _verify_password(self, input_password, stored_hashed_password):
        #Проверка на пароль+
        return self._hash_password(input_password) == stored_hashed_password
def show_game_window(user_manager):
    #Открытие окна игры
    main_window = Tk()
    main_window.title('Шашки')
    main_window.resizable(0, 0)

    # Установка иконки окна
    icon_image = PhotoImage(file="icon.png")  # Укажите путь к вашей иконке
    main_window.iconphoto(False, icon_image)

    main_canvas = Canvas(main_window, width=cell_size * X_SIZE, height=cell_size * Y_SIZE)
    main_canvas.pack()

    game = Game(main_canvas, X_SIZE, Y_SIZE)

    main_canvas.bind("<Motion>", game.mouse_move)
    main_canvas.bind("<Button-1>", game.mouse_down)

    main_window.protocol("WM_DELETE_WINDOW", lambda: on_close(main_window, user_manager))
    main_window.mainloop()

def on_close(main_window, user_manager):
    user_manager.save_users()
    main_window.destroy()

def main():
    user_manager = UserManager()

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if user_manager.login_user(username, password):
            login_window.destroy()
            show_game_window(user_manager)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    login_window = Tk()
    login_window.title("Вход")
    login_window.geometry("400x400")

    username_label = Label(login_window, text="Имя пользователя:", bg="lightgray")
    username_label.pack()
    username_entry = Entry(login_window)
    username_entry.pack()

    password_label = Label(login_window, text="Пароль:", bg="lightgray")
    password_label.pack()
    password_entry = Entry(login_window, show="*")
    password_entry.pack()

    login_button = Button(login_window, text="Войти", command=login)
    login_button.pack()

    register_button = Button(login_window, text="Регистрация", command=lambda: register_window(user_manager))
    register_button.pack()

    login_window.mainloop()
def register_window(user_manager):
    #Окно регестрации
    register_window = Tk()
    register_window.title("Регистрация")
    register_window.geometry("400x400")

    username_label = Label(register_window, text="Имя пользователя:")
    username_label.pack()
    username_entry = Entry(register_window)
    username_entry.pack()
    password_label = Label(register_window, text="Пароль:")
    password_label.pack()
    password_entry = Entry(register_window, show="*")
    password_entry.pack()
    def register():
        username = username_entry.get()
        password = password_entry.get()
        if user_manager.register_user(username, password):
            register_window.destroy()
            messagebox.showinfo("Успешная регистрация", f"Пользователь {username} успешно зарегистрирован.")
        else:
            messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует")

    register_button = Button(register_window, text="Зарегистрироваться", command=register)
    register_button.pack()
    register_window.mainloop()

if __name__ == '__main__':
    main()
