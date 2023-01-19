import os
import math
import copy
import statistics
import colorama
import winsound
import PIL as pil
import glob
from PIL import ImageGrab, ImageFont
from tkinter.ttk import *
from art import tprint
from tkinter import *
from math import *
from colorama import Fore


def calculation():
    global angels, sides, triangle_area, result, round_combobox, triangle_sides, triangle_angl, sides_sort, a_canvas_lbl, b_canvas_lbl, c_canvas_lbl,triangle_find

    canvas.delete("all")
    try:
        c_canvas_lbl.destroy()
        a_canvas_lbl.destroy()
        b_canvas_lbl.destroy()
        AB_value_lbl.destroy()
        BC_value_lbl.destroy()
        AC_value_lbl.destroy()
    except NameError:
        pass

    result = " "
    sides = []
    angels = []

    side_ab = side1.get()
    side_bc = side2.get()
    side_ac = side3.get()

    angel_a = angle1.get()
    angel_b = angle2.get()
    angel_c = angle3.get()

    angles_entry = [angel_a, angel_b, angel_c]
    sides_entry = [side_ab, side_bc, side_ac]
    print(f"{Fore.YELLOW} -----Введённые данные-----")
    for i in range(len(sides_entry)):
        try:
            sides.append(float(sides_entry[i]))
        except ValueError:
            sides.append("_")
    print(f" Стороны: {sides}")

    for j in range(len(angles_entry)):
        try:
            angels.append(float(angles_entry[j]))
        except ValueError:
            angels.append("_")
    print(f" Углы: {angels}")
    check_sides = tuple(sides)
    sum_angles = sum([i for i in angels if isinstance(i, float)])
    if sum_angles > 180:
        area_lbl['text'] = "Сумма углов должна быть \n равна 180 гpадусам"
        print(f"{Fore.RED} Error2: Сумма углов должна быть равна 180 гpадусам")
        print("------------------------------------------------------------")
        return None

    if "_" not in angels:
        if sum(angels) != 180:
            area_lbl['text'] = "Сумма углов должна быть \n равна 180 гадусам"
            print(f"{Fore.RED} Error2: Сумма углов должна быть равна 180 гpадусам")
            print("------------------------------------------------------------")
            return None

    for k in sides:
        if k != "_" and k <= 0:
            area_lbl['text'] = "Значения сторон должны \n быть больше нуля!!! "
            print(f"{Fore.RED} Error4: Значения сторон должны быть больше нуля ")
            print("------------------------------------------------------------")
            return None

    for l in angels:
        if l != "_" and (l < 0) or l != "_" and (l > 180):
            area_lbl['text'] = "углы должны быть больше 0, \n но меньше 180 градусов "
            print(f"{Fore.RED} Error5: углы должны быть больше 0, но меньше 180 градусов ")
            print("------------------------------------------------------------")
            return None

    a = [x for x in angels if type(x) != str]
    if (len(a) == 2) and (sum(a) < 180):
        index = angels.index("_")
        third_angl = 180 - sum(a)
        a.insert(index, third_angl)
        angels = a

    if round_combobox.get() == "до целых":
        difference = 1
    elif round_combobox.get() == "до десятых":
        difference = 0.1
    elif round_combobox.get() == "до сотых":
        difference = 0.01
    elif round_combobox.get() == "до тысячных":
        difference = 0.001

    if "_" not in sides and all(t > 0 for t in sides):
        if (sides[0] + sides[1] < sides[2]) or (sides[1] + sides[2] < sides[0]) or (sides[2] + sides[0] < sides[1]):
            area_lbl['text'] = "Ошибка ввода сторон \n(нельзя построить треугольник)"
            print(f"{Fore.RED} Error3: ввода сторон (нельзя построить треугольник)")
            print("------------------------------------------------------------")
            return None
        avg = statistics.mean(sides)
        average_side = min(sides, key=lambda num: abs(num - avg))
        sides = [average_side, min(sides), max(sides)]
        print(three_sides())

    elif "_" != sides[1] and "_" != sides[2] and "_" != angels[2]:  # С угол мужду сторонами
        print(two_sides_one_angle(sides[1], sides[2], angels[2]))
    elif "_" != sides[0] and "_" != sides[1] and "_" != angels[1]:  # B угол между сторонами
        print(two_sides_one_angle(sides[0], sides[1], angels[1]))
    elif "_" != sides[0] and "_" != sides[2] and "_" != angels[0]:  # A угол между сторонами
        print(two_sides_one_angle(sides[0], sides[2], angels[0]))

    elif "_" != angels[0] and "_" != angels[1] and "_" != sides[0]:
        print(two_angles_one_side(angels[0], angels[1], sides[0]))
    elif "_" != angels[1] and "_" != angels[2] and "_" != sides[1]:
        print(two_angles_one_side(angels[1], angels[2], sides[1]))
    elif "_" != angels[0] and "_" != angels[2] and "_" != sides[2]:
        print(two_angles_one_side(angels[0], angels[2], sides[2]))
    else:
        area_lbl['text'] = "Недостаточно данных\n или неправильный ввод!!!"
        print(f"{Fore.RED} Error1: Недостаточно данных или неправильный ввод")
        print("------------------------------------------------------------")
        return None

    num_sides = sides.copy()
    num_angl = angels.copy()

    count_slash_sides = sides.count("_")
    count_slash_angl = angels.count("_")

    for x in range(count_slash_sides):
        num_sides.remove("_")

    for y in range(count_slash_angl):
        num_angl.remove("_")

    check_s = True
    check_a = True

    for m in range(len(num_sides)):
        closest_side = min(triangle_sides, key=lambda x: abs(x - num_sides[m]))
        if abs(closest_side - num_sides[m]) > difference:
            check_s = False

    for n in range(len(num_angl)):
        closest_angl = min(triangle_angl, key=lambda z: abs(z - num_angl[n]))
        if abs(closest_angl - num_angl[n]) > difference:
            check_a = False

    print(f" Проверка сторон: {check_s} \n Проверка углов: {check_a}")
    if (check_a is True) and (check_s is True):
        half_p = sum(triangle_sides) / 2
        triangle_area = sqrt(
            (half_p * (half_p - triangle_sides[0]) * (half_p - triangle_sides[1]) * (half_p - triangle_sides[2])))
        area_lbl['text'] = f"S = {triangle_area}      "
        print(f"{Fore.GREEN} S = {triangle_area}      ")
        if "_" not in sides:
            triangle_sides = copy.copy(check_sides)
        else:
            sides_copy = copy.copy(sides)
            for o in range(3):
                if triangle_sides[o] not in sides_copy:
                    slash_index_sides = sides_copy.index("_")
                    sides.insert(slash_index_sides, triangle_sides[o])
                    sides.remove("_")
            triangle_sides = sides
        draw(triangle_sides[0], triangle_sides[1], triangle_sides[2])
        triangle_find = True
        print("------------------------------------------------------------")
    else:
        try:
            c_canvas_lbl.destroy()
            a_canvas_lbl.destroy()
            b_canvas_lbl.destroy()
            AB_value_lbl.destroy()
            BC_value_lbl.destroy()
            AC_value_lbl.destroy()
        except NameError:
            pass
        area_lbl['text'] = "Ошибка ввода данных!!! "
        print(f"{Fore.RED} Error1: Недостаточно данных или неправильный ввод")
        print("------------------------------------------------------------")


