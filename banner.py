import random

class Banner:
    """A class simulating a basic banner in Arknights.

    A basic banner has a basic six-star rate of 2%, and a pity-rule where:
     - If a six-star character does not appear in 50 continuous pulls, beginning
     from the 51th pull, the rate of six-star increase by 2% each pull. (i.e. 
     51th: 4%, 52th: 6%, etc.)
     - Once gained a six-star character, the rate returns to 2%.
    
    Attributes:
     - prob_6star: the probability of getting a six-star of the next pull.
     - pity_counter_basic: pity counter for the basic pity rule.
     - pulls: current number of pulls used.
     - records: a list of integers containing the # of pulls of each six-star.
    """
    
    prob_6star: float
    pity_counter_basic: int
    pulls: int
    records: list

    def __init__(self) -> None:
        self.prob_6star = 0.02
        self.pity_counter_basic = 0
        self.pulls = 0
        self.records = []
    
    def pull_times(self, n: int) -> list:
        """Make n pulls!
        """
        rslt = []
        for _ in range(n):
            rslt.append(self.pull_once())
        return rslt
        
    def pull_once(self) -> bool:
        """Make a pull!
        
        >>> banner = Banner()
        >>> banner.pull_once()
        False
        >>> banner.pull_once()
        True
        """
        self.pulls += 1
        # If got a six-star:
        if random.random() < self.prob_6star:
            self.records.append(self.pulls)
            self.prob_6star = 0.02  # Reset probability
            self.pity_counter_basic = 0  # Reset pity counter
            return True
        # Didn't get a six-star
        else:
            self.pity_counter_basic += 1
            if self.pity_counter_basic >= 50:
                self.prob_6star = min(1.0, self.prob_6star + 0.02)
            return False

    def convert_gap_records(self) -> list:
        """Output records based on the pulls used between the occurance of each
        six-star gained.

        Precondition:
         - len(self.records) > 0
        """
        cur_pull = 0
        records_gap = []
        for pull_cnt in self.records:
            records_gap.append(pull_cnt - cur_pull)
            cur_pull = pull_cnt
        return records_gap

if __name__ == '__main__':
    random.seed(100)
    b = Banner()
    b.pull_times(100)
    print(b.convert_gap_records())

