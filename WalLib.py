from ursina import *

def is_close(number1, number2, tolerance):
    return abs(number2 - number1) <= tolerance

class Move(Entity):
    def __init__(self, object, x, y, z, speed):
        super().__init__()
        self.object = object
        self.x = x
        self.y = y
        self.z = z
        self.speed = speed


    def update(self):
        self.rx = round(self.object.x, 1)
        self.ry = round(self.object.y, 1)
        self.rz = round(self.object.z, 1)        
        if is_close(self.rx, self.x, 0.001):
            self.object.x = self.x
        if is_close(self.ry, self.y, 0.001):
            self.object.y = self.y
        if is_close(self.rz, self.z, 0.001):
            self.object.z = self.z    

        if self.object.x != self.x:
            if self.object.x < self.x:
                self.object.x += 0.1 * time.dt * self.speed
            elif self.object.x > self.x:
                self.object.x -= 0.1 * time.dt * self.speed
        if self.object.y != self.y:
            if self.object.y < self.y:
                self.object.y += 0.1 * time.dt * self.speed
            elif self.object.y > self.y:
                self.object.y -= 0.1 * time.dt * self.speed
        if self.object.z != self.z:
            if self.object.z < self.z:
                self.object.z += 0.1 * time.dt * self.speed
            elif self.object.z > self.z:
                self.object.z -= 0.1 * time.dt * self.speed

class MenuItem(Button):
    def __init__(self, parent, text, y, scale_x=0.4, scale_y=0.4, on_click=None):
        super().__init__(
            parent=parent,
            text=text,
            y=y,
            scale_x=scale_x,
            scale_y=scale_y,
            text_color=color.black,
            color=color.gray,
            highlight_color=color.rgb(r=50, g=50, b=50),
            pressed_color=color.dark_gray,
            on_click=on_click
        )

class Menu(Entity):
    def __init__(self, *button_data, spacing=-0.5, offset=0.15, scale_x=0.4, scale_y=0.4):
        super().__init__(parent=camera.ui)
        self.menu_items = []
        self.background = Entity(parent=self, z=0.1, color=color.rgb(r=50, g=50, b=50, a=120), scale=20, model='quad')

        for i, (button_text,callback) in enumerate(zip(button_data[::2], button_data[1::2])):
            menu_item = MenuItem(
                parent=self,
                text=button_text,
                y=(spacing - i * offset),
                scale_x=scale_x,
                scale_y=scale_y,
                on_click=self.handle_option_click(callback)
            )
            self.menu_items.append((menu_item))

        self.active = False

    def handle_option_click(self, callback):
        def on_click():
            try:
                if callable(callback):
                    callback()
                else:
                    print(f"Error executing logic: '{callback}' is not callable")
            except Exception as e:
                print(f"Error executing logic: {e}")

        return on_click