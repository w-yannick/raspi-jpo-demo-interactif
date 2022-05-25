from PIL import Image, ImageDraw
import cv2
import os
import math
import numpy as np
import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw

# from optimizedFilter import quantize_gray


class ImageProcessor:
    """Image acquistion and modification class

    This class manages the cv2 capture source for data acquisition and offers a variety of image filters.
    """
    FILTER_1 = {'hats': 'Chapeaux', 'hats_by_color': 'Chapeaux (par couleur)', 'blur': 'flou'}
    FILTER_2 = {'grayscale': 'gris', 'illumination': 'illumination', 'ascii': 'ascii'}

    def __init__(self, source=0):
        """Constructor

        Keyword argument:
        source -- video source path (default 0 for pi camera)
        """
        self.faceCascade = cv2.CascadeClassifier('../face_detection/data/data.xml')
        self.hats = []
        self.initHats()
        self.capture = cv2.VideoCapture(source)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FPS, 30)

    def initHats(self):
        for hat in os.listdir("../resources/hats/"):
            # self.crop_hats_image(f"../resources/hats/{hat}", Image.open(f"../resources/hats/{hat}"))
            img = Image.open(f"../resources/hats/{hat}")
            w_hat, h_hat = img.size[0], img.size[1]
            offset_x = 0
            offset_y = - h_hat
            if 'Harry' in hat:
                offset_x = -math.floor(w_hat / 4)
            elif 'Graduation' in hat:
                offset_x = -math.floor(w_hat / 4)
                offset_y += 100
            elif 'propeller' not in hat:
                offset_y += 100
            self.hats.append({'img': img, 'offset_x': offset_x, 'offset_y': offset_y})

    def read(self):
        """Acquire new image

        Returns image as numpy array
        """
        return self.capture.read()

    def __del__(self):
        """Destructor

        Releases video source
        """
        self.capture.release()

    def getResolution(self):
        """Get video source resolution

        Returns (width, height) tuple
        """
        width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return width, height

    def setResolution(self, x, y):
        """Set video source resolution

        Positional arguments:
        x -- width of the new resolution
        y -- height of the new resolution
        """
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, x)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, y)

    def setFramerate(self, framerate):
        """Set video source framerate

        Positional argument:
        framerate -- desired new frame rate
        """
        self.capture.set(cv2.CAP_PROP_FPS, framerate)

    def addPolyLogo(self, back):
        """Paste polytechnique logo on lower left corner of image

        Positional argument:
        back -- image (numpy array) on which logo will be pasted
        """
        pil_img = Image.fromarray(back)
        if (pil_img.mode == "RGB"):
            b, g, r = pil_img.split()
            pil_img = Image.merge("RGB", (r, g, b))
        else:
            pil_img = pil_img.convert('RGB')
        front = Image.open("../resources/logos/flag_polymtl2_outlined.png")
        height = pil_img.size[1] // 4
        width = int(front.size[0]/(front.size[1] / height)) #Keep the aspect ratio of the original image
        front = front.resize((width, height), Image.ANTIALIAS)
        pil_img.paste(front, (0, 3*height), front)
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGR)

    def countdown(self, frame, counter):
        """Add countdown timestamp on frame

        Positional argument:
        frame -- frame (numpy array) to be modified
        counter -- timestamp to be added to frame
        """
        width, height = self.getResolution()
        circle_position = (int(width/2), int(height/2))
        circle_color = (0, 0, 0)
        circle_radius = 100
        text_position = (int(circle_position[0]-circle_radius/2), int((circle_position[1]-circle_radius/2)+circle_radius))
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        text_color = (255, 255, 255)
        text_size = 5
        text_thickness = 7
        text_line_type = cv2.LINE_AA
        alpha = 0.7

        frame_copy = frame.copy()
        cv2.circle(frame_copy, circle_position, circle_radius, circle_color, -1)
        cv2.putText(frame_copy, str(counter), text_position, font, text_size, text_color, text_thickness, text_line_type)
        cv2.addWeighted(frame_copy, alpha, frame, 1-alpha, 0, frame)
        return frame

    def applyFilter(self, frame, effect, slider):
        """Apply specific filter at specific intensity on specific frame

        Positional arguments:
        frame -- frame (numpy array) to be modified
        effect -- name (str) of desired filter
        slider -- intensity (int) of filter
        """
        if effect == "none":
            return frame
        elif effect == "blur":
            return self.applyBlurFilter(frame, slider)
        elif effect == "grayscale":
            return self.applyGrayQuantizationFilter(frame, slider)
        elif effect == "illumination":
            return self.applyIlluminosityFilter(frame, slider)
        elif effect == "hats":
            return self.applyHats(frame, slider,hat_picker=False)
        elif effect == "hats_by_color":
            return self.applyHats(frame, slider, hat_picker=True)
        elif effect == "ascii":
            return self.applyAsciiFilter(frame,slider)
        else:
            raise ValueError("Filter does not exist!")

    def applyBlurFilter(self, frame, slider):
        """Blur frame

        Builds blend/blur kernel whose size is based on slider value

        Positional arguments:
        frame -- frame (numpy array) to be modified
        slider -- desired intensity (int) of filter
        """
        if (not 1 <= slider <= 100):
            raise ValueError("Invalid value of Blur Filter Parameters")
        # max blur intensity = 20%
        new_slider = slider * 0.2
        width, height = frame.shape[0], frame.shape[1]
        max_value = min(width, height)
        x = int((new_slider * max_value) / 100)
        if (slider == 1):
            x = 1
        return cv2.blur(frame, (x, x))

    def applyGrayQuantizationFilter(self, frame, slider):
        """ Quantize gray levels of frame

        Transforms BGR frame to grayscale. Cuts down available gray levels based on slider value.

        Maths for number of levels:
        We want exponential growth, because the effect is much more subtle at high levels, and much more drastic
        at low levels. 4 ^ 0.5 = 2 levels of gray, 4 ^ 4 = 256 levels of gray.
        So, we first transform slider input (1, 100) to an exponent value (0.5, 4),
        then round 4 ^ X to get our number of gray levels.

        Maths for quantization:
        Normalize frame values between 0 and 1, then multiply by number of gray levels wanted.
        To get back the full dynamic range (pure black/pure white), multiply these new values by 255 / n_levels.

        Positional arguments:
        frame -- frame (numpy array) to be modified
        slider -- desired intensity (int) of filter
        """
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        n_levels = round(4 ** ((slider - 1) * 0.035 + 0.5))
        # quantized = quantize_gray(frame_gray, n_levels)
        return (np.rint((frame_gray / 255) * n_levels) * (255 / n_levels)).astype(np.ubyte)

    def applyIlluminosityFilter(self, frame, slider):
        """Change frame luminosty

        Transforms BGR frame to grayscale. Scales gray values to brighten or darken frame

        Positional arguments:
        frame -- frame (numpy array) to be modfieid
        slider -- desired intensity (int) of filter
        """
        phi = slider / 10.
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame_bw * phi
        
    def applyAsciiFilter(self,frame,slider):
        """Change frame into mesmerizing ascii art

        Transforms frame in rows of text. Rows of text are then converted back to an image (numpy array)

        Positional arguments:
        frame -- frame (numpy array) to be modified
        slider -- desired intensity (int) of filter
        """

        # Credit : 
        # https://gist.github.com/cdiener/10567484
        # https://stackoverflow.com/questions/29760402/converting-a-txt-file-to-an-image-in-python

        PIXEL_ON = 0  # PIL color to use for "on"
        PIXEL_OFF = 255  # PIL color to use for "off"
        large_font = 20  # get better resolution with larger size        
        font_path = "/usr/share/fonts/truetype/ttf-bitstream-vera/VeraMono.ttf"
        img = Image.fromarray(frame)
        width_original, height_original = img.size[0], img.size[1]
        chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))
        SC = 1/(slider+7.5) #scale image
        GCF = 1.5 #intensity correction 1 = normal intensity, 0 = all black, +infinite = white
        WCF = 7/4
        
        S = ( round(width_original*SC*WCF), round(height_original*SC) )
        img = np.sum( np.asarray( img.resize(S) ), axis=2)
        
        img -= img.min()
        img = (1.0 - img/img.max())**GCF*(chars.size-1)
        lines = tuple()
        for r in chars[img.astype(int)] :
            lines += tuple(["".join(r)])
        
        try:
            # Reading from a font file is slower but have a better rendering
            font = PIL.ImageFont.truetype(font_path, size=large_font)
        except IOError:
            # Loading default font may be faster but less mesmerizing
            font = PIL.ImageFont.load_default()
            print('Could not use chosen font. Using default.')

        # make the background image based on the combination of font and lines
        pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
        max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
        # max height is adjusted down because it's too large visually for spacing
        max_height = pt2px(font.getsize("".join(chars))[1])
        max_width = pt2px(font.getsize(max_width_line)[0])
        height = max_height * len(lines)  # perfect or a little oversized
        width = int(round(max_width + 40))  # a little oversized
        image = PIL.Image.new( 'L', (width, height), color=PIXEL_OFF)
        draw = PIL.ImageDraw.Draw(image)

        # draw each line of text
        vertical_position = 5
        horizontal_position = 5
        line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
        for line in lines:
            draw.text((horizontal_position, vertical_position),
                      line, fill=PIXEL_ON, font=font)
            vertical_position += line_spacing
        c_box = PIL.ImageOps.invert(image).getbbox()
        image = image.crop(c_box)
        image = image.resize((width_original, height_original), Image.ANTIALIAS)
        image = image.convert('RGB')
        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        return open_cv_image

    def saveImage(self, frame, name="capture", folder="capture"):
        """Write image on disk

        Positional argument:
        frame -- frame (numpy array) to be written on disk

        Keyword arguments:
        name -- name of the file (default "capture")
        folder -- folder or path in which file will be saved (default "capture")
        """
        if not os.path.isdir(folder):
            raise ValueError("Folder is invalid!")
        cv2.imwrite(os.path.join(folder, name + ".jpeg"), frame)

    def applyHats(self, frame, slider, hat_picker=False):
        """Add hat over detected heads in frame

        Detects faces in image using AI. Pastes scaled hat over the faces.

        Positional arguments:
        frame -- frame (numpy array) to be modfieid
        slider -- hat number
        """

        MAX_FACE_HEIGHT = 250

        # convert frame to grayscale to pass to the openCV detectMultiScale function
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if not hat_picker:
            hat_number = math.floor((slider - 1) / 100 * len(self.hats))
            hat = self.hats[hat_number]['img']
            w_hat, h_hat = hat.size[0], hat.size[1]

        # detect the faces present in the frame
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(20, 20)
        )

        # create a PIL image to paste the hat on the detected faces
        pil_img = Image.fromarray(frame)

        for (x, y, w, h) in faces:

            factor = math.floor(h/2) / MAX_FACE_HEIGHT

            if hat_picker:
                hat_number = self.determine_hat_by_color(frame, x, y, w, h, factor)
                hat = self.hats[hat_number]['img']
                w_hat, h_hat = hat.size[0], hat.size[1]

            hat_to_add = hat.resize((math.floor(factor * w_hat), math.floor(factor * h_hat)))

            w_hat, h_hat = hat_to_add.size[0], hat_to_add.size[1]

            hat_offset_x = math.floor(self.hats[hat_number]['offset_x'] * factor)
            hat_offset_y = math.floor(self.hats[hat_number]['offset_y'] * factor)

            hat_to_add = cv2.cvtColor(np.array(hat_to_add), cv2.COLOR_RGBA2BGRA)

            hat_to_add = Image.fromarray(hat_to_add)

            # paste the hat on the face of the person
            pil_img.paste(hat_to_add, (x + hat_offset_x, y + hat_offset_y), hat_to_add)

        return np.array(pil_img)

    def determine_hat_by_color(self, frame, x, y, w, h, factor):

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        shirt_x = x + math.floor(w/2)
        shirt_y = y + h + math.floor(factor * 400)

        w_frame, h_frame = frame.shape[:2]

        if shirt_y >= h_frame:
            shirt_y = h_frame - 1

        color_mat = frame[shirt_x-20:shirt_x+20, shirt_y-20:shirt_y+20]
        color = np.mean(color_mat, axis=(0, 1))
        return ColorDetection().nearest_color(color, limit=len(self.hats) - 1)

    def crop_hats_image(self, path, image):

        image = np.array(image)

        image_bw = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

        ret, thresh = cv2.threshold(image_bw, 240, 255, cv2.THRESH_BINARY)

        image_bw[thresh == 255] = 0

        non_white_pixels_height = np.where(image_bw.sum(axis=1))
        non_white_pixels_width = np.where(image_bw.sum(axis=0))

        top = np.min(non_white_pixels_height)
        bottom = np.max(non_white_pixels_height)
        left = np.min(non_white_pixels_width)
        right = np.max(non_white_pixels_width)

        image = image[top:bottom, left:right]
        pil_img = Image.fromarray(image)
        pil_img.save(path)

