import re
from inventory.models import Card


def rename_cards(*args, **kwargs):
    cards = Card.objects.all()
    for card in cards:
        card_name = card.card_name
        # if the card name doesn't match
        if not re.match(r'^[A-Za-z0-9_]+$', card_name):
            new_name = clean_str(card_name)
            rename_card_if_necessary(card, new_name)


def rename_card_if_necessary(card, new_name, index=0):

    name_to_be_used = new_name
    if index != 0:
        name_to_be_used = new_name + str(index)
    # if the new named card already exists
    if len(Card.objects.filter(card_name=name_to_be_used)) > 0:
        rename_card_if_necessary(card, new_name, index + 1)
    else:
        card.card_name = name_to_be_used
        card.save()


def clean_str(text):
    string = text.strip().lower()
    # replace whitespace with '_'
    string = re.sub(' ', '_', string)
    # remove invalid characters
    string = re.sub('[^0-9a-zA-Z_]', '', string)
    # remove leading characters until a letter or underscore
    string = re.sub('^[^a-zA-Z_]+', '', string)
    return string
