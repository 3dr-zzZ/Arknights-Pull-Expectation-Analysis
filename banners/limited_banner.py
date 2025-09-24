import random
from banners.banner import Banner

class LimitedBanner(Banner):
    """A class for the Limited Banner.

    Limited Banner:
    - This banner features two rate-up six-star character.
    - When a six-star character is pulled, there is a 70% chance it will be a
    rate-up, each character with a 35% chance.
    - Pity rule: when reach 300 pulls, the player will be gifted a limited
    operator.

    Attributes:
    - records_limited: A list of integers indicating the pull numbers where
    the limited operator was obtained.
    - records_peipao: A list of integers indicating the pull numbers where
    the peipao operator was obtained.
    """

    records_limited: list[int]
    records_peipao: list[int]

    def __init__(self) -> None:
        super().__init__()
        self.records_limited = []
        self.records_peipao = []

    def reset(self) -> None:
        super().reset()
        self.records_limited = []
        self.records_peipao = []

    def pull_once(self) -> bool:
        is_6star = super().pull_once()

        # 300th gifted
        if self.pulls == 300:
            self.records_limited.append(300)

        if is_6star:
            if random.random() < 0.7:
                if random.random() < 0.5:
                    self.records_limited.append(self.pulls)
                else:
                    self.records_peipao.append(self.pulls)
        return is_6star

    def pull_desired(self, n: int, m: int) -> tuple[list[int], list[int]]:
        """Pull n limited operators and m peipao operators.

        Note: there might be more than n limited operators or more than m peipao
        operators in the records, as the simulation stops when reaching *both*
        number requirements.
        """
        while len(self.records_limited) < n or len(self.records_peipao) < m:
            self.pull_once()
        return self.records_limited, self.records_peipao

if __name__ == "__main__":
    random.seed(123)
    b = LimitedBanner()
    n = 1
    m = 1
    records = b.pull_desired(n, m)
    print(f"在限定池中，抽到至少{n}个限定干员 + {m}个陪跑干员需要{max(records[0][-1], records[1][-1])}抽。")
    print(f"限定干员出现在：")
    print(records[0])
    print(f"陪跑干员出现在：")
    print(records[1])
