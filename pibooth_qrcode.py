# -*- coding: utf-8 -*-

"""Pibooth plugin to display a QR Code on the screen during idle time."""

import os
import qrcode
import pygame
import pibooth


__version__ = "0.0.3"


POSITION_OFFSET = [20, 40]


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('QRCODE', 'prefix_url', "https://github.com/pibooth/pibooth",
                   "Prefix URL for the QR code")
    cfg.add_option('QRCODE', 'unique_url', True,
                   "Use only one URL for all photos (one QR code linking to the album)",
                   "Use only one URL", ["True", "False"])
    cfg.add_option('QRCODE', 'foreground', (255, 255, 255),
                   "QR code foreground color", "Color", (255, 255, 255))
    cfg.add_option('QRCODE', 'background', (0, 0, 0),
                   "QR code background color", "Background color", (0, 0, 0))


def get_position(win, qrcode_image, location):
    win_rect = win.get_rect()
    win_rect.topleft = (0, 0)
    pos = list(getattr(win_rect, location))
    if location.startswith('top'):
        pos[1] += POSITION_OFFSET[1]
    else:
        pos[1] -= POSITION_OFFSET[1]
    if location.endswith('left'):
        pos[0] += POSITION_OFFSET[0]
    else:
        pos[0] -= POSITION_OFFSET[0]
    qr_rect = qrcode_image.get_rect(**{location: pos})
    return qr_rect.topleft


@pibooth.hookimpl
def pibooth_startup(cfg, app):
    """Store the qrcode prefix as an attribute of the app
    """
    app.qrcode_prefix = cfg.get('QRCODE', 'prefix_url')


@pibooth.hookimpl
def state_wait_do(app, win):
    """
    Display the QR Code on the wait view.
    """
    if hasattr(app, 'previous_qr'):
        win.surface.blit(app.previous_qr, get_position(win, app.previous_qr, 'bottomleft'))


@pibooth.hookimpl
def state_processing_exit(app, cfg):
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

    qr.add_data(os.path.join(app.qrcode_prefix, name))
    qr.make(fit=True)
    qrcode_fill_color = '#%02x%02x%02x' % cfg.gettyped("QRCODE", 'foreground')
    qrcode_background_color = '#%02x%02x%02x' % cfg.gettyped("QRCODE", 'background')

    image = qr.make_image(fill_color=qrcode_fill_color, back_color=qrcode_background_color)
    app.previous_qr = pygame.image.fromstring(image.tobytes(), image.size, image.mode)


@pibooth.hookimpl
def state_print_enter(app, win):
    """
    Display the QR Code on the print view.
    """
    win.surface.blit(app.previous_qr, get_position(win, app.previous_qr, 'bottomright'))
