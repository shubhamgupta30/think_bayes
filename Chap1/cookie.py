from numpy.random import binomial
from numpy.random import uniform
from numpy import ones_like
import matplotlib.pyplot as plt

jar1_h = 0.55
jar2_h = 0.56

def jar1():
  # This jar has 30 vanilla cookies and 10 Chocolate cookies
  return binomial(1, jar1_h)

def jar2():
  # This jar has 20 vanilla cookies and 20 chocolate cookies
  return binomial(1, jar2_h)

def pickAJar():
  jarNum = binomial(1, 0.5)
  if jarNum == 0:
    print "Picked Jar 1"
    return jar1
  print "Picked Jar 2"
  return jar2

def main():
  # pick a jar randomly
  jar = pickAJar()

  # start with a random prior
  eps = 0.00001
  prior_jar1 = uniform(0+2*eps, 1-2*eps)
  prior_jar2 = 1 - prior_jar1
  num_trials = []

  # Perform the same experiment for a given prior 1000 times to find number of trials needed
  for x in xrange(10000):
    p_jar1 = prior_jar1
    p_jar2 = prior_jar2
    trials = 0

    # perform trials till one of the probability fall below eps
    while(p_jar1 > eps and p_jar2 > eps):
      trials += 1
      outcome = jar()
      if outcome == 1:
        p_h = jar1_h * p_jar1 + jar2_h * p_jar2
        p_jar1 = (jar1_h * p_jar1) / p_h
      if outcome == 0:
        p_t = (1-jar1_h) * p_jar1 + (1-jar2_h) * p_jar2
        p_jar1 = (((1-jar1_h) * p_jar1) / p_t)

      p_jar2 = 1 - p_jar1

    num_trials.append(trials)

  # Print a distribution chart
  count, bins, ignored = plt.hist(num_trials, 100, normed=True)
  plt.show()

if __name__ == '__main__':
  main()
