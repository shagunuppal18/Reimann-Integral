# %matplotlib widget
from tkinter import *
from PIL import Image, ImageTk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, TextBox
import numpy as np

root = Tk()
root.title("INSTRUCTIONS")
root.geometry("200x200")
root.configure(background = "black")

logo = Image.open('Instructions.png')
logo = ImageTk.PhotoImage(logo)
logo_label = Label(image=logo)
logo_label.image = logo
logo_label.pack(side= LEFT, padx = 40, pady =30)

nb_subdivisions = 10
intervall_start = 0
intervall_end = 0

class f:
    def __init__(self, expression, value, x):
        self.expression = expression
        self.value = value
        self.x = x
    
    def Calculate(self, expression):
        self.value = eval(expression)

class Rectangle:
    def __init__(self, x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4, area, type):
        self.x_1 = x_1
        self.y_1 = y_1
        self.x_2 = x_2
        self.y_2 = y_2
        self.x_3 = x_3
        self.y_3 = y_3
        self.x_4 = x_4
        self.y_4 = y_4
        self.area = area
        self.type = type

def Init_Rectangle(subdivision_start, subdivision_end, type, function):
    rectangle = Rectangle(0, 0, 0, 0, 0, 0, 0, 0, 0, type)

    rectangle.x_4 = subdivision_start
    rectangle.x_1 = subdivision_start
    rectangle.x_2 = subdivision_end
    rectangle.x_3 = subdivision_end

    #create linspace of the subdivision
    subdivision_linespace = np.linspace(subdivision_start,subdivision_end,100)
    function.x = subdivision_linespace
    function.Calculate(function.expression)
    y = function.value
    if type == "small":
        #find the smallest value of the function over the subdivision
        y_ = np.amin(y)
    else:
        y_ = np.amax(y)

    rectangle.y_1 = y_
    rectangle.y_2 = y_
    rectangle.y_3 = 0
    rectangle.y_4 = 0    
    #calculate the area of the rectangle
    rectangle.area = y_ * (subdivision_end-subdivision_start)

    return rectangle

def Draw_Rectangle(rectangle):

    subdivison_linespace = np.linspace(rectangle.x_1, rectangle.x_2, 100)
    y = np.linspace(rectangle.y_1, rectangle.y_2, 100)
    
    if rectangle.type == "small":
        y_ = np.amin(y)
        color = "blue"
    else:
        y_ = np.amax(y)
        color = "red"

    #fill the area of the rectangle
    axes.fill_between(subdivison_linespace, y, color=color, alpha=0.3)

def Intervall_to_Subdivisions(intervall_start, intervall_end, nb_subdivisions):
    tmp_subdivisons = []
    for i in range(0, nb_subdivisions+1):
        try:
            tmp = i*((intervall_end-intervall_start)/nb_subdivisions) + intervall_start
        except:
            return []
        tmp_subdivisons.append(tmp)
    subdivisions = np.array(tmp_subdivisons)
    # print(tmp_subdivisons);
    return subdivisions

def Rectangles_over_Subdivions(subdivisions, function):
    rectangles = []
    for i in range(0, len(subdivisions)-1):
        small_rectangle = Init_Rectangle(subdivisions[i], subdivisions[i+1], "small", function)
        big_rectangle = Init_Rectangle(subdivisions[i], subdivisions[i+1], "big", function)
        rectangles.append(small_rectangle)
        rectangles.append(big_rectangle)
    # print(rectangles)
    return rectangles

def Subdivisons_to_Values(rectangles, function):

    tmp_y_data_s = []
    tmp_y_data_b = []

    for i in range(0, len(rectangles)):
        if rectangles[i].type == "small":
            tmp_y_data_s.append(np.linspace(rectangles[i].y_1, rectangles[i].y_2, 100))
        else:
            tmp_y_data_b.append(np.linspace(rectangles[i].y_1, rectangles[i].y_2, 100))

    y_data_s = []
    y_data_b = []

    for i in range(0, len(tmp_y_data_s)):
        for j in range(0, len(tmp_y_data_s[i])):
            y_data_s.append(tmp_y_data_s[i][j])

    for i in range(0, len(tmp_y_data_b)):
        for j in range(0, len(tmp_y_data_b[i])):
            y_data_b.append(tmp_y_data_b[i][j])
    
    return (y_data_s, y_data_b)

