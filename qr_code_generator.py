"""
    Script to generate simple qr code business cards with or without certain features.
    The goal is to digitize this information in the form of a qr code and stop wasting paper
"""

import json
import sys
from pyzbar.pyzbar import decode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
import qrcode
from PIL import Image

BUSINESS_CARD_ATTRIBUTES = ['name', 'position', 'company', 'phone', 'email', 'website', 'logo',
                            'pixel_color', 'background_color']
DEBUG = False


def qr_code_generator(data: str) -> None:
    """
    Driver function to generate a simple qr code business card.
    :param data: the json file to be loaded in
    :return: No return type, images will be saved if viable
    """
    try:
        with open(data, 'r', encoding='utf-8') as json_entry:
            data = json.load(json_entry)
            if 'members' in data.keys():
                for member in data['members']:
                    single_qr_code_generator(member)
                    if qr_tester(member):
                        print(f'{member["name"]} good to go')
            else:
                single_qr_code_generator(data)
                if qr_tester(data):
                    print('Good to go')
    except FileNotFoundError:
        print('Json file not found, might be in wrong folder')


def single_qr_code_generator(single_entry: dict) -> None:
    """
    Generates a business card for one set of features
    :param single_entry: one json object corresponding to one business card
    :return: No return type, image will be saved if viable
    """
    card = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    if "name" in single_entry.keys():
        filename = f'{single_entry["name"]}.png'
        card.add_data(single_entry['name'] + "\n")
    else:
        filename = 'qr_card.png'

    for attribute in BUSINESS_CARD_ATTRIBUTES[1:-3]:
        if attribute in single_entry.keys():
            card.add_data(single_entry[attribute] + "\n")

    card.make()
    card.make()
    qr_color = 'Black'
    if "pixel_color" in single_entry.keys():
        qr_color = tuple(single_entry['pixel_color'])
    qr_background_color = 'white'
    if "background_color" in single_entry.keys():
        qr_background_color = tuple(single_entry['background_color'])

    if "logo" in single_entry.keys():
        try:
            logo = Image.open(single_entry['logo'])
            # taking base width
            basewidth = 100

            # adjust image size
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

            qr_card = card.make_image(
                image_factory=StyledPilImage,
                module_drawer=GappedSquareModuleDrawer(),
                color_mask=SolidFillColorMask(
                    front_color=qr_color, back_color=qr_background_color)).convert('RGB')

            # set size of QR code
            pos = ((qr_card.size[0] - logo.size[0]) // 2,
                   (qr_card.size[1] - logo.size[1]) // 2)
            qr_card.paste(logo, pos)
            if DEBUG:
                qr_card.show()
            else:
                qr_card.save(filename)

        except FileNotFoundError:
            print('Logo not found, might be in wrong folder')

    else:
        image = card.make_image(
            image_factory=StyledPilImage,
            module_drawer=GappedSquareModuleDrawer(),
            color_mask=SolidFillColorMask(
                front_color=qr_color,
                back_color=qr_background_color)).convert(
            'RGB')
        if DEBUG:
            image.show()
        else:
            image.save(filename)


def qr_tester(single_entry: dict) -> bool:
    """
    Simple tester to check if all information was relayed
    :param single_entry: one json object corresponding to one business card
    :return: Boolean representing whether all information was relayed
    """
    try:
        data = decode(Image.open(f'{single_entry["name"]}.png'))[0].data.decode()
        for key in BUSINESS_CARD_ATTRIBUTES[:-3]:
            if key in single_entry.keys():
                if not single_entry[key] in data:
                    raise AssertionError('Not all data was passed to the qr code')

    except FileNotFoundError:
        print("File was not saved correctly and thus can't be tested")
        return False
    return True


if __name__ == '__main__':
    qr_code_generator(sys.argv[1])
