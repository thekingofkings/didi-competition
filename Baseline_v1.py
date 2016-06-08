"""
Time series baseline predictor.

Use different periodicity to learn a predictor.


Hongjian
6/7/2016
"""


from DemandSupplyGap import *
from Utilities import *




if __name__ == "__main__":

    train = calculateDemandSupplyGap("demand", "train")
    WP = weeklyPattern(train)

    test = calculateDemandSupplyGap("demand", "test")
    
    grnd_truth = []
    estimation = []

    for date in test:
        for region in test[date]:
            for tid, observation in enumerate(test[date][region]):
                if observation != -1:
                    grnd_truth.append(observation)
                    estimation.append(WP[getWeekDay(date)][region][tid])

    print MAPE(grnd_truth, estimation), len(grnd_truth)
