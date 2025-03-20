import base64
import datetime
import inspect
import io
from enum import IntEnum

import cairo
from PIL import Image

GUACENC_DISPLAY_MAX_BUFFERS = 4096

GUACENC_DISPLAY_MAX_LAYERS = 64

GUACENC_DISPLAY_MAX_STREAMS = 64


GUACENC_DEFAULT_WIDTH = 640

GUACENC_DEFAULT_HEIGHT = 480

GUACENC_DEFAULT_BITRATE = 2000000

GUACENC_LAYER_NO_PARENT = -1


class Instruction(object):
    def __init__(self, cmd, *args):
        self.cmd = cmd
        self.args = args


class GuacCompositeMode(IntEnum):
    GUAC_COMP_ROUT = 0x2
    GUAC_COMP_ATOP = 0x6
    GUAC_COMP_XOR = 0xA
    GUAC_COMP_ROVER = 0xB
    GUAC_COMP_OVER = 0xE
    GUAC_COMP_PLUS = 0xF

    GUAC_COMP_RIN = 0x1
    GUAC_COMP_IN = 0x4
    GUAC_COMP_OUT = 0x8
    GUAC_COMP_RATOP = 0x9
    GUAC_COMP_SRC = 0xC


def guacenc_display_cairo_operator(mask):
    comp_cairo_map = {
        GuacCompositeMode.GUAC_COMP_SRC: cairo.OPERATOR_SOURCE,
        GuacCompositeMode.GUAC_COMP_OVER: cairo.OPERATOR_OVER,
        GuacCompositeMode.GUAC_COMP_IN: cairo.OPERATOR_IN,
        GuacCompositeMode.GUAC_COMP_OUT: cairo.OPERATOR_OUT,
        GuacCompositeMode.GUAC_COMP_ATOP: cairo.OPERATOR_ATOP,
        GuacCompositeMode.GUAC_COMP_ROVER: cairo.OPERATOR_DEST_OVER,
        GuacCompositeMode.GUAC_COMP_RIN: cairo.OPERATOR_DEST_IN,
        GuacCompositeMode.GUAC_COMP_ROUT: cairo.OPERATOR_DEST_OUT,
        GuacCompositeMode.GUAC_COMP_RATOP: cairo.OPERATOR_DEST_ATOP,
        GuacCompositeMode.GUAC_COMP_XOR: cairo.OPERATOR_XOR,
        GuacCompositeMode.GUAC_COMP_PLUS: cairo.OPERATOR_ADD,
    }
    return comp_cairo_map.get(mask, cairo.OPERATOR_OVER)


class GuacencBuffer(object):

    def __init__(self):
        self.autosize = False
        self.width = 0
        self.height = 0
        self.stride = 0
        self.surface = None
        self.cairo = None
        self.image = None

    def resize(self, width, height):
        if self.width == width and self.height == height:
            return
        if width == 0 or height == 0:
            self.width = 0
            self.height = 0
            self.surface = None
            self.cairo = None
            self.image = None
            return

        stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, width)
        image = bytearray([0 for _ in range(stride * height)])
        surface = cairo.ImageSurface.create_for_data(
            image, cairo.FORMAT_ARGB32, width, height, stride
        )
        context = cairo.Context(surface)
        if self.surface is not None:
            context.set_operator(cairo.OPERATOR_SOURCE)
            context.set_source_surface(self.surface, 0, 0)
            context.set_operator(cairo.OPERATOR_SOURCE)
            context.paint()

        self.width = width
        self.height = height
        self.stride = stride
        self.image = image
        self.surface = surface
        self.cairo = context

    def fit(self, x, y):
        new_width = self.width
        if new_width < (x + 1):
            new_width = x + 1
        new_height = self.height
        if new_height < (y + 1):
            new_height = y + 1
        if new_width != self.width or new_height != self.height:
            self.resize(new_width, new_height)


def guacenc_buffer_copy(dst, src):
    dst.resize(src.width, src.height)
    if src.surface is not None:
        dst.cairo.reset_clip()
        dst.cairo.set_operator(cairo.OPERATOR_SOURCE)
        dst.cairo.set_source_surface(src.surface, 0, 0)
        dst.cairo.paint()
        dst.cairo.set_operator(cairo.OPERATOR_OVER)


