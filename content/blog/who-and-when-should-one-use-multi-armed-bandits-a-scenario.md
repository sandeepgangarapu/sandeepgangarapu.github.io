---
title: "Who and when should one use Multi-Armed Bandits? A scenario."
date: 2020-10-11T23:13:00-06:00
draft: false
tags: ["Technical", "Intuition", "MAB"]
---

> 💡 This is a humor piece. I am using the scenario to communicate the use of MAB's. Please take it with a pinch of salt.

A manager at a tech company that sells Alphonso mangoes online is stuck with one of the most difficult decisions. What should the color of the "Buy Now" button be? She recently came to know that data-driven decision making is the new fad and wants to follow suit. She has a meeting with her team of data scientists and marketing folks. 

Manager: So what's the plan? 

Marketing folks: Based on our market research and intuition we narrowed down to these 3 colors and you can pick anything you like. 

Manager: Uh! but I want to make a data-driven decision. Data Science team, we pay you 6 figures. Give me a solution, not intuition.

DS team: Well, we could conduct A/B testing on the three colors and see which one performs the best and we can pick the winning color.

Manager: Wait a second, do you really trust the intuition of the Marketing folks, have you guys not come across all the anecdotal evidence that data is the king and how intuition can often be wrong. Where did you guys learn DS? A boot camp? I want to test all the primary, secondary, and colors in our corporate branding. I want to make a DATA-DRIVEN decision. 

DS Team: Well, it will be futile to conduct an A/B test on so many colors. First of all, we may not have so much traffic, so our test might be severely underpowered. Second, some users might find some colors so repulsive that they may not only not buy the delicious, heavenly Alphonso mangoes, they may never come back to our website.

Manager: Tell me what you can do. Not what you can't do. I WANT TO MAKE A DATA-DRIVEN DECISION.

DS Team: Well, we were saving this for a dooms day. But there is something we can do. 

Manager: What?

DS Team: We can use Multi-Armed Bandits. 

Manager: What even is that?

DS Team: Well, these are sequential and dynamic experimentation procedures.

Manger: That sounds fancy.

DS Team: We keep checking the best performing colors and send more users to those variants and minimize the loss. If we do this right by implementing the right algorithm we can minimize our losses while also identifying the best color or a set of colors.

Manager: Then go ahead and get me the data. I want to make a data driven decision. 

Marketing folks: No wonder AI will take our jobs. No one cares about our intuition anymore!
