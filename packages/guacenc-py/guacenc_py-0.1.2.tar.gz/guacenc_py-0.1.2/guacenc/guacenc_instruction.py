import cairo

from .guacenc_types import *


def guacenc_handle_size(display, inst):
    if len(inst.args) < 3:
        print("Invalid number of arguments for size instruction")
        return
    index = int(inst.args[0])
    width = int(inst.args[1])
    height = int(inst.args[2])

    buffer = display.get_related_buffer(index)
    if not buffer:
        print("Invalid buffer index: %d" % index)
        return

    buffer.resize(width, height)


def guacenc_handle_img(display, inst):
    if len(inst.args) < 6:
        print("Invalid number of arguments for img instruction")
        return
    stream_index = int(inst.args[0])
    mask = int(inst.args[1])
    layer_index = int(inst.args[2])
    mimetype = inst.args[3]
    x = int(inst.args[4])
    y = int(inst.args[5])
    display.create_image_stream(stream_index, mask, layer_index, mimetype, x, y)


def guacenc_handle_blob(display, inst):
    if len(inst.args) < 2:
        print("Invalid number of arguments for blob instruction")
        return

    index = int(inst.args[0])
    data = inst.args[1]
    buffer = display.get_image_stream(index)
    if not buffer:
        print("Invalid stream index: %d" % index)
        return
    buffer.receive_blob(data)


def guacenc_handle_end(display, inst):
    if len(inst.args) < 1:
        print("Invalid number of arguments for end instruction")
        return
    index = int(inst.args[0])
    stream = display.get_image_stream(index)
    if not stream:
        print("Invalid stream index: %d" % index)
        return
    buffer = display.get_related_buffer(stream.index)
    if not buffer:
        print("Invalid buffer index: %d" % stream.index)
        return
    stream.end(buffer)


def guacenc_handle_sync(display, inst):
    if len(inst.args) < 1:
        print("Invalid number of arguments for sync instruction")
        return
    timestamp = int(inst.args[0])
    display.sync(timestamp)


def guacenc_handle_copy(display, inst):
    if len(inst.args) < 9:
        print("Invalid number of arguments for copy instruction")
        return

    sindex = int(inst.args[0])
    sx = int(inst.args[1])
    sy = int(inst.args[2])
    width = int(inst.args[3])
    height = int(inst.args[4])
    mask = int(inst.args[5])
    dindex = int(inst.args[6])
    dx = int(inst.args[7])
    dy = int(inst.args[8])
    src = display.get_related_buffer(sindex)
    if not src:
        print("Invalid source buffer index: %d" % sindex)
        return
    dst = display.get_related_buffer(dindex)
    if not dst:
        print("Invalid destination buffer index: %d" % dindex)
        return

    if dst.autosize:
        dst.fit(dx + width, dy + height)

    if src.surface and dst.cairo:
        surface = src.surface
        if src != dst:
            surface = src.surface
        else:
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
            ctx = cairo.Context(surface)
            ctx.set_operator(cairo.OPERATOR_SOURCE)
            ctx.set_source_surface(src.surface, -sx, -sy)
            ctx.paint()
            sx = 0
            sy = 0
        dst.cairo.set_operator(guacenc_display_cairo_operator(mask))
        dst.cairo.set_source_surface(surface, dx - sx, dy - sy)
        dst.cairo.rectangle(dx, dy, width, height)
        dst.cairo.fill()


def guacenc_handle_mouse(display, inst):
    if len(inst.args) < 2:
        print("Invalid number of arguments for mouse instruction")
        return
    x = int(inst.args[0])
    y = int(inst.args[1])
    cursor = display.cursor
    cursor.x = x
    cursor.y = y
    if len(inst.args) < 4:
        return
    layer_index = int(inst.args[2])
    if layer_index != 0:
        return
    timestamp = int(inst.args[3])
    if display.last_sync > timestamp:
        return
    display.sync(timestamp)


def guacenc_handle_dispose(display, inst):
    if len(inst.args) < 1:
        print("Invalid number of arguments for dispose instruction")
        return
    index = int(inst.args[0])
    if index >= 0:
        display.free_layer(index)
    else:
        display.free_buffer(index)


