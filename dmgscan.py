import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageGrab
import os
import sys

class DamageScan(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.wm_attributes("-topmost", 1)
        self.InitUI()
        self.loaded = 0
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.dmg_h = 0
        self.dmg_l = 0
        self.rng_c = 0
        self.rng_l = 0
        self.dmg_ratio = 0
        self.rng_ratio = 0

    def ResourcePath(self, relative):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative)

    def InitUI(self):
        #self.icon_path = self.ResourcePath("icon.ico")
        #self.parent.wm_iconbitmap(self.icon_path)

        self.button_scan = tk.Button(
            self.master,
            command = self.OnScanButtonClick,
            text = "Scan"
        )
        self.button_scan.place(
            x=14, y=10, width=50,height=40
        )

        self.checkvar_ontop = tk.IntVar()
        self.checkvar_ontop.set(1)
        self.checkbutton_ontop = tk.Checkbutton(
            self.master,
            text = "On Top",
            variable = self.checkvar_ontop,
            command = self.OnTopButtonClick
        )
        self.checkbutton_ontop.place(
            x=5, y=51
        )

        self.frame_heavyset = tk.Frame(
            self.master,
            width = 300,
            height = 60,
            #relief = 'solid',
            #bd = 1
        )
        self.frame_heavyset.place(
            x=90,y=3
        )

        self.frame_heavyset_pic = tk.Frame(
            self.frame_heavyset,
            width=150,
            height=25
        )
        self.frame_heavyset_pic.place(
            x=73,y=10
        )

        self.frame_heavyset_num = tk.Frame(
            self.frame_heavyset,
            width=180,
            height=27,
        )
        self.frame_heavyset_num.place(
            x=0,y=30
        )

        self.label_damage = tk.Label(
            self.frame_heavyset,
            anchor = 'e',
            text = 'N/A d'
        )
        self.label_damage.place(
            x=190, y=37
        )

        self.label_range = tk.Label(
            self.frame_heavyset,
            anchor = 'e',
            text = 'N/A m'
        )
        self.label_range.place(
            x=190, y=17
        )

        self.label_pic_n = tk.Label(
            self.frame_heavyset_pic,
            anchor = 'center',
            text = 'N'
        )
        self.label_pic_n.place(
            x=0,y=0
        )

        self.label_pic_b = tk.Label(
            self.frame_heavyset_pic,
            anchor = 'center',
            text ='B'
        )
        self.label_pic_b.place(
            x=28,y=0
        )


        self.label_pic_s = tk.Label(
            self.frame_heavyset_pic,
            anchor = 'center',
            text = 'S'
        )
        self.label_pic_s.place(
            x=57,y=0
        )

        self.label_pic_g = tk.Label(
            self.frame_heavyset_pic,
            anchor = 'center',
            text = 'G'
        )
        self.label_pic_g.place(
            x=86,y=0
        )

        self.canvas_graph = tk.Canvas(
            self.master,
            width = 370,
            height = 200,
            relief = "solid",
            cursor = "plus",
            bd = 1,
        )
        self.canvas_graph.place(
            x=0,y=75,width=370,height=200
        )
        self.canvas_graph.bind('<Motion>', self.MouseOnGraph)

        self.label_hs = tk.Label(
            self.frame_heavyset_num,
            text='Heavy Set',
        )
        self.label_hs.place(
            x=0,y=0, height =25
        )

        self.label_nohs = tk.Label(
            self.frame_heavyset_num,
            text='0',
            bg='#035003',
            fg='#E0E0E0',
            highlightcolor = '#303030',
            relief = 'solid',
            borderwidth = 1
        )
        self.label_nohs.place(
            x=65,y=0,width=30,height=25
        )

        self.label_bhs = tk.Label(
            self.frame_heavyset_num,
            text='0',
            bg='#035003',
            fg='#E0E0E0',
            highlightcolor = '#303030',
            relief = 'solid',
            borderwidth = 1
        )
        self.label_bhs.place(
            x=94,y=0,width=30,height=25
        )

        self.label_shs = tk.Label(
            self.frame_heavyset_num,
            text='0',
            bg='#035003',
            fg='#E0E0E0',
            highlightcolor = '#303030',
            relief = 'solid',
            borderwidth = 1
        )
        self.label_shs.place(
            x=123,y=0,width=30,height=25
        )

        self.label_ghs = tk.Label(
            self.frame_heavyset_num,
            text='0',
            bg='#035003',
            fg='#E0E0E0',
            highlightcolor = '#303030',
            relief = 'solid',
            borderwidth = 1
        )
        self.label_ghs.place(
            x=152,y=0,width=30,height=25
        )

    def MouseOnGraph(self, event):
        #print('{}, {}'.format(event.x, event.y))
        if not (self.loaded):
            return
        x = event.x
        y = event.y
        self.DrawVerticalLine(x, y, self.canvas_graph)
        
    def DrawVerticalLine(self, x, y, canvas):
        canvas.delete('vline')
        width = int(canvas["width"])
        height = int(canvas["height"])
        canvas.create_line(
            x,0,
            x,height,
            fill="#353535",
            tag='vline'
        )
        # where is the x?
        if (x <= self.x1):
            sx = x
            sy = self.y1
        elif ((x > self.x1) and (x <= self.x2)):
            sx = x
            sy = ((self.y2 - self.y1)/(self.x2 - self.x1)*(x - self.x1) + self.y1)
        else:
            sx = x
            sy = self.y2
        canvas.create_rectangle(
            sx+3, sy+3,
            sx-3, sy-3,
            fill = "#ff0000",
            tag='vline'
        )
        if (x >= (width - 50)):
            ta = "e"
            px = -5
        else:
            ta = "w"
            px = 5
        
        if (sy < height/3):
            py_1 = 10
            py_2 = 22
            ta = "e"
            px = -5
        else:
            py_1 = -22
            py_2 = -10
        
        if (x < 50):
            ta = 'w'
            px = 5

        canvas.create_text(
            sx+px, sy+py_1,
            anchor = ta,
            fill = "#B6EBA0",
            font = ("Arial", 10,'bold'),
            text = "{}{}".format(str(round((height - sy)/self.dmg_ratio, 1)), ' d'),
            tag='vline'
        )
        canvas.create_text(
            sx+px, sy+py_2,
            anchor = ta,
            fill = "#B6EBA0",
            font = ("Arial", 10, 'bold'),
            text = "{}{}".format(str(round(x/self.rng_ratio, 1)), ' m'),
            tag='vline'
        )

        #calculate heavy set damage and apply changes
        dmg = (height-sy)/self.dmg_ratio
        rng = x/self.rng_ratio
        dmg_b = dmg*0.95
        dmg_s = dmg*0.9
        dmg_g = dmg*0.85
        
        shot_n = int(100/dmg) + 1
        shot_b = int(100/dmg_b) + 1
        shot_s = int(100/dmg_s) + 1
        shot_g = int(100/dmg_g) + 1
        self.ChangeColor(self.label_nohs, shot_n)
        self.ChangeColor(self.label_bhs, shot_b)
        self.ChangeColor(self.label_shs, shot_s)
        self.ChangeColor(self.label_ghs, shot_g)
        self.ChangeData(self.label_damage, round(dmg,1))
        self.ChangeData(self.label_range, round(rng,1))

    def ChangeColor(self, label, shot):
        label['text'] = str(shot)
        # Colors
        # #035003
        # #023402
        # #805009
        # #573401
        # #773708
        # #701B1B
        # #5B1314
        if (shot == 1):
            label['bg'] = '#035003'
        elif ((shot >= 2) and (shot <= 3)):
            label['bg'] = '#023402'
        elif (shot == 4):
            label['bg'] = '#805009'
        elif (shot == 5):
            label['bg'] = '#701B1B'
        else:
            label['bg'] = '#5B1314'

    def ChangeData(self, label, data):
        text = label['text']
        label['text'] = '{} {}'.format(data,text[-1])

    def OnScanButtonClick(self):
        self.loaded = 0
        img = self.CaptureImage()
        data = self.ScanImage(img)
        self.ClearCanvas(self.canvas_graph)
        self.DrawGraph(self.canvas_graph, data)

    def OnTopButtonClick(self):
        if (self.checkvar_ontop.get()):
            #print("ON")
            self.parent.wm_attributes("-topmost", 1)
        else:
            #print("OFF")
            self.parent.wm_attributes("-topmost", 0)

    def CaptureImage(self):
        img = ImageGrab.grab()
        width, height = img.size
        crop_size = (
            786/1920 * width,
            552/1080 * height,
            1191/1920 * width,
            729/1080 * height
        )
        img = img.crop(
            crop_size
        )
        #save result for debugging
        #img.save("temp.png")
        return img

    def ScanImage(self, img):
        width, height = img.size
        width = width - 1
        height = height - 1
        print(img.size)
        px = img.load()

        # Check if the weapon is modded
        modded = 0
        for y in reversed(range(height)):
            if (
                (px[width,y][0], px[width,y][1], px[width,y][2])
                ==
                (248,177,51)
            ):
                modded = 1
                print("Modded")
                break
        
        # Check the weapon type
        px_type = None
        for y in range(height):
            if (
                px[width,y][0] - px[width,y+1][0] > 5 and
                px[width,y][1] - px[width,y+1][1] > 5 and
                px[width,y][2] - px[width,y+1][2] > 5
            ):
                px_type = y+1
                print(px_type)
                break
        if (px_type == None):
            print("no graph found.")
            return (None, None, None, None, None)

        if (
            (px_type <= 28/(177 / (height+1))+1)
            and
            (px_type >= 28/(177 / (height+1))-1)
        ):
            weapon_type = 0
        elif (
            (px_type <= 65/(177 / (height+1)) + 1)
            and
            (px_type >= 65/(177 / (height+1)) - 1)
        ):
            weapon_type = 1
        else:
            weapon_type = 2
        # Types:
        # SMG/HG    0
        # SA/AR     1
        # BA/MG     2

        # Scan highest damage and closest range
        if (modded):
            graph_rgb = (248,177,51)
        else:
            graph_rgb = (138,198,235)

        damage_h = None
        range_c = None
        for x in range(width):
            if (damage_h is not None):
                break
            for y in reversed(range(height)):
                if (px[x,y] == graph_rgb):
                    if not (px[x,y-1] == graph_rgb):
                        if not (px[x+1,y] == graph_rgb):
                            damage_h = y+1
                            range_c = x
                            break
                        else:
                            break

        #Scan lowest damage and longest range
        damage_l = None
        range_l = None
        for x in reversed(range(width)):
            if (damage_l is not None):
                break
            for y in reversed(range(height)):
                if (px[x,y] == graph_rgb):
                    if not (px[x-1,y] == graph_rgb):
                        damage_l = y-1
                        range_l = x
                        break
                    else:
                        break

        if (
            (damage_h == None) or
            (damage_l == None) or
            (range_c == None) or
            (range_l == None)
        ):
            print("No data found")
            return (None, None, None, None, None)

        #calculate actual damage and range from pixel's x,y
        # BA Px per dmg = 1.36
        # SMG px per dmg = 2.96
        # SA px per dmg = 2.2
        if (weapon_type == 0):
            dmg_ratio = float(50 / (148/177 * (height+1)))
        elif (weapon_type == 1):
            dmg_ratio = float(25 / (55/177 * (height+1)))
        else:
            dmg_ratio = float(100 / (136/177 * (height+1)))
        damage_h = height + 1 - damage_h
        damage_l = height + 1 - damage_l
        damage_h = float(damage_h * dmg_ratio)
        damage_l = float(damage_l * dmg_ratio)

        rng_ratio = float(50 / (202/405 * (width+1)))
        if (weapon_type == 1):
            rng_ratio = rng_ratio * 3
        elif (weapon_type == 2):
            rng_ratio = rng_ratio * 10
        range_c = float(range_c * rng_ratio)
        range_l = float(range_l * rng_ratio)

        self.dmg_h = damage_h
        self.dmg_l = damage_l
        self.rng_c = range_c
        self.rng_l = range_l
        
        data = (weapon_type, damage_h, damage_l, range_c, range_l)
        print(data)
        return data

    def ClearCanvas(self, canvas):
        width = float(canvas["width"])
        height = float(canvas["height"])
        canvas.delete('all')
        canvas.configure(bg="#151515")
        #vertical lines
        canvas.create_line(
            1/4*width,0,1/4*width,height,
            fill = "#090909"
        )
        canvas.create_line(
            1/2*width,0,1/2*width,height,
            fill = "#090909"
        )
        canvas.create_line(
            3/4*width,0,3/4*width,height,
            fill = "#090909"
        )
        #horizontal line
        canvas.create_line(
            0,1/3*height,width,1/3*height,
            fill = "#090909"
        )
        canvas.create_line(
            0,2/3*height,width,2/3*height,
            fill = "#090909"
        )

    def DrawGraph(self, canvas, data):
        width = float(canvas["width"])
        height = float(canvas["height"])
        for dat in data:
            if (dat == None):
                canvas.create_text(
                    1/2*width, 1/2*height,
                    text="No data found",
                    font=("Arial", 20),
                    fill = "#ff0000"
                )
                return

        wpn_type = data[0]
        dmg_h = data[1]
        dmg_l = data[2]
        rng_c = data[3]
        rng_l = data[4]

        #graph texts
        if (wpn_type == 0):
            dmg_ratio = (2/3*height) / 50
            rng_ratio = (3/4*width) / 75
            v1 = "25m"
            v2 = "50m"
            v3 = "75m"
            h1 = "25"
            h2 = "50"
        elif (wpn_type == 1):
            dmg_ratio = (2/3*height) / 50
            rng_ratio = (3/4*width) / 225
            v1 = "75m"
            v2 = "150m"
            v3 = "225m"
            h1 = "25"
            h2 = "50"
        else:
            dmg_ratio = (2/3*height) / 100
            rng_ratio = (3/4*width) / 750
            v1 = "250m"
            v2 = "500m"
            v3 = "750m"
            h1 = "50"
            h2 = "100"

        canvas.create_text(
            1/4*width,height-10,
            text = v1,
            font = ("Arial", 10),
            fill = "#00ff00"
        )
        canvas.create_text(
            1/2*width,height-10,
            text = v2,
            font = ("Arial", 10),
            fill = "#00ff00"
        )
        canvas.create_text(
            3/4*width,height-10,
            text = v3,
            font = ("Arial", 10),
            fill = "#00ff00"
        )
        canvas.create_text(
            12,1/3*height,
            text= h2,
            font = ("Arial", 10),
            fill = "#00ff00"
        )
        canvas.create_text(
            12,2/3*height,
            text= h1,
            font = ("Arial", 10),
            fill = "#00ff00"
        )

        #Draw actual graph
        canvas.create_line(
            0,(height - dmg_h*dmg_ratio),
            rng_c*rng_ratio, (height - dmg_h*dmg_ratio),
            rng_l*rng_ratio, (height - dmg_l*dmg_ratio),
            width, (height - dmg_l*dmg_ratio),
            fill = "#ff0000"
        )
        self.dmg_ratio = dmg_ratio
        self.rng_ratio = rng_ratio
        self.x1 = rng_c*rng_ratio
        self.x2 = rng_l*rng_ratio
        self.y1 = (height - dmg_h*dmg_ratio)
        self.y2 = (height - dmg_l*dmg_ratio)
        self.loaded = 1

def main():
    root = tk.Tk()
    root.geometry("370x275")
    root.title("H&G Damage Scanner")
    root.resizable(0,0)
    app = DamageScan(root)
    root.mainloop()

if __name__ == "__main__":
    main()