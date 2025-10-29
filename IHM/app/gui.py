# Interface graphique WASPStorm
# DDoS Testing Tool

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1024x728")
window.configure(bg = "#FFFFFF")
window.title("WASPStorm - DDoS Tester")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 728,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    512.0,
    364.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    112.0,
    659.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    512.0,
    149.0,
    image=image_image_3
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    205.0,
    102.22992515563965,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=52.0,
    y=84.72262573242188,
    width=306.0,
    height=33.01459884643555
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    114.0,
    71.27737045288086,
    image=image_image_4
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    668.0,
    102.22992515563965,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=515.0,
    y=84.72262573242188,
    width=306.0,
    height=33.01459884643555
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    526.0,
    69.27737045288086,
    image=image_image_5
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    205.0,
    186.62409019470215,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=52.0,
    y=169.11679077148438,
    width=306.0,
    height=33.01459884643555
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    108.0,
    154.7737274169922,
    image=image_image_6
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    67.05389785766602,
    255.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=53.624755859375,
    y=239.0,
    width=26.85828399658203,
    height=30.0
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    111.0,
    225.0,
    image=image_image_7
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    176.42914199829102,
    256.0,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=163.0,
    y=240.0,
    width=26.85828399658203,
    height=30.0
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    226.0,
    226.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    547.0,
    156.36495971679688,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    551.0,
    185.78831481933594,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    656.0,
    518.0,
    image=image_image_11
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    648.0,
    185.78831481933594,
    image=image_image_12
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    135.0,
    48.0,
    image=image_image_13
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    657.0,
    598.0,
    image=image_image_14
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    723.0,
    392.0,
    image=image_image_15
)

image_image_16 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(
    742.0,
    448.0,
    image=image_image_16
)

image_image_17 = PhotoImage(
    file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(
    700.0,
    448.0,
    image=image_image_17
)

canvas.create_text(
    761.0,
    438.0,
    anchor="nw",
    text="/",
    fill="#0021F5",
    font=("Montserrat SemiBold", 20 * -1)
)

image_image_18 = PhotoImage(
    file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(
    574.0,
    448.0,
    image=image_image_18
)

image_image_19 = PhotoImage(
    file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(
    529.0,
    448.0,
    image=image_image_19
)

canvas.create_text(
    593.0,
    438.0,
    anchor="nw",
    text="/",
    fill="#F44336",
    font=("Montserrat SemiBold", 20 * -1)
)

image_image_20 = PhotoImage(
    file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(
    911.0,
    448.0,
    image=image_image_20
)

image_image_21 = PhotoImage(
    file=relative_to_assets("image_21.png"))
image_21 = canvas.create_image(
    864.0,
    448.0,
    image=image_image_21
)

canvas.create_text(
    930.0,
    438.0,
    anchor="nw",
    text="/",
    fill="#000000",
    font=("Montserrat SemiBold", 20 * -1)
)

image_image_22 = PhotoImage(
    file=relative_to_assets("image_22.png"))
image_22 = canvas.create_image(
    405.0,
    448.0,
    image=image_image_22
)

canvas.create_text(
    424.0,
    438.0,
    anchor="nw",
    text="/",
    fill="#199E58",
    font=("Montserrat SemiBold", 20 * -1)
)

image_image_23 = PhotoImage(
    file=relative_to_assets("image_23.png"))
image_23 = canvas.create_image(
    360.0,
    448.0,
    image=image_image_23
)

image_image_24 = PhotoImage(
    file=relative_to_assets("image_24.png"))
image_24 = canvas.create_image(
    152.0,
    411.0,
    image=image_image_24
)

image_image_25 = PhotoImage(
    file=relative_to_assets("image_25.png"))
image_25 = canvas.create_image(
    98.0,
    350.0,
    image=image_image_25
)

image_image_26 = PhotoImage(
    file=relative_to_assets("image_26.png"))
image_26 = canvas.create_image(
    901.0,
    391.0,
    image=image_image_26
)

image_image_27 = PhotoImage(
    file=relative_to_assets("image_27.png"))
image_27 = canvas.create_image(
    388.0,
    350.0,
    image=image_image_27
)

image_image_28 = PhotoImage(
    file=relative_to_assets("image_28.png"))
image_28 = canvas.create_image(
    566.0,
    391.0,
    image=image_image_28
)

image_image_29 = PhotoImage(
    file=relative_to_assets("image_29.png"))
image_29 = canvas.create_image(
    396.0,
    391.0,
    image=image_image_29
)

image_image_30 = PhotoImage(
    file=relative_to_assets("image_30.png"))
image_30 = canvas.create_image(
    830.0,
    107.0,
    image=image_image_30
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat",
    bg="#1E1E3F",
    activebackground="#1E1E3F",
    cursor="hand2"
)
button_1.place(
    x=148.0,
    y=389.0,
    width=89.0,
    height=69.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat",
    bg="#1E1E3F",
    activebackground="#1E1E3F",
    cursor="hand2"
)
button_2.place(
    x=30.0,
    y=389.0,
    width=96.0,
    height=74.0
)

window.resizable(False, False)
window.mainloop()