class GuacencLayer(object):

    def __init__(self):
        self.buffer = GuacencBuffer()
        self.frame = GuacencBuffer()
        self.opacity = 0xFF
        self.parent_index = 0
        self.x = 0
        self.y = 0
        self.z = 0


class GuacencCursor(object):

    def __init__(self):
        self.x = -1
        self.y = -1
        self.hotspot_x = 0
        self.hotspot_y = 0
        self.buffer = GuacencBuffer()


class ImageDecoder(object):

    def __init__(self, mime_type):
        self.mime_type = mime_type

    def decode(self, data):
        if self.mime_type == "image/png":
            return self.decode_png(data)
        elif self.mime_type == "image/jpeg":
            return self.decode_jpeg(data)
        elif self.mime_type == "image/webp":
            return self.decode_webp(data)
        else:
            return self.decode_general(data)

    def decode_png(self, data):
        io_fd = io.BytesIO(data)
        surface = cairo.ImageSurface.create_from_png(io_fd)
        return surface

    def decode_jpeg(self, data):
        webp_image = Image.open(io.BytesIO(data))
        buffer = io.BytesIO()
        webp_image.save(buffer, "PNG")
        return self.decode_png(buffer.getbuffer())

    def decode_webp(self, data):
        webp_image = Image.open(io.BytesIO(data))
        buffer = io.BytesIO()
        webp_image.save(buffer, "PNG")
        return self.decode_png(buffer.getbuffer())

    def decode_general(self, data):
        webp_image = Image.open(io.BytesIO(data))
        buffer = io.BytesIO()
        webp_image.save(buffer, "PNG")
        return self.decode_png(buffer.getbuffer())


class GuacencImageStream(object):

    def __init__(self, mask, index, mimetype, x, y):
        self.index = index
        self.mask = mask
        self.x = x
        self.y = y
        self.mimetype = mimetype
        self.decoder = ImageDecoder(mimetype)
        self.length = 0
        self.max_length = 0
        self.buffer = b""

    def receive_blob(self, data):
        self.buffer += base64.b64decode(data)
        self.length = len(self.buffer)

    def end(self, buffer):
        surface = self.decoder.decode(self.buffer)
        width = surface.get_width()
        height = surface.get_height()
        if buffer.autosize:
            buffer.fit(self.x + width, self.y + height)

        if buffer.cairo:
            buffer.cairo.set_operator(guacenc_display_cairo_operator(self.mask))
            buffer.cairo.set_source_surface(surface, self.x, self.y)
            buffer.cairo.rectangle(self.x, self.y, width, height)
            buffer.cairo.fill()


