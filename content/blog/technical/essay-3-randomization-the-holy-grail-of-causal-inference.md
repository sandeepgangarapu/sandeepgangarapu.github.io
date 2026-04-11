---
title: "Essay 3 - Randomization - the holy grail of causal inference"
date: 2020-08-18T00:00:00-06:00
draft: false
categories: ["Technical"]
series: ["Essays on Causal Inference"]
---

Going back to the red car example, how would we establish the causal effect of red colored car on accidents. In an ideal scenario, we select a random set of drivers and give them a red car to drive for x days and record the total number of accidents. We then go back in the time machine and give the exact set of drivers a grey car to driver and see if the accidents are less. This would give us a causal effect. But unfortunately, this is not possible.

In reality, we could randomly select drivers who already have red cars, observe their characteristics, and pick drivers of other cars who have exactly same characteristics as those of the red car drivers. We then track both of them for a period of x days, see the difference in the number of accidents and find the causal effect.

For example, Red cars may have all young drivers, so we pick young drivers but those who own other color cars. Red cars may have drivers who drive fast. We need to pick drivers of other color cars who are also drive fast. But how do we define fast? Do we ask them? Do we set average speed limit? May be they are driving in different kinds of roads. This seems difficult, but still possible to do. Red card may have reckless drivers. How do we define recklessness? Do we look at speeding tickets and infractions?

As you can see, creating a control group to establish the causal effect looks so hard. This is where randomization comes in.

{{< figure src="/images/blog/technical/essay-3-randomization-the-holy-grail-of-causal-inference/coin.png" alt="Coin toss illustration" align="center" >}}

Let’s take a bunch of drivers and randomly assign them to a red car or other color cars using a coin toss. Given them their assigned cars for x days. Then, compare the number of accidents and establish the causal effect.

Because of randomization, young drivers have equal chance to be in both red car group or other car group. Fast drivers had equal probability to be put in either of groups. Even reckless drivers would have the same propensity to be in either groups. Not just these three features, any thinkable feature of a driver has equal probability to be put in both groups.

In theory, both groups are balances and fair and now we can establish the true causal effect of driving a red car on accident incidence.

💡 One caveat, randomization does not guarantee balancing of all features in a given sample. But on average, it is expected to be balanced. Just like flipping coin 10 times does not guarantee 5 heads and 5 tails all the time, but on average, it does.
