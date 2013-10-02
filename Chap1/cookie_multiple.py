from numpy.random import binomial
from numpy.random import uniform
from numpy.random import random_integers
from numpy import ones_like
import matplotlib.pyplot as plt

def main():
  # Define 5 coins. Each coin is represented by the parameter p
  coins = [0.05, 0.25, 0.65, 0.85]

  # These are our hypotheses. 5 hypotheses - we will be assuming that we are
  # picking any one of these coins. But say that is not true. Say that at each
  # step we decide randomly which coin we choose from a subset of these coins.
  # Can we find which coins were chosen? More so, if we choose one coin more
  # often than the others, does this reflect in our bayesian beliefs?

  chosen_coins = filter(lambda a: binomial(1, 0.5), coins)
  priors = [0.0, 0.50, 0.50, 0.0]

  print "Chosen Coins:"
  heads = 0
  total = 0

  # Perform some trials
  for x in xrange(10):
    # Choose a coin and flip it
    # coin_num = random_integers(0, len(chosen_coins)-1)
    # coin_result = binomial(1, chosen_coins[coin_num])
    coin_result = binomial(1, 0.45)

    # Get posteriors
    if coin_result == 1:
      temp = [a*b for (a,b) in zip(coins, priors)]
    else:
      temp = [a*b for (a,b) in zip([1-j for j in coins], priors)]

    # Check coins :P
    if coin_result == 1:
      heads += 1
    total += 1

    p_h = sum(temp)
    temp = [a/p_h for a in temp]
    priors = temp
    print coin_result, priors

  print priors
  print coins
  print chosen_coins
  print float(heads)/total

if __name__ == '__main__':
  main()
