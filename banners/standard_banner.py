import random
from banners.banner import Banner

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
    - records_main: A list of integers indicating the pull numbers where
    the main operator (could be traded with the yellow-ticket) was obtained.
    - records_peipao: A list of integers indicating the pull numbers where
    the peipao operator was obtained.
    - pity1_used: True if the pity rule 1 (the guarantee of 150 pulls) is used.
    - pity2_used: True if the pity rule 2 (the guarantee of 150 pulls) is used.
    - pity1_is_main: True if the pity rule 1 results in the main operator.
    """
    records_main: list[int]
    records_peipao: list[int]
    pity1_used: bool
    pity2_used: bool
    pity1_is_main: None|bool

    def __init__(self) -> None:
        super().__init__()
        self.records_main = []
        self.records_peipao = []
        self.pity1_used = False
        self.pity2_used = False
        self.pity1_is_main = None

    def reset(self) -> None:
        super().reset()
        self.records_main = []
        self.records_peipao = []
        self.pity1_used = False
        self.pity2_used = False
        self.pity1_is_main = None

    def pull_once(self) -> bool:
        is_6star = super().pull_once()
        if is_6star:
            if 150 <= self.pulls < 300 and self.pity1_used == False:
                if random.random() < 0.5:
                    self.records_main.append(self.pulls)
                    self.pity1_is_main = True
                else:
                    self.records_peipao.append(self.pulls)
                    self.pity1_is_main = False
                self.pity1_used = True
            elif self.pulls >= 300 and self.pity2_used == False:
                if self.pity1_is_main:
                    self.records_peipao.append(self.pulls)
                else:
                    self.records_main.append(self.pulls)
                self.pity2_used = True
            else:
                if random.random() < 0.5:
                    self.records_main.append(self.pulls)
                else:
                    self.records_peipao.append(self.pulls)
        return is_6star

    def pull_desired(self, n: int, m: int) -> tuple[list[int], list[int]]:
        """Pull n main operator(s) and m peipao operator(s)"""
        while len(self.records_main) < n or len(self.records_peipao) < m:
            self.pull_once()
        return self.records_main, self.records_peipao

if __name__ == "__main__":
    random.seed(123)
    b = StandardBanner()
    n = 6
    m = 3
    records = b.pull_desired(n, m)
    print(f"在标准池中，抽到至少{n}个进店干员 + {m}个陪跑干员需要{max(records[0][-1], records[1][-1])}抽。")
    print(f"进店干员出现在：")
    print(records[0])
    print(f"陪跑干员出现在：")
    print(records[1])
