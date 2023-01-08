#!/usr/bin/python3

# # Imports # #
from typing import Optional
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from scipy.ndimage import zoom


class ImgCanvas(tk.Canvas):
    """Canvas to draw image for color selection and displaying results"""
    verbose: bool
    debug: bool

    display_img: Optional[np.array]  # # probably not needed # #
    scale_img: Optional[np.array]  # # probably not needed (maybe return from function?) # #
    tk_img: Optional[ImageTk.PhotoImage]  # Current image in canvas

    def __init__(self, master: Optional[tk.Frame] = None,
                 width: int = 400, height: int = 400,
                 verbose: bool = False, debug: bool = False):
        # Initialize tk.Canvas
        super().__init__(master)
        self.master = master

        self.verbose = verbose
        self.debug = debug

        # Add callbacks for user inputs
        self.bind('<Button-1>', self.pressed)
        self.bind('<B1-Motion>', self.drag)
        self.bind('<ButtonRelease-1>', self.released)

        # set default size
        self.configure(width=width, height=height)
        
        # save currently displayed image data
        self.display_img = None
        self.scale_img = None
        self.tk_img = None

    def pressed(self, event):
        """Callback for Clicking on Image"""
        app = self.master

        if self.debug:
            print('\t\t', 'Button 1 pressed:', event)

        # Start Oval Selection
        if app.color.enable:
            app.color.reset_oval()
            app.color.oval.append(self.create_oval(event.x, event.y, event.x, event.y))
            app.color.oval.append(event.x)
            app.color.oval.append(event.y)
            app.color.oval.append(0)  # initial radius

            if self.debug:
                print('\t\t', 'Color Oval:', app.color.oval)

    def drag(self, event):
        """Callback for dragging on Image"""
        app = self.master

        if app.color.enable:
            # Calculate radius from original position
            app.color.oval[3] = round(((event.x - app.color.oval[1]) ** 2 + (event.y - app.color.oval[2]) ** 2) ** 0.5)
            if self.debug:
                print('\t\t', 'Color Oval Radius:', app.color.oval[3])

            # Redraw color oval
            self.coords(app.color.oval[0],                      # oval handle
                        app.color.oval[1] - app.color.oval[3],  # x1
                        app.color.oval[2] - app.color.oval[3],  # y1
                        app.color.oval[1] + app.color.oval[3],  # x2
                        app.color.oval[2] + app.color.oval[3])  # y2

    def released(self, event):
        """Callback for finishing click/drag on Image"""
        app = self.master

        if self.debug:
            print('\t\t', 'Button 1 released:', event)

        if app.color.enable:
            # Reset Color Button
            app.color.enable = False
            app.color.button.config(state=tk.NORMAL)

            if self.debug:
                print('\t\t', 'Color Oval:', app.color.oval)

            self.get_color()

    def get_color(self):
        """Get average color inside selected oval"""
        app = self.master

        if type(app.img) is np.ndarray and app.img.size > 1:
            # calculate selection on original image size
            x = int(float(app.color.oval[1]) / app.scale_factor)
            y = int(float(app.color.oval[2]) / app.scale_factor)
            r = int(float(app.color.oval[3]) / app.scale_factor)

            # make mask
            y_grid, x_grid = np.ogrid[-r:r + 1, -r:r + 1]
            mask = x_grid * x_grid + y_grid * y_grid <= r * r

            y_min = y - r
            y_max = y + r + 1
            x_min = x - r
            x_max = x + r + 1
            
            # clip mask to fit within image
            if y_min < 0:
                mask = mask[-y_min:,:]
                y_min = 0;
            if y_max > app.img.shape[0]:
                mask = mask[:app.img.shape[0]-y_max,:]
                y_max = app.img.shape[0];
            if x_min < 0:
                mask = mask[:, -x_min:]
                x_min = 0;
            if x_max > app.img.shape[1]:
                mask = mask[:, :app.img.shape[1]-x_max]
                x_max = app.img.shape[1];
            
            if self.debug:
                print('\t\t', 'Color Mask:', x, y, r)
                print('\t\t', 'Color Mask:', mask)
                print('\t\t', 'Color Mask:', mask.shape)
                print('\t\t', 'Color Mask:', 'Mask Bounds:', [y_min, y_max, x_min, x_max])
                print('\t\t', 'Color Mask:', 'Image Bounds:', app.img.shape)

            # get average of color over mask
            img_area = app.img[y_min:y_max, x_min:x_max, :]
            color = [img_area[mask, 0].mean(),
                     img_area[mask, 1].mean(),
                     img_area[mask, 2].mean()]

            if self.verbose or self.debug:
                print('Color Selector:\t', color)

            # maybe everything after this should be moved out of Canvas Class...

            # write color values to color entries
            for idx, rgb in enumerate(app.color.rgb):
                rgb.entry.delete(0, 'end')
                rgb.entry.insert(0, "{:.0f}".format(round(color[idx])))

            app.color.draw_rect(color)
            app.thresh.make_distance_img()

            if app.thresh.enable.get() == 1:
                app.thresh.process()

    def clear(self):
        """Reset canvas to default state"""
        self.delete("all")
        self.configure(width=400, height=400)

    def update_img(self, img_arr: Optional[np.array] = None):
        """Draw Image in canvas"""
        app = self.master
        
        # Clear Canvas
        self.delete("all")

        if img_arr is None:
            self.clear()
            return

        # Apply overlay (should really move this outside of ImgCanvas)
        # maybe add update_img function to main app that applies overlay and calls this function
        # could return scaled image and scale factor...
        if app.overlay.enable.get():
            self.display_img = app.overlay.add_overlay(img_arr)
        else:
            self.display_img = img_arr
        
        # Scale image to fit on screen
        self.scale_img, app.scale_factor = self.scale_image(self.display_img)
        
        # Add img to canvas
        self.tk_img = ImageTk.PhotoImage(master=self, image=Image.fromarray(self.scale_img))
        self.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        self.config(width=self.scale_img.shape[1], height=self.scale_img.shape[0])
        
        # Redraw selection circle
        # make app.color.oval an input parameter!
        # or even it's own function (duh!)
        if app.color.oval:
            self.delete(app.color.oval[0])
            app.color.oval[0] = self.create_oval(app.color.oval[1] - app.color.oval[3],
                                                 app.color.oval[2] - app.color.oval[3],
                                                 app.color.oval[1] + app.color.oval[3],
                                                 app.color.oval[2] + app.color.oval[3])

    def scale_image(self, img_arr: np.array, scale: Optional[float] = None, max_pixels: int = 1000):
        """Scale img to fit on Screen"""
        # Set scale_factor if not passed in
        # TO DO: set max_pixels based on screen width/height https://www.geeksforgeeks.org/getting-screens-height-and-width-using-tkinter-python/
        if scale is None:
            max_dim = max(img_arr.shape[0], img_arr.shape[1])
            if max_dim > max_pixels:
                scale = max_pixels / max_dim
            else:
                scale = 1
        
        if scale != 1:
            # Calculate final Height, Width, Depth
            scale_height = int(round(float(img_arr.shape[0]) * scale))
            scale_width = int(round(float(img_arr.shape[1]) * scale))
            n = img_arr.ndim
            
            if self.verbose or self.debug:
                print("\t\t", "Scaling Image:", str(scale))

            if n > 2:
                # initialize array
                scale_img = np.zeros([scale_height, scale_width, img_arr.shape[2]])
                # zoom r,g, and b separately
                for rgb in range(img_arr.shape[2]):
                    scale_img[:, :, rgb] = zoom(img_arr[:, :, rgb], scale)
            else:
                if img_arr.dtype == bool:
                    scale_img = np.zeros(img_arr.shape)
                    scale_img[img_arr] += 255.0
                    scale_img = zoom(scale_img, scale, order=1)
                else:
                    scale_img = zoom(img_arr, scale)

            # recast to uint8 for canvas
            scale_img = scale_img.astype(np.uint8)
            
            if self.verbose or self.debug:
                print("\t\t", str(scale_img.shape))
        else:
            scale_img = img_arr
        
        return scale_img, scale