def three_sides():
    global triangle_angl, triangle_sides

    check_angle1 = degrees(acos((sides[1] ** 2 + sides[2] ** 2 - sides[0] ** 2) / (2 * sides[1] * sides[2])))
    check_angle2 = degrees(acos((sides[1] ** 2 + sides[0] ** 2 - sides[2] ** 2) / (2 * sides[0] * sides[1])))
    check_angle3 = 180 - (check_angle1 + check_angle2)
    triangle_sides = [sides[0], sides[1], sides[2]]
    triangle_angl = [check_angle1, check_angle2, check_angle3]
    print(f"{Fore.YELLOW} ---Решение Треугольника---")
    return f" Углы: {triangle_angl} \n Стороны: {triangle_sides} \n Рещение треугольника: по трем сторонам"


def two_sides_one_angle(check_side1, check_side2, check_angle1):
    global triangle_angl, triangle_sides

    check_side3 = sqrt(
        check_side1 ** 2 + check_side2 ** 2 - 2 * check_side1 * check_side2 * cos(check_angle1 / 360 * math.pi * 2))
    check_angle2 = degrees(
        acos((check_side2 ** 2 + check_side3 ** 2 - check_side1 ** 2) / (2 * check_side2 * check_side3)))
    check_angle3 = 180 - (check_angle1 + check_angle2)
    triangle_sides = [check_side1, check_side2, check_side3]
    triangle_angl = [check_angle1, check_angle3, check_angle2]
    print(f"{Fore.YELLOW} ---Решение Треугольника---")
    return f" Углы: {triangle_angl} \n Стороны: {triangle_sides} \n Рещение треугольника: по двум сторонам и углу между ними"


def two_angles_one_side(check_angle2, check_angle3, check_side1):
    global triangle_angl, triangle_sides

    check_angle1 = 180 - (check_angle2 + check_angle3)
    check_side2 = (check_side1 * sin(check_angle2 / 180 * math.pi)) / sin(check_angle1 / 180 * math.pi)
    check_side3 = (check_side1 * sin(check_angle3 / 180 * math.pi)) / sin(check_angle1 / 180 * math.pi)
    triangle_angl = [check_angle1, check_angle2, check_angle3]
    triangle_sides = [check_side1, check_side2, check_side3]
    print(f"{Fore.YELLOW} ---Решение Треугольника---")
    return f" Углы: {triangle_angl} \n Стороны: {triangle_sides} \n Рещение треугольника: по двум сторонам и углу между ними"


def draw(a, b, c):
    global triangle_sides, a_canvas_lbl, b_canvas_lbl, c_canvas_lbl, AB_value_lbl, BC_value_lbl, AC_value_lbl
    try:
        c_canvas_lbl.destroy()
        a_canvas_lbl.destroy()
        b_canvas_lbl.destroy()
        AB_value_lbl.destroy()
        BC_value_lbl.destroy()
        AC_value_lbl.destroy()
    except NameError:
        pass

    a_canvas_lbl = Label(canvas, text="A", fg="#E98176", bg="white", font=('Comics 16 bold'))
    b_canvas_lbl = Label(canvas, text="B", fg="#E98176", bg="white", font=('Comics 16 bold'))
    c_canvas_lbl = Label(canvas, text="C", fg="#E98176", bg="white", font=('Comics 16 bold'))

    AB_value_lbl = Label(canvas,text=f"{round(triangle_sides[0],4)}", fg="#E98176", bg="#FFF", font=('Comics 11 bold'))
    BC_value_lbl = Label(canvas, text=f"{round(triangle_sides[1],4)}", fg="#E98176", bg="#FFF", font=('Comics 11 bold'))
    AC_value_lbl = Label(canvas, text=f"{round(triangle_sides[2],4)}", fg="#E98176", bg="#FFF", font=('Comics 11 bold'))

    font = ImageFont.truetype('times.ttf', 12)
    lenth_side1 = font.getlength(f'{round(triangle_sides[0],4)}')
    lenth_side2 = font.getlength(f'{round(triangle_sides[1],4)}')
    lenth_side3 = font.getlength(f'{round(triangle_sides[2],4)}')

    hc = (2 * (a ** 2 * b ** 2 + b ** 2 * c ** 2 + c ** 2 * a ** 2) - (a ** 4 + b ** 4 + c ** 4)) ** 0.5 / (2. * c)
    dx = (b ** 2 - hc ** 2) ** 0.5
    if abs((c - dx) ** 2 + hc ** 2 - a ** 2) > 0.01:
        dx = -dx
    scale_point = 230 / max(triangle_sides)
    coords = [60, 50, c * scale_point + 60, 50, abs(dx) * scale_point + 60, hc * scale_point + 50]

    AC_value_lbl.place(x=0.5 * (coords[0] + coords[2]) - lenth_side1, y=5)
    AB_value_lbl.place(x=0.5 * (coords[2] + coords[4]) + lenth_side2, y=0.5 * (coords[3] + coords[5]) - 11)
    BC_value_lbl.place(x=0.5 * (coords[4] + coords[0]) - (lenth_side3 + 35), y=0.5 * (coords[5] + coords[1]) - 11)

    c_canvas_lbl.place(x=40, y=25)
    a_canvas_lbl.place(x=c * scale_point + 70, y=25)
    b_canvas_lbl.place(x=abs(dx) * scale_point + 50, y=hc * scale_point + 55)

    canvas.create_polygon(*coords, fill="#FFF", outline="#E98176", width=3)

def clear():
    side1.delete(0, END)
    side2.delete(0, END)
    side3.delete(0, END)

    angle1.delete(0, END)
    angle2.delete(0, END)
    angle3.delete(0, END)


def getter():
    global count, triangle_sides,triangle_angl,triangle_find,files_count
    widget = canvas
    if triangle_find is True:
        file_name = r"images_triangle\Triangle with" + f" sides(AB({round(triangle_sides[0], 2)}), BC({round(triangle_sides[1], 2)}), AC({round(triangle_sides[2], 2)});" \
                                                        f" angl(∠A({round(triangle_angl[0],2)}), ∠B({round(triangle_angl[1],2)}), ∠C({round(triangle_angl[2],2)})).png"

        pil.ImageGrab.grab(bbox=(
            widget.winfo_rootx(),
            widget.winfo_rooty(),
            widget.winfo_rootx() + widget.winfo_width() - 40,
            widget.winfo_rooty() + widget.winfo_height()
        )).save(file_name)
        lst = os.listdir(r"images_triangle")
        number_files = len(lst)
        if number_files > files_count:
            print(f"{Fore.CYAN} Изображение сохранено в папку images_triangle")
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            print("------------------------------------------------------------")
            files_count = number_files

    elif triangle_find is False:
        area_lbl['text'] = "Невозможно сохранить файл \n (треугольник не найден)"
        print(f"{Fore.RED} Error5: Невозможно сохранить файл (треугольник не найден)")
        print("------------------------------------------------------------")


triangle_find = False
files_count = 0
main = Tk()
main.geometry('720x480')
main.config(bg="#ECE3DC")
main.resizable(width=False, height=False)
main.iconbitmap('icon_triangle.ico')
main.title("Расчёт площади треугольника")
main_lbl = Label(main, text=" Площадь треугольника", font=('Comics 22 bold'), bg="#ECE3DC", fg="#E98176")
main_lbl.place(x=150, y=20)
colorama.init(autoreset=True)
tprint("Triangle Area", chr_ignore=True)

ab = Label(main, text="AB", font=('Comics 16 bold'), bg="#ECE3DC", fg="#E98176")
bc = Label(main, text="BC", font=('Comics 16 bold'), bg="#ECE3DC", fg="#E98176")
ac = Label(main, text="AC", font=('Comics 16 bold'), bg="#ECE3DC", fg="#E98176")

angle_a = Label(main, text="∠A", font=('Comics 16 bold'), bg="#ECE3DC", fg="#E98176")
angle_b = Label(main, text="∠B", font=('Comics 16 bold'), bg="#ECE3DC", fg="#E98176")
angle_c = Label(main, text="∠C", font=('Comics 16 bold'), bg="#ECE3DC", fg="#E98176")

ab.grid(column=0, row=0, pady=(160, 0), padx=8)
bc.grid(column=0, row=1, pady=(0, 0), padx=8)
ac.grid(column=0, row=2, pady=(0, 0), padx=8)

angle_a.grid(column=0, row=3, pady=(40, 0), padx=8)
angle_b.grid(column=0, row=4, pady=(0, 0), padx=8)
angle_c.grid(column=0, row=5, pady=(0, 0), padx=8)

combobox_lbl = Label(main, text="Точность введенных данных:", font=('Comics 12 bold'), bg="#ECE3DC", fg="#E98176")
combobox_lbl.place(x=0, y=95)

round_lst = ["до целых", "до десятых", "до сотых", "до тысячных"]
default_round = StringVar(value=round_lst[1])
round_combobox = Combobox(main, values=round_lst, width=25, height=20, textvariable=default_round,
                              font=('Comics 10 bold'), foreground="#E98176")
round_combobox.set(round_lst[1])
round_combobox.place(x=5, y=125)
main.option_add('*TCombobox*Listbox.font', ('Comics 10 bold'))
main.option_add('*TCombobox*Listbox.foreground' % main, "#E98176")

side1 = Entry(main, bg='#fff', foreground="#FFB8A6", font=('Comics 16 bold'), width=6)
side2 = Entry(main, bg='#fff', foreground="#FFB8A6", font=('Comics 16 bold'), width=6)
side3 = Entry(main, bg='#fff', foreground="#FFB8A6", font=('Comics 16 bold'), width=6)

angle1 = Entry(main, bg='#fff', foreground="#FFB8A6", font=('Comics 16 bold'), width=6)
angle2 = Entry(main, bg='#fff', foreground="#FFB8A6", font=('Comics 16 bold'), width=6)
angle3 = Entry(main, bg='#fff', foreground="#FFB8A6", font=('Comics 16 bold'), width=6)

side1.grid(column=1, row=0, pady=(160, 0))
side2.grid(column=1, row=1)
side3.grid(column=1, row=2)

angle1.grid(column=1, row=3, pady=(40, 0))
angle2.grid(column=1, row=4)
angle3.grid(column=1, row=5)

result = Button(main, text="Расчитать", font=('Comics 16 bold'), bd=0, fg="#E98176", command=calculation)
result.place(x=10, y=430)

canvas = Canvas(main, width=430, height=320, bg="white", highlightthickness=0)
canvas.place(x=260, y=90)

save_image = PhotoImage(file="save_image123.png")
save_button = Button(main, image=save_image, command=getter)
save_button.place(x=650, y=370)

area_lbl = Label(main, text="", font=('Comics 16 bold'), bg="#ECE3DC", fg="#E98176")
area_lbl.place(x=360, y=420)

clear_button = Button(main, text="Очистить", font=('Comics 16 bold'), bd=0, fg="#E98176", command=clear)
clear_button.place(x=140, y=430)

main.mainloop()

triangle_images = glob.glob('images_triangle/*')
for t in triangle_images:
    os.remove(t)