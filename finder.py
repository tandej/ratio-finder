import argparse
import math

e12Values = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

tempArr = []
for val in e12Values:
    tempArr.append(val * 10)
e12Values.extend(tempArr)


def findSimpleRatio(ratio: float, biasPositive: bool, biasNegative: bool) -> str:
    maybeFlippedRatio: float = ratio

    if ratio == 0:
        return "Ratio of zero, aborting!"
    if ratio < 0:
        return "Ratio negative, aborting!"
    if ratio == 1:
        return "Ratio of one, aborting!"
    if ratio < 1:
        maybeFlippedRatio = 1 / maybeFlippedRatio
        print("Ratio less than 1, flipping!")

    exponent: int = int(abs(math.log10(maybeFlippedRatio)))

    trueMantissa = maybeFlippedRatio / (math.pow(10, exponent))

    closestMatch: float = 0
    closestMatchA: float = 0
    closestMatchB: float = 0

    for a in e12Values:
        for b in e12Values:
            approxMantissa: float = a / b

            if (
                not (trueMantissa - approxMantissa > 0 and biasPositive)
                and not (trueMantissa - approxMantissa < 0 and biasNegative)
                and (
                    abs(trueMantissa - approxMantissa)
                    < abs(trueMantissa - closestMatch)
                    or closestMatch == 0
                )
            ):
                closestMatch = approxMantissa
                closestMatchA = a
                closestMatchB = b

    closestMatchA = closestMatchA * (math.pow(10, exponent))

    errorPct = ((closestMatch - trueMantissa) / trueMantissa) * 100

    biasString = (
        " (biased positive)"
        if biasPositive
        else " (biased negative)" if biasNegative else ""
    )

    return (
        str(closestMatchA)
        + " "
        + str(closestMatchB)
        + " "
        + str(errorPct)
        + "%"
        + biasString
    )


def findDividerRatio(ratio: float) -> str:
    return "todo"


parser = argparse.ArgumentParser()
parser.add_argument(
    "ratio",
    help="ratio to target",
    type=float,
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-p",
    "--bias-positive",
    action="store_true",
    help="Biases result positive (e.g. such that the output ratio is AT LEAST the target)",
)
group.add_argument(
    "-n",
    "--bias-negative",
    action="store_true",
    help="Biases result negative (e.g. such that the output ratio is AT MOST the target)",
)

args = parser.parse_args()

print(findSimpleRatio(args.ratio, args.bias_positive, args.bias_negative))