class Display(object):

    def __init__(self, width, height, callback=None):
        self.width = width
        self.height = height
        self.last_sync = 0
        self.buffers = [None for _ in range(GUACENC_DISPLAY_MAX_BUFFERS)]
        self.layers = [None for _ in range(GUACENC_DISPLAY_MAX_LAYERS)]
        self.image_streams = [None for _ in range(GUACENC_DISPLAY_MAX_STREAMS)]
        self.cursor = GuacencCursor()
        self._start_sync = 0
        self.interval = None
        self.callback = callback
        # check callback function with two arguments
        if len(inspect.signature(self.callback).parameters) != 2:
            raise ValueError("Callback function must have two arguments")


    def get_layer(self, index):
        if index < 0 or index >= GUACENC_DISPLAY_MAX_LAYERS:
            print("Invalid layer index: %d" % index)
            return None
        layer = self.layers[index]
        if layer is None:
            layer = GuacencLayer()
            if index == 0:
                layer.parent_index = -1
            self.layers[index] = layer
        return layer

    def free_layer(self, index):
        if index < 0 or index >= GUACENC_DISPLAY_MAX_LAYERS:
            print("Invalid layer index: %d" % index)
            return
        self.layers[index] = None

    def get_related_buffer(self, index):
        if index >= 0:
            layer = self.get_layer(index)
            if not layer:
                return None
            return layer.buffer
        return self.get_buffer(index)

    def get_buffer(self, index):
        internal_index = -index - 1
        if internal_index < 0 or internal_index >= GUACENC_DISPLAY_MAX_BUFFERS:
            print("Invalid buffer index: %d" % index)
            return None

        buffer = self.buffers[internal_index]
        if buffer is None:
            buffer = GuacencBuffer()
            buffer.autosize = True
            self.buffers[internal_index] = buffer

        return buffer

    def free_buffer(self, index):
        internal_index = -index - 1
        if internal_index < 0 or internal_index >= GUACENC_DISPLAY_MAX_BUFFERS:
            print("Invalid buffer index: %d" % index)
            return
        self.buffers[internal_index] = None

    def create_image_stream(self, index, mask, layer_index, mimetype, x, y):
        if index < 0 or index >= GUACENC_DISPLAY_MAX_STREAMS:
            print("Invalid stream index: %d" % index)
            return None
        self.image_streams[index] = GuacencImageStream(
            index, layer_index, mimetype, x, y
        )

    def get_image_stream(self, index):
        if index < 0 or index >= GUACENC_DISPLAY_MAX_STREAMS:
            print("Invalid stream index: %d" % index)
            return None
        return self.image_streams[index]

    def sync(self, timestamp):
        if timestamp < self.last_sync:
            print("Invalid timestamp: %d" % timestamp)
            return
        if self._start_sync == 0:
            self._start_sync = timestamp
        self.last_sync = timestamp
        self.flatten()
        if self._start_sync != self.last_sync:
            interval = int(self.last_sync) - int(self._start_sync)
            timedelta = datetime.timedelta(milliseconds=interval)
            self.interval = timedelta

    def flatten(self):
        layers = self.layers
        for i in range(GUACENC_DISPLAY_MAX_LAYERS):
            layer = layers[i]
            if not layer:
                continue
            buffer = layer.buffer
            frame = layer.frame
            guacenc_buffer_copy(frame, buffer)

        for i in range(GUACENC_DISPLAY_MAX_LAYERS):
            layer = layers[i]
            if not layer:
                continue
            if layer.opacity == 0:
                continue
            if layer.parent_index == GUACENC_LAYER_NO_PARENT:
                continue

            parent = self.get_layer(layer.parent_index)
            if not parent:
                continue
            src = layer.frame
            dst = parent.frame
            if src.surface is None:
                continue
            if dst.cairo is None:
                continue
            dst.cairo.reset_clip()
            dst.cairo.rectangle(layer.x, layer.y, src.width, src.height)
            dst.cairo.clip()
            dst.cairo.set_source_surface(src.surface, layer.x, layer.y)
            dst.cairo.paint_with_alpha(layer.opacity / 255.0)
        self.render_cursor()

    def render_cursor(self):
        cursor = self.cursor
        if cursor.x < 0 or cursor.y < 0:
            return
        def_layer = self.get_layer(0)
        if not def_layer:
            return
        src = cursor.buffer
        dst = def_layer.frame
        if src.width > 0 and src.height > 0:
            dst.cairo.set_source_surface(
                src.surface, cursor.x - cursor.hotspot_x, cursor.y - cursor.hotspot_y
            )
            dst.cairo.rectangle(
                cursor.x - cursor.hotspot_x,
                cursor.y - cursor.hotspot_y,
                src.width,
                src.height,
            )
            dst.cairo.fill()

    def save(self, img_name):
        def_layer = self.get_layer(0)
        if not def_layer:
            raise Exception("No default layer")
        if not def_layer.frame.surface:
            print("No default layer surface yet")
            return
        def_layer.frame.surface.write_to_png(img_name)

    def get_current_display_image(self):
        def_layer = self.get_layer(0)
        if not def_layer:
            raise Exception("No default layer")
        if not def_layer.frame.surface:
            print("No default layer surface yet")
            return None
        img_buffer = io.BytesIO()
        def_layer.frame.surface.write_to_png(img_buffer)
        img = Image.open(img_buffer)
        return img