class ColorDetection:
    """
    https://stackoverflow.com/questions/3565108/which-is-most-accurate-way-to-distinguish-one-of-8-colors/3565191#3565191
    """
    def __init__(self):
        self.colors = dict((
            ((196, 2, 51), 0),  # red
            ((255, 165, 0),  1),  # orange
            ((0, 128, 0),  2),  # green
            ((0, 0, 255), 3),  # blue
            ((127, 0, 255), 4),  # violet
            ((0, 0, 0), 5),  # black
            ((255, 255, 255), 6),))  # white

    def rgb_to_ycc(self, r, g, b):  # http://bit.ly/1blFUsF
        y = .299 * r + .587 * g + .114 * b
        cb = 128 - .168736 * r - .331364 * g + .5 * b
        cr = 128 + .5 * r - .418688 * g - .081312 * b
        return y, cb, cr

    def to_ycc(self, color):
        """ converts color tuples to floats and then to yuv """
        return self.rgb_to_ycc(*[x / 255.0 for x in color])

    def color_dist(self, c1, c2):
        """ returns the squared euklidian distance between two color vectors in yuv space """
        return sum((a - b) ** 2 for a, b in zip(self.to_ycc(c1), self.to_ycc(c2)))

    def min_color_diff(self, color_to_match, colors):
        """ returns the `(distance, color_name)` with the minimal distance to `colors`"""
        return min(  # overal best is the best match to any color:
            (self.color_dist(color_to_match, test), colors[test])  # (distance to `test` color, color name)
            for test in colors)

    def nearest_color(self, color_to_determine, limit=100):
        color_to_determine = tuple(color_to_determine)
        res = self.min_color_diff(color_to_determine, self.colors)
        return res[1] % limit
