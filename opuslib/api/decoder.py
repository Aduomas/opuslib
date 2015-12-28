#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Никита Кузнецов <self@svartalf.info>'
__copyright__ = 'Copyright (c) 2012, SvartalF'
__license__ = 'BSD 3-Clause License'


import array
import ctypes

import opuslib.api
import opuslib.exceptions


class Decoder(ctypes.Structure):
    """Opus decoder state.

    This contains the complete state of an Opus decoder.

    """
    pass

DecoderPointer = ctypes.POINTER(Decoder)


get_size = opuslib.api.libopus.opus_decoder_get_size
get_size.argtypes = (ctypes.c_int,)
get_size.restype = ctypes.c_int
get_size.__doc__ = 'Gets the size of an OpusDecoder structure'


_create = opuslib.api.libopus.opus_decoder_create
_create.argtypes = (ctypes.c_int, ctypes.c_int, opuslib.api.c_int_pointer)
_create.restype = DecoderPointer


def create(fs, channels):
    """Allocates and initializes a decoder state"""

    result_code = ctypes.c_int()

    result = _create(fs, channels, ctypes.byref(result_code))
    if result_code.value is not opuslib.api.constants.OK:
        raise opuslib.exceptions.OpusError(
            "Decoder returned: %s" % result_code.value)

    return result


_packet_get_bandwidth = opuslib.api.libopus.opus_packet_get_bandwidth
_packet_get_bandwidth.argtypes = (ctypes.c_char_p,)
_packet_get_bandwidth.restype = ctypes.c_int


def packet_get_bandwidth(data):
    """Gets the bandwidth of an Opus packet."""

    try:
        data_pointer = ctypes.c_char_p(data)
    except TypeError:
        data_pointer = ctypes.c_char_p(bytes(data.encode('latin-1')))

    result = _packet_get_bandwidth(data_pointer)
    if result_code.value is not opuslib.api.constants.OK:
        raise opuslib.exceptions.OpusError(
            "Decoder returned: %s" % result_code.value)

    return result


_packet_get_nb_channels = opuslib.api.libopus.opus_packet_get_nb_channels
_packet_get_nb_channels.argtypes = (ctypes.c_char_p,)
_packet_get_nb_channels.restype = ctypes.c_int


def packet_get_nb_channels(data):
    """Gets the number of channels from an Opus packet"""

    try:
        data_pointer = ctypes.c_char_p(data)
    except TypeError:
        data_pointer = ctypes.c_char_p(bytes(data.encode('latin-1')))

    result = _packet_get_nb_channels(data_pointer)
    if result_code.value is not opuslib.api.constants.OK:
        raise opuslib.exceptions.OpusError(
            "Decoder returned: %s" % result_code.value)

    return result


_packet_get_nb_frames = opuslib.api.libopus.opus_packet_get_nb_frames
_packet_get_nb_frames.argtypes = (ctypes.c_char_p, ctypes.c_int)
_packet_get_nb_frames.restype = ctypes.c_int


def packet_get_nb_frames(data, length=None):
    """Gets the number of frames in an Opus packet"""

    try:
        data_pointer = ctypes.c_char_p(data)
    except TypeError:
        data_pointer = ctypes.c_char_p(bytes(data.encode('latin-1')))
    if length is None:
        length = len(data)

    result = _packet_get_nb_frames(data_pointer, ctypes.c_int(length))
    if result_code.value is not opuslib.api.constants.OK:
        raise opuslib.exceptions.OpusError(
            "Decoder returned: %s" % result_code.value)

    return result


_packet_get_samples_per_frame = \
    opuslib.api.libopus.opus_packet_get_samples_per_frame
_packet_get_samples_per_frame.argtypes = (ctypes.c_char_p, ctypes.c_int)
_packet_get_samples_per_frame.restype = ctypes.c_int


