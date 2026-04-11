---
title: "Why and How of Heterogeneous treatment effects"
date: 2021-11-17T12:03:00-06:00
draft: true
categories: ["Technical"]
---

What are HTE:

Moderators

Why HTE:

Personalized treatments are better than avearge

Cherry picking under constraints - more common than expected -priotitization

1. HTE are interaction effects. can be estimated using regression but some problems
2. Exploding parameters. Power problems. 5 variables require 64 parameters.
3. Computational problems
4. Assumption of linearity in all interaction will overfit

Generalized Random forest

Problem with using trees for HTE is that we never observe both outcomes for a given x, so we cannot calculate treatment effect at a given node. 

To solve this:

Training data is divided into two - splitting data and estimating data

split criteria is made to maximize the treatment effect at the node

tree is build using splitting data but treatment effect estimates at each node is obtained by parsing the estimating data through the built tree and calculating the treatment effect.  This will make it consistent and asymptotically gaussian

contributiono f athey is that they prove the estimated treamtne effects are symptoticslly normal.

Difference with estimating treatment effects

1. 

[https://www.statworx.com/en/blog/machine-learning-goes-causal-ii-meet-the-random-forests-causal-brother/](https://www.statworx.com/en/blog/machine-learning-goes-causal-ii-meet-the-random-forests-causal-brother/)

[https://egap.org/resource/10-things-to-know-about-heterogeneous-treatment-effects/](https://egap.org/resource/10-things-to-know-about-heterogeneous-treatment-effects/)

[https://www.markhw.com/blog/causalforestintro](https://www.markhw.com/blog/causalforestintro)
