# -*- coding: utf-8 -*-

"""Pibooth plugin to display a QR Code on the screen during idle time."""

import os
import qrcode
import pygame
import pibooth


__version__ = "0.0.4"


SECTION = 'QRCODE'
LOCATIONS = ['topleft', 'topright',
             'bottomleft', 'bottomright',
             'midtop-left', 'midtop-right',
             'midbottom-left', 'midbottom-right']


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option(SECTION, 'prefix_url', "https://github.com/pibooth/pibooth",
                   "Prefix URL for the QR code")
    cfg.add_option(SECTION, 'unique_url', True,
                   "Use only one URL for all photos (one QR code linking to the album)",
                   "Use only one URL", ["True", "False"])
    cfg.add_option(SECTION, 'foreground', (255, 255, 255),
                   "QR code foreground color",
                   "Color", (255, 255, 255))
    cfg.add_option(SECTION, 'background', (0, 0, 0),
                   "QR code background color",
                   "Background color", (0, 0, 0))
    cfg.add_option(SECTION, 'offset', (20, 40),
                   "QR code offset from location")
    cfg.add_option(SECTION, 'wait_location', "bottomleft",
                   "QR code location on 'wait' state: {}".format(', '.join(LOCATIONS)),
                   "Location on wait screen", LOCATIONS)
    cfg.add_option(SECTION, 'print_location', "bottomright",
                   "QR code location on 'print' state: {}".format(', '.join(LOCATIONS)),
                   "Location on print screen", LOCATIONS)


def get_position(win, qrcode_image, location, offset):
    win_rect = win.get_rect()
    win_rect.topleft = (0, 0)
    location, sublocation = location, ''
    if '-' in location:
        location, sublocation = location.split('-')
    pos = list(getattr(win_rect, location))
    if 'top' in location:
        pos[1] += offset[1]
    else:
        pos[1] -= offset[1]
    if 'left' in location:
        pos[0] += offset[0]
    else:
        pos[0] -= offset[0]
    if 'mid' in location:
        if 'left' in sublocation:
            pos[0] -= qrcode_image.get_size()[0] // 2
        else:
            pos[0] += (qrcode_image.get_size()[0] // 2 + 2 * offset[0])
    qr_rect = qrcode_image.get_rect(**{location: pos})
    return qr_rect.topleft


@pibooth.hookimpl
def pibooth_startup(cfg):
    """
    Check the coherence of options.
    """
    for state in ('wait', 'print'):
        if cfg.get(SECTION, '{}_location'.format(state)) not in LOCATIONS:
            raise ValueError("Unknown QR code location on '{}' state '{}'".format(
                             state, cfg.get(SECTION, '{}_location'.format(state))))


@pibooth.hookimpl
def state_wait_do(cfg, app, win):
    """
    Display the QR Code on the wait view.
    """
    if hasattr(app, 'previous_qr'):
        offset = cfg.gettuple(SECTION, 'offset', int, 2)
        location = cfg.get(SECTION, 'wait_location')
        win.surface.blit(app.previous_qr, get_position(win, app.previous_qr, location, offset))


@pibooth.hookimpl
def state_processing_exit(cfg, app):
    """
    Generate the QR Code and store it in the application.
    """
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=3,
                       border=1)

    if cfg.getboolean("QRCODE", 'unique_url'):
        name = ''
    else:
        name = os.path.basename(app.previous_picture_file)

    qr.add_data(os.path.join(cfg.get(SECTION, 'prefix_url'), name))
    qr.make(fit=True)
    qrcode_fill_color = '#%02x%02x%02x' % cfg.gettyped("QRCODE", 'foreground')
    qrcode_background_color = '#%02x%02x%02x' % cfg.gettyped("QRCODE", 'background')

    image = qr.make_image(fill_color=qrcode_fill_color, back_color=qrcode_background_color)
    app.previous_qr = pygame.image.fromstring(image.tobytes(), image.size, image.mode)


@pibooth.hookimpl
def state_print_enter(cfg, app, win):
    """
    Display the QR Code on the print view.
    """
    offset = cfg.gettuple(SECTION, 'offset', int, 2)
    location = cfg.get(SECTION, 'print_location')
    win.surface.blit(app.previous_qr, get_position(win, app.previous_qr, location, offset))
