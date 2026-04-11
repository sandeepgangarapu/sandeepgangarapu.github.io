---
title: "Essay 1 - The fundamental problem of causal inference"
date: 2020-08-18T00:00:00-06:00
draft: false
categories: ["Technical"]
series: ["Essays on Causal Inference"]
---

You probably know the COVID-19 pandemic and the race between all the pharma companies to create a vaccine. There was a lot of talk about different phases of clinical trials and the effectiveness of various vaccines. In clinical trials, companies are trying to estimate the causal effect of giving a drug on patient’s health.

{{< figure src="/images/blog/technical/essay-1-the-fundamental-problem-of-causal-inference/coronavirus.png" alt="Coronavirus illustration" align="center" >}}

{{< figure src="/images/blog/technical/essay-1-the-fundamental-problem-of-causal-inference/flask.png" alt="Flask illustration" align="center" >}}

Causal effect is the difference between what happened if the treatment was given and what would have happened if the treatment was not given

or

Causal effect is the difference between what would have happened if the treatment was given and what happened if the treatment was not given

In both definitions, only one condition (treatment or control) is observable for any given person. It is impossible to get a determinate value of the effect of treatment on a given unit. This is called the fundamental problem of causal inference.

Let’s look at an example. Netflix wants to advertise its marquee show Squid Games by placing billboards all over New York City. They want to evaluate the effect of placing billboards on subscriber growth. They put billboards at the start of the month and simultaneously released the show on Netflix. They see the subscribers from New York increase by 15% month on month. The program manager in charge of this project claims that the effect of billboards is 15% subscription growth, and they should implement this program everywhere. However, this doesn’t seem right for so many reasons.

1. There could be a lockdown, and no one saw billboards. The reason why subscriber growth happened is that people were bored and subscribed to Netflix.
2. There was a massive buzz on the Internet about Squid games. This prompted a lot of NY folks to sign up for Netflix.
3. Netflix was growing month on month anyway and people would have signed up even in the absence of billboards.

The only way to estimate the effect of placing billboards is if we had another universe where billboards were not present and Squid Games was released anyway. Unfortunately, we only have one universe, and we can only observe one side of the effect. This is the fundamental problem of causal inference.

{{< figure src="/images/blog/technical/essay-1-the-fundamental-problem-of-causal-inference/squid-game-illustration.png.webp" alt="Squid Game illustration" align="center" >}}

The entire field of causal inference is about trying to estimate what would have happened if treatment was not present and then calculate the treatment effect to understand the effectiveness of the intervention. Randomized control trials (AB Testing) does this by randomly allocating people to treatment and control. Regression does this by including every other possibility of the effect in the regression equation and controlling for it. Differences in differences looks for a control group which was similar to treatment before the intervention but did not receive the treatment.