def packet_get_samples_per_frame(data, fs):
    """Gets the number of samples per frame from an Opus packet"""

    try:
        data_pointer = ctypes.c_char_p(data)
    except TypeError:
        data_pointer = ctypes.c_char_p(bytes(data.encode('latin-1')))

    result = _packet_get_nb_frames(data_pointer, ctypes.c_int(fs))
    if result_code.value is not opuslib.api.constants.OK:
        raise opuslib.exceptions.OpusError(
            "Decoder returned: %s" % result_code.value)
    return result


_get_nb_samples = opuslib.api.libopus.opus_decoder_get_nb_samples
_get_nb_samples.argtypes = (DecoderPointer, ctypes.c_char_p, ctypes.c_int32)
_get_nb_samples.restype = ctypes.c_int


def get_nb_samples(decoder, packet, length):
    try:
        result = _get_nb_samples(decoder, packet, length)
    except ctypes.ArgumentError:
        result = _get_nb_samples(
            decoder, bytes(packet.encode('latin-1')), length)
    if result_code.value is not opuslib.api.constants.OK:
        raise opuslib.exceptions.OpusError(
            "Decoder returned: %s" % result_code.value)

    return result


_decode = opuslib.api.libopus.opus_decode
_decode.argtypes = (
    DecoderPointer, ctypes.c_char_p, ctypes.c_int32,
    opuslib.api.c_int16_pointer, ctypes.c_int, ctypes.c_int)
_decode.restype = ctypes.c_int


def decode(decoder, data, length, frame_size, decode_fec, channels=2):
    """Decode an Opus frame

    Unlike the `opus_decode` function , this function takes an additional
    parameter `channels`, which indicates the number of channels in the frame
    """

    pcm_size = frame_size * channels * ctypes.sizeof(ctypes.c_int16)
    pcm = (ctypes.c_int16 * pcm_size)()
    pcm_pointer = ctypes.cast(pcm, opuslib.api.c_int16_pointer)

    # Converting from a boolean to int
    decode_fec = int(bool(decode_fec))

    try:
        result = _decode(
            decoder, data, length, pcm_pointer, frame_size, decode_fec)
    except ctypes.ArgumentError:
        result = _decode(
            decoder, bytes(data.encode('latin-1')), length, pcm_pointer,
            frame_size, decode_fec)
    if result_code.value is not opuslib.api.constants.OK:
        raise opuslib.exceptions.OpusError(
            "Decoder returned: %s" % result_code.value)

    return array.array('h', pcm[:result * channels]).tostring()


_decode_float = opuslib.api.libopus.opus_decode_float
_decode_float.argtypes = (
    DecoderPointer, ctypes.c_char_p, ctypes.c_int32,
    opuslib.api.c_float_pointer, ctypes.c_int, ctypes.c_int)
_decode_float.restype = ctypes.c_int


def decode_float(decoder, data, length, frame_size, decode_fec, channels=2):
    pcm_size = frame_size * channels * ctypes.sizeof(ctypes.c_float)
    pcm = (ctypes.c_float * pcm_size)()
    pcm_pointer = ctypes.cast(pcm, opuslib.api.c_float_pointer)

    # Converting from a boolean to int
    decode_fec = int(bool(decode_fec))

    try:
        result = _decode_float(
            decoder, data, length, pcm_pointer, frame_size, decode_fec)
    except:
        result = _decode_float(
            decoder, bytes(data.encode('latin-1')), length, pcm_pointer,
            frame_size, decode_fec)
    if result_code.value is not opuslib.api.constants.OK:
        raise opuslib.exceptions.OpusError(
            "Decoder returned: %s" % result_code.value)

    return array.array('f', pcm[:result * channels]).tostring()


_ctl = opuslib.api.libopus.opus_decoder_ctl
_ctl.restype = ctypes.c_int


def ctl(decoder, request, value=None):
    if value is not None:
        return request(_ctl, decoder, value)

    return request(_ctl, decoder)


destroy = opuslib.api.libopus.opus_decoder_destroy
destroy.argtypes = (DecoderPointer,)
destroy.restype = None
destroy.__doc__ = 'Frees an OpusDecoder allocated by opus_decoder_create()'