def Update_Plot(function, nb_subdivisons, intervall_start, intervall_end):
    axes.collections.clear()
    #update the rectagnles
    small_area = 0
    big_area = 0

    subdivisions = Intervall_to_Subdivisions(intervall_start, intervall_end, nb_subdivisons)
    rectangles = Rectangles_over_Subdivions(subdivisions, function)
    for rectangle in rectangles:
        Draw_Rectangle(rectangle)
        if(rectangle.type == "small"):
            small_area += rectangle.area
        else:
            big_area += rectangle.area

    area = "Small Area {}\nBig Area {}".format(small_area, big_area)

    y_data_s, y_data_b = Subdivisons_to_Values(rectangles, function)

    # print("ydataS", y_data_s)
    # print(area);

    x = np.linspace(intervall_start, intervall_end, len(y_data_s))

    l_s.set_xdata(x)
    l_s.set_ydata(y_data_s)
    l_b.set_xdata(x)
    l_b.set_ydata(y_data_b)

    #Update the function
    # function.x = np.linspace(-10, 10, len(y_data_s))
    function.Calculate(function.expression)
    l_1.set_ydata(function.value)
    l_1.set_xdata(function.x)

    # print(y_data_b[1], y_data_b[-1]);
    axes.set_xlim([cursor_start.val-5, cursor_stop.val+5])    # change
    axes.set_ylim([y_data_s[0]-max(5,(y_data_s[0]/4)), y_data_b[-1]+max(5,y_data_b[-1]/4)])

    text_area.set_text(area)
    figure.canvas.draw()
    figure.canvas.flush_events()


#Draw the function

figure, axes = plt.subplots()

x = np.linspace(-10, 10, 100)
function = f("self.x**3", 0, x)
function.Calculate(function.expression)
y = function.value

axamp = plt.axes([0.25, .03, 0.50, 0.02])
axbox = plt.axes([0.25, .9, 0.25, 0.05])
ax_intervall_start = plt.axes([0.6, .9, 0.10, 0.05])
ax_intervall_stop = plt.axes([0.8, .9, 0.10, 0.05])

# def update_cursor(number):

#     return number*number;

text_box = TextBox(axbox, 'Function', initial="", color = "#eeeeee")
samp = Slider(axamp, 'Numbers', 0, 1200, valinit=0, valstep=1, color = "#00adb5")

# slider = widgets.IntSlider(
#     value=0,
#     min=-10,
#     max=10,
#     step=1,
#     description='Test:',
#     disabled=False,
#     continuous_update=False,
#     orientation='horizontal',
#     readout=True,
#     readout_format='d'
# )

# widgets.interact(update_cursor, number = slider)


cursor_start = Slider(ax_intervall_start, 'Start', -10, 10, valinit = 0, valstep=1, color = "#00adb5");
cursor_stop = Slider(ax_intervall_stop, 'Stop', -10, 10, valinit = 0, valstep=1, color = "#00adb5");


small_area = 0
big_area = 0
subdivisions = Intervall_to_Subdivisions(intervall_start, intervall_end, nb_subdivisions)
rectangles = Rectangles_over_Subdivions(subdivisions, function)
# axes.set_xlim([cursor_start.val, cursor_stop.val])
axes.set_xlim([-10, 10])
axes.set_ylim([-10, 10])
# axes.set_ylim([cursor_start.val, cursor_stop.val])
axes.grid()
axes.set_ylabel('f(x)')
axes.set_xlabel('x')

y_data_s, y_data_b = Subdivisons_to_Values(rectangles, function)
l_1, = plt.plot(x, y, label='quadratic')
x = np.linspace(-5, 5, 1000)
for rectangle in rectangles:
    Draw_Rectangle(rectangle)
    if(rectangle.type == "small"):
        small_area += rectangle.area
    else:
        big_area += rectangle.area

l_s, = plt.plot(x, y_data_s, 'b')
l_b, = plt.plot(x, y_data_b, 'r')

area = "Small Area {}\nBig Area {}".format(small_area, big_area)


figure.canvas.draw()
small_area = 0
big_area = 0
area = "Small Area {}\nBig Area {}".format(small_area, big_area)
props = dict(boxstyle='round', facecolor='#393e46', alpha=0.5)
text_area = axes.text(0.05, 0.95, area, transform=axes.transAxes, fontsize=14, verticalalignment='top', bbox=props)

def update_start(val):
    global intervall_start
    intervall_start = cursor_start.val
    Update_Plot(function, nb_subdivisions, intervall_start, intervall_end)

def update_end(val):
    global intervall_end
    intervall_end = cursor_stop.val
    Update_Plot(function, nb_subdivisions, intervall_start, intervall_end)

def update_subdivisions(val):
    global nb_subdivisions 
    nb_subdivisions = samp.val
    Update_Plot(function, nb_subdivisions, intervall_start, intervall_end)

def submit(text):
    #Update the function
    text = text.replace("x", "self.x")
    function.expression = text
    Update_Plot(function, nb_subdivisions, intervall_start, intervall_end)

    
samp.on_changed(update_subdivisions)
cursor_start.on_changed(update_start)
cursor_stop.on_changed(update_end)
text_box.on_submit(submit)
plt.show()

# X = 10*np.random.rand(5,3)
# plt.imshow(X, aspect='auto')



root.mainloop()