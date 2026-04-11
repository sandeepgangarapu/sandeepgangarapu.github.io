---
title: "Intuitive understanding of why Inverse propensity score reweighting works"
date: 2021-12-06T13:21:00-06:00
draft: true
tags: ["Statistics"]
categories: ["Technical"]
---

This post and concept related to design of experiments. For the scope of this article, I will assume the reader knows the basics of randomized control trials, randomization, need for experimentation etc.

Lets say there are just two groups in the RCT (Control, Treatment). Let's say the treatment effect is constant across individuals and known to us.  Let's assume its 10. Let's say there are two groups of people. Group1 has the propensity score of 0.75 for treatment and Group 2 has the propensity score of 0.5
