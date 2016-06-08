"""
Time series baseline predictor.

Use different periodicity to learn a predictor.


Hongjian
6/7/2016
"""


from DemandSupplyGap import *
from Utilities import *


def directly_predict(WP_gap, test_gap, target="gap"):
    """
    WP_gap is the weeklyPattern of gap.
    test_gap is map of map.
    """
    print "Directly predict", target
    grnd_truth = []
    estimation = []

    for date in test_gap:
        for region in test_gap[date]:
            for tid, observation in enumerate(test_gap[date][region]):
                if observation != -1:
                    grnd_truth.append(observation)
                    estimation.append(WP_gap[getWeekDay(date)][region][tid])

    print MAPE(grnd_truth, estimation), len(grnd_truth)



def use_supply_demand_predict_gap(WP_supply, WP_demand, test_gap):
    """
    WP_gap is the weeklyPattern of gap.
    test_gap is map of map.
    """
    print "Predict supply and demand then calculate gap"
    grnd_truth = []
    estimation = []

    for date in test_gap:
        for region in test_gap[date]:
            for tid, observation in enumerate(test_gap[date][region]):
                if observation != -1:
                    grnd_truth.append(observation)

                    wd = getWeekDay(date)
                    estm = WP_demand[wd][region][tid] - WP_supply[wd][region][tid]
                    estimation.append(estm)

    print MAPE(grnd_truth, estimation), len(grnd_truth)





train_supply = calculateDemandSupplyGap("supply", "train")
WP_supply = weeklyPatternByRegion(train_supply)
train_demand = calculateDemandSupplyGap("demand", "train")
WP_demand = weeklyPatternByRegion(train_demand)



def make_prediction(rid, date, tid):
    """
    Track best prediction method
    """
    method = "use_supply_demand_predict_gap"
    if method == "use_supply_demand_predict_gap":
        wd = getWeekDay(date)
        estm = WP_demand[wd][rid][tid] - WP_supply[wd][rid][tid]
    else:
        estm = 0
    return estm





def generatePrediction_Submission():
    """
    Generate submission file for given testing time slot
    """
    with open(join(TestFolder, "read_me_1.txt"), 'r') as fin, \
        open("data/output-test.csv", 'w') as fout:
        for line in fin:
            time = line.strip()
            reg = re.match("(\d{4}-\d{2}-\d{2})-(\d+)", time)
            date = reg.groups()[0]
            tid = int(reg.groups()[1])
            for rid in range(1, 67):
                estim = make_prediction(rid, date, tid)
                fout.write("{0},{1},{2}\n".format(rid, time, estim))



if __name__ == "__main__":

    
    train_gap = calculateDemandSupplyGap("gap", "train")
    WP_gap = weeklyPatternByRegion(train_gap)

    test_gap = calculateDemandSupplyGap("gap", "test")
    test_demand = calculateDemandSupplyGap("demand", "test")
    test_supply = calculateDemandSupplyGap("supply", "test")
    
    directly_predict(WP_gap, test_gap, "gap")
    directly_predict(WP_supply, test_supply, "supply")
    directly_predict(WP_demand, test_demand, "demand")
    use_supply_demand_predict_gap(WP_supply, WP_demand, test_gap)



    generatePrediction_Submission()
