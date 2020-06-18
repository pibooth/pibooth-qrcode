#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import qrcode
import pygame

import pibooth

__version__ = "0.0.1"

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('QRCODE', 'qrcode_prefix', "https://github.com/pibooth/pibooth",
                   "Prefix for the qrcode")

@pibooth.hookimpl
def pibooth_startup(cfg, app):
    """Store the qrcode prefix as an attribute of the app
    """
    app.qrcode_prefix = cfg.get('QRCODE', 'qrcode_prefix')

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
def state_processing_exit(app):
    """
    Generate the QR Code and store it in the application.
    """
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=3,
                       border=1)

    name = os.path.basename(app.previous_picture_file)

    qr.add_data(os.path.join(app.qrcode_prefix, name))
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white").convert('RGB')
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
