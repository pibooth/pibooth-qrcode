import os
import qrcode
import pygame

import pibooth

__version__ = "1.0.0"

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('QRCODE', 'activate', True,
                   "Enable qr code",
                   "Enable qr code", ['True', 'False'])
    cfg.add_option('QRCODE', 'by_photo', True,
                   "Generate new link by photo with basename and photo name",
                   "Generate by photo", ["True","False"])
    cfg.add_option('QRCODE', 'url', "",
                   "The qr code basename of URL or unique URL(if by_photo=False)",
                   "url", "")
    cfg.add_option('QRCODE', 'color', ("black", "white"),
                   "The qr code color to fill and background",
                   "color", ['("black", "white")', '("darkred", "white")', '("darkgreen", "white")', '("darkblue", "white")',
                           '("black", "transparent")', '("darkred", "transparent")', '("darkgreen", "transparent")',
                           '("darkblue", "transparent")'])

@pibooth.hookimpl
def state_wait_enter(app, win, cfg):
    """
    Display the QR Code on the wait view.
    """
    if hasattr(app, 'previous_qr') and cfg.getboolean('QRCODE', 'activate'):
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

    name = os.path.basename(app.previous_picture_file)

    if cfg.getboolean('QRCODE', 'by_photo'):
        qr.add_data(os.path.join(cfg.get('QRCODE', 'url'), name))
    else:
        qr.add_data(cfg.get('QRCODE', 'url'))
    qr.make(fit=True)

    image = qr.make_image(fill_color=cfg.gettyped('QRCODE', 'color')[0], back_color=cfg.gettyped('QRCODE', 'color')[1]).convert('RGBA')
    app.previous_qr = pygame.image.fromstring(image.tobytes(), image.size, image.mode)


@pibooth.hookimpl
def state_print_enter(app, win, cfg):
    """
    Display the QR Code on the print view.
    """
    win_rect = win.get_rect()
    qr_rect = app.previous_qr.get_rect()
    if cfg.getboolean('QRCODE', 'activate'):
        win.surface.blit(app.previous_qr, (win_rect.width - qr_rect.width - 10,
                                           win_rect.height - qr_rect.height - 10))
