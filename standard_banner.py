import random
from banner import Banner

class StandardBanner(Banner):
    """A class for the Standard Banner.

    Standard Banner:
    - This banner features two rate-up six-star character.
    - When a six-star character is pulled, there is a 50% chance it will be a
    rate-up, each character with a 25% chance.
    - Pity rule: after 150 pulls, the next six-star character must be one of the
    rate-up character; after 300 pulls, the next six-star character must be the
    other rate-up character.

    Attributes:


    """
    def __init__(self):
        super().__init__()
