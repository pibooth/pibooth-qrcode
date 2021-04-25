# -*- coding: utf-8 -*-

"""Pibooth plugin to display a QR Code on the screen during idle time."""

import os
import qrcode
import pygame
import pibooth


__version__ = "0.0.3"


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
                   "QR code background color", "Background color", (0 ,0 ,0))

@pibooth.hookimpl
def pibooth_startup(cfg, app):
    """Store the qrcode prefix as an attribute of the app
    """
    app.qrcode_prefix = cfg.get('QRCODE', 'prefix_url')


@pibooth.hookimpl
def state_wait_enter(app, win):
    """
    Display the QR Code on the wait view.
    """
    if hasattr(app, 'previous_qr'):
        win_rect = win.get_rect()
        qr_rect = app.previous_qr.get_rect()
        win.surface.blit(app.previous_qr, (10, win_rect.height - qr_rect.height - 10))


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
    qrcode_fill_color = '#%02x%02x%02x' %cfg.gettyped("QRCODE", 'foreground')
    qrcode_background_color = '#%02x%02x%02x' % cfg.gettyped("QRCODE", 'background')

    image = qr.make_image(fill_color=qrcode_fill_color, back_color=qrcode_background_color)
    app.previous_qr = pygame.image.fromstring(image.tobytes(), image.size, image.mode)


@pibooth.hookimpl
def state_print_enter(app, win):
    """
    Display the QR Code on the print view.
    """
    win_rect = win.get_rect()
    qr_rect = app.previous_qr.get_rect()
    win.surface.blit(app.previous_qr, (win_rect.width - qr_rect.width - 10,
                                       win_rect.height - qr_rect.height - 10))