def guacenc_handle_cursor(display, inst):
    if len(inst.args) < 7:
        print("Invalid number of arguments for cursor instruction")
        return
    hotspot_x = int(inst.args[0])
    hotspot_y = int(inst.args[1])
    sindex = int(inst.args[2])
    sx = int(inst.args[3])
    sy = int(inst.args[4])
    width = int(inst.args[5])
    height = int(inst.args[6])

    src = display.get_related_buffer(sindex)
    if not src:
        print("Invalid source buffer index: %d" % sindex)
        return
    cursor = display.cursor
    cursor.hotspot_x = hotspot_x
    cursor.hotspot_y = hotspot_y
    cursor.buffer.resize(width, height)
    dst = cursor.buffer
    if src.surface and dst.cairo:
        dst.cairo.set_operator(cairo.OPERATOR_SOURCE)
        dst.cairo.set_source_surface(src.surface, sx, sy)
        dst.cairo.paint()

def guacenc_handle_rect(display, inst):
    if len(inst.args) < 5:
        print("Invalid number of arguments for rect instruction")
        return
    index = int(inst.args[0])
    x = int(inst.args[1])
    y = int(inst.args[2])
    width = int(inst.args[3])
    height = int(inst.args[4])
    buffer = display.get_related_buffer(index)
    if not buffer:
        print("Invalid buffer index: %d" % index)
        return
    if buffer.autosize:
        buffer.fit(x + width, y + height)
    if buffer.cairo:
        buffer.cairo.rectangle(x, y, width, height)



def guacenc_handle_cfill(display, inst):
    if len(inst.args) < 6:
        print("Invalid number of arguments for cfill instruction")
        return
    mask = int(inst.args[0])
    index = int(inst.args[1])
    r = float(inst.args[2])/ 255.0
    g = float(inst.args[3]) / 255.0
    b = float(inst.args[4]) / 255.0
    a = float(inst.args[5]) / 255.0

    buffer = display.get_related_buffer(index)
    if not buffer:
        print("Invalid buffer index: %d" % index)
        return
    if buffer.cairo:
        buffer.cairo.set_operator(guacenc_display_cairo_operator(mask))
        buffer.cairo.set_source_rgba(r, g, b, a)
        buffer.cairo.fill()


def guacenc_handle_move(display, inst):
    if len(inst.args) < 5:
        print("Invalid number of arguments for move instruction")
        return
    layer_index = int(inst.args[0])
    parent_index = int(inst.args[1])
    x = int(inst.args[2])
    y = int(inst.args[3])
    z = int(inst.args[4])
    layer = display.get_layer(layer_index)
    if not layer:
        print("Invalid layer index: %d" % layer_index)
        return
    if display.get_layer(parent_index) is None:
        print("Invalid parent layer index: %d" % parent_index)
        return
    layer.parent_index = parent_index
    layer.x = x
    layer.y = y
    layer.z = z

def guacenc_handle_shade(display, inst):
    if len(inst.args) < 2:
        print("Invalid number of arguments for shade instruction")
        return
    index = int(inst.args[0])
    opacity = int(inst.args[1])

    layer = display.get_layer(index)
    if not layer:
        print("Invalid layer index: %d" % index)
        return
    layer.opacity = opacity

def guacenc_handle_transfer(display, inst):

    if len(inst.args) < 9:
        print("Invalid number of arguments for transfer instruction")
        return
    src_index = int(inst.args[0])
    src_x = int(inst.args[1])
    src_y = int(inst.args[2])
    src_w = int(inst.args[3])
    src_h = int(inst.args[4])
    function = int(inst.args[5])
    dst_index = int(inst.args[6])
    dst_x = int(inst.args[7])
    dst_y = int(inst.args[8])
    print("Transfer instruction not implemented")



handle_func_map = {
    "blob": guacenc_handle_blob,
    "img": guacenc_handle_img,
    "end": guacenc_handle_end,
    "mouse": guacenc_handle_mouse,
    "sync": guacenc_handle_sync,
    "cursor": guacenc_handle_cursor,
    "copy": guacenc_handle_copy,
    "transfer": guacenc_handle_transfer,
    "size": guacenc_handle_size,
    "rect": guacenc_handle_rect,
    "cfill": guacenc_handle_cfill,
    "move": guacenc_handle_move,
    "shade": guacenc_handle_shade,
    "dispose": guacenc_handle_dispose,
}

def guacenc_handle_instruction(display, inst):
    func_handler = handle_func_map.get(inst.cmd, None)
    if not func_handler:
        # print("No handler for instruction: %s" % inst.cmd)
        return
    func_handler(display, inst)
    if display.callback and callable(display.callback):
        display.callback(display, inst)
