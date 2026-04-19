---
title: "Essays on Causal Inference"
date: 2022-10-29T15:30:00-06:00
draft: false
tags: ["Technical"]
series: ["Essays on Causal Inference"]
---

## The fundamental problem of causal inference

You probably know the COVID-19 pandemic and the race between all the pharma companies to create a vaccine. There was a lot of talk about different phases of clinical trials and the effectiveness of various vaccines. In clinical trials, companies are trying to estimate the causal effect of giving a drug on patient's health.

{{< figure src="/images/blog/technical/essay-1-the-fundamental-problem-of-causal-inference/coronavirus.png" alt="Coronavirus illustration" align="center" >}}

{{< figure src="/images/blog/technical/essay-1-the-fundamental-problem-of-causal-inference/flask.png" alt="Flask illustration" align="center" >}}

Causal effect is the difference between what happened if the treatment was given and what would have happened if the treatment was not given

or

Causal effect is the difference between what would have happened if the treatment was given and what happened if the treatment was not given

In both definitions, only one condition (treatment or control) is observable for any given person. It is impossible to get a determinate value of the effect of treatment on a given unit. This is called the fundamental problem of causal inference.

Let's look at an example. Netflix wants to advertise its marquee show Squid Games by placing billboards all over New York City. They want to evaluate the effect of placing billboards on subscriber growth. They put billboards at the start of the month and simultaneously released the show on Netflix. They see the subscribers from New York increase by 15% month on month. The program manager in charge of this project claims that the effect of billboards is 15% subscription growth, and they should implement this program everywhere. However, this doesn't seem right for so many reasons.

1. There could be a lockdown, and no one saw billboards. The reason why subscriber growth happened is that people were bored and subscribed to Netflix.
2. There was a massive buzz on the Internet about Squid games. This prompted a lot of NY folks to sign up for Netflix.
3. Netflix was growing month on month anyway and people would have signed up even in the absence of billboards.

The only way to estimate the effect of placing billboards is if we had another universe where billboards were not present and Squid Games was released anyway. Unfortunately, we only have one universe, and we can only observe one side of the effect. This is the fundamental problem of causal inference.

{{< figure src="/images/blog/technical/essay-1-the-fundamental-problem-of-causal-inference/squid-game-illustration.png.webp" alt="Squid Game illustration" align="center" >}}

The entire field of causal inference is about trying to estimate what would have happened if treatment was not present and then calculate the treatment effect to understand the effectiveness of the intervention. Randomized control trials (AB Testing) does this by randomly allocating people to treatment and control. Regression does this by including every other possibility of the effect in the regression equation and controlling for it. Differences in differences looks for a control group which was similar to treatment before the intervention but did not receive the treatment.

## What is a causal effect?

Let's take a look at this chart.

{{< figure src="https://s3-eu-west-1.amazonaws.com/candela-iglesias/comfy/cms/files/files/000/000/014/original/sharks.png" alt="Chart showing correlation between ice cream sales and shark attacks" align="center" >}}

There is a perfect association between ice cream sales and shark attacks at the beach. When ice cream sales go up, shark attacks go up and when ice cream sales go down, shark attacks go down.

{{< figure src="/images/blog/technical/essay-2-what-is-a-causal-effect/shark.png" alt="Shark illustration" align="center" >}}

{{< figure src="/images/blog/technical/essay-2-what-is-a-causal-effect/ice-cream.png" alt="Ice cream illustration" align="center" >}}

If we were to take this association seriously, in order to lessen shark attacks for public safety, we would cut down on the number of ice cream shops at the beach. Of course, this would not work. The hidden story is that more people go to the beach in the summer and this increases both the probaility of a shark attack and ice cream sales. In order to attribute the effect of ice cream sales on shark attacks, we need to establish that the effect is because of the ice cream sales, not just associated with ice cream sales.

Correlation is not causation! The causal effect is the effect produced by the treatment and not just associated with the treatment.

Let's look at another example.

Red cars have a 7 percent higher risk of an accident [1].

{{< figure src="/images/blog/technical/essay-2-what-is-a-causal-effect/accident.png" alt="Car accident illustration" align="center" >}}

If the color of the car is responsible for accidents because of visibility and that other traffic signs are also red, then it is a causal effect. If it is because young, fast and reckless drivers prefer red color car and then cause accidents, then it is not a causal effect. But it is important to know the causality from the perspective of policy. If it is indeed causal effect, it makes sense to pass a legislation restricting the sale of red cars or repainting existing cars. If it is not, all that effort would be worthless.

[https://www.citywidelaw.com/los-angeles-car-accident-attorney/car-color-and-crash-risk/](https://www.citywidelaw.com/los-angeles-car-accident-attorney/car-color-and-crash-risk/)

## Randomization - the holy grail of causal inference

Going back to the red car example, how would we establish the causal effect of red colored car on accidents. In an ideal scenario, we select a random set of drivers and give them a red car to drive for x days and record the total number of accidents. We then go back in the time machine and give the exact set of drivers a grey car to driver and see if the accidents are less. This would give us a causal effect. But unfortunately, this is not possible.

In reality, we could randomly select drivers who already have red cars, observe their characteristics, and pick drivers of other cars who have exactly same characteristics as those of the red car drivers. We then track both of them for a period of x days, see the difference in the number of accidents and find the causal effect.

For example, Red cars may have all young drivers, so we pick young drivers but those who own other color cars. Red cars may have drivers who drive fast. We need to pick drivers of other color cars who are also drive fast. But how do we define fast? Do we ask them? Do we set average speed limit? May be they are driving in different kinds of roads. This seems difficult, but still possible to do. Red card may have reckless drivers. How do we define recklessness? Do we look at speeding tickets and infractions?

As you can see, creating a control group to establish the causal effect looks so hard. This is where randomization comes in.

{{< figure src="/images/blog/technical/essay-3-randomization-the-holy-grail-of-causal-inference/coin.png" alt="Coin toss illustration" align="center" >}}

Let's take a bunch of drivers and randomly assign them to a red car or other color cars using a coin toss. Given them their assigned cars for x days. Then, compare the number of accidents and establish the causal effect.

Because of randomization, young drivers have equal chance to be in both red car group or other car group. Fast drivers had equal probability to be put in either of groups. Even reckless drivers would have the same propensity to be in either groups. Not just these three features, any thinkable feature of a driver has equal probability to be put in both groups.

In theory, both groups are balances and fair and now we can establish the true causal effect of driving a red car on accident incidence.

> 💡 One caveat, randomization does not guarantee balancing of all features in a given sample. But on average, it is expected to be balanced. Just like flipping coin 10 times does not guarantee 5 heads and 5 tails all the time, but on average, it does.

See [this](/resources/) page for more learning resources on Causal Inference.
