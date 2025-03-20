#!/usr/local/python env
# -*- coding: utf-8 -*-

class Status(object):
    LENGTH = 0
    CONTENT = 1
    END = 2

class GuacamoleParser(object):
    terminator = ';'
    arg_separator = '.'
    args_separator = ','
    max_read_size = 1024*8

    def __init__(self):
        self.buffer = ''
        self.current_status = Status.LENGTH
        self.args = []
        self.arg_len = ''
        self.arg_str = ''

    def parse(self, data):
        self.buffer += data
        while 1:
            ret = self.parse_inst()
            if not ret:
                break
            yield ret

    def parse_inst(self):
        tmp_buffer = self.buffer
        arg_str = ''
        if self.current_status == Status.END:
            self.current_status = Status.LENGTH
            self.args = []
            self.arg_len = ''
            self.arg_str = ''
        while 1:
            if len(tmp_buffer) == 0:
                self.buffer = tmp_buffer
                return None
            if self.current_status == Status.LENGTH:
                arg_len_str = tmp_buffer[0]
                tmp_buffer = tmp_buffer[1:]
                if arg_len_str == self.arg_separator:
                    self.current_status = Status.CONTENT
                    continue
                self.arg_len += arg_len_str
                continue
            elif self.current_status == Status.CONTENT:
                len_int = int(self.arg_len)
                if len(tmp_buffer) < len_int or len(tmp_buffer[len_int:]) < 1:
                    self.buffer = tmp_buffer
                    return None
                self.arg_len = ''
                arg_str = tmp_buffer[:len_int]
                tmp_buffer = tmp_buffer[len_int:]
                self.args.append(arg_str)
                if len(tmp_buffer) > 0:
                    tmp_str = tmp_buffer[0]
                    tmp_buffer = tmp_buffer[1:]
                    if tmp_str == self.args_separator:
                        self.current_status = Status.LENGTH
                    elif tmp_str == self.terminator:
                        self.current_status = Status.END
                        self.buffer = tmp_buffer
                        return self.args
                    else:
                        raise Exception(f'Invalid protocol string `{tmp_str}`, Must `,` or `;`')
                else:
                    self.buffer = tmp_buffer
                    continue
