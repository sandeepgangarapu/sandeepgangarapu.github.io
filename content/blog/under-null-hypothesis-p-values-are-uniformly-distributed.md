---
title: "Under null hypothesis, p-values are uniformly distributed"
date: 2022-10-06T16:44:00-06:00
draft: false
tags: ["Technical"]
---

Central limit theorem states that sample means follow normal distribution. People often confuse this with and question the validity of uniform distribution of p-values under nul hypothesis. Should we not be observing extreme p-values much less ofter than usual pvalues like 0.2 or 0.3?

Imagine if null hypothesis is true. This means there is no difference betweem treatment and control. 

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt
```

```python
pval_lis = []
t_stat_lis = []
samp_mean_lis = []

for i in range(100000):
    sample = np.random.normal(0, 1, 10)
    samp_mean = sample.mean()
    samp_mean_lis.append(samp_mean)
    t_stat = sample.mean()/(sample.std()/np.sqrt(sample.size))
    t_stat_lis.append(t_stat)
    pval = stats.t.sf(abs(t_stat), df=sample.size)*2
    pval_lis.append(pval)
```

```python
plt.hist(np.array(samp_mean_lis))
```

{{< figure src="/images/blog/technical/under-null-hypothesis-p-values-are-uniformly-distributed/output_2_1.png" alt="Histogram of sample means" caption="Distribution of sample means" align="center" >}}

```python
plt.hist(np.array(t_stat_lis))
```

{{< figure src="/images/blog/technical/under-null-hypothesis-p-values-are-uniformly-distributed/output_2_1-1.png" alt="Histogram of t-statistics" caption="Distribution of t-statistics" align="center" >}}

```python
plt.hist(np.array(pval_lis))
```

{{< figure src="/images/blog/technical/under-null-hypothesis-p-values-are-uniformly-distributed/output_3_1.png" alt="Histogram of p-values under the null hypothesis" caption="Distribution of p-values under the null hypothesis — uniformly distributed" align="center" >}}
