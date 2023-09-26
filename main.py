from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    pass_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 12)
    nr_symbols = random.randint(3, 5)
    nr_numbers = random.randint(3, 5)

    letter_list = [random.choice(letters) for char in range(nr_letters)]

    symbol_list = [random.choice(symbols) for char in range(nr_symbols)]

    number_list = [random.choice(numbers) for char in range(nr_numbers)]

    password_list = letter_list + symbol_list + number_list

    random.shuffle(password_list)

    password = "".join(password_list)

    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    website = web_entry.get()
    mail = mail_entry.get()
    password = pass_entry.get()
    new_data = {
        website: {
            "email": mail,
            "password": password,
        }
    }

    if len(website) == 0 or len(mail) == 0 or len(password) == 0:
        messagebox.showwarning(title="WARNING!!", message="YOU LEFT SOMETHING OPEN, YOU FOOL!")
    else:
        try:
            with open("../../pass_data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("pass_data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("pass_data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            web_entry.delete(0, END)
            pass_entry.delete(0, END)


def search():
    website = web_entry.get()
    try:
        with open("pass_data.json", "r") as data_file:
            data = json.load(data_file)
            pyperclip.copy(data[website]['password'])
            messagebox.showinfo(title=f"{website}", message=f"Email: {data[website]['email']}\n"
                                                            f"Password: {data[website]['password']}")

    except FileNotFoundError:
        messagebox.showwarning(title="No data.", message="No password has been saved yet.")
    except KeyError:
        messagebox.showwarning(title="Not Found", message="This website has not been found")
    finally:
        web_entry.delete(0, END)
        pass_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
my_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=my_image)
canvas.grid(column=2, row=1)

website_label = Label(text="Website:")
website_label.grid(column=1, row=2)

email_label = Label(text="Email/Username:")
email_label.grid(column=1, row=3)

password_label = Label(text="Password:")
password_label.grid(column=1, row=4)

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.config(width=15)
generate_button.grid(column=3, row=4)

add_button = Button(text="Add", command=save_data)
add_button.config(width=44)
add_button.grid(column=2, row=5, columnspan=2)

search_button = Button(text="Search", command=search)
search_button.config(width=15)
search_button.grid(column=3, row=2)

web_entry = Entry()
web_entry.config(width=33)
web_entry.grid(column=2, row=2)
web_entry.focus()

mail_entry = Entry()
mail_entry.config(width=52)
mail_entry.grid(column=2, row=3, columnspan=2)
mail_entry.insert(0, "your_mail@gmail.com")

pass_entry = Entry()
pass_entry.config(width=33)
pass_entry.grid(column=2, row=4)

window.mainloop()
