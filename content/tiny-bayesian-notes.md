---
title: "A tiny Bayesian hello"
date: 2026-10-25
slug: tiny-bayesian-hello
type: writing
description: "A small test post for equations, Python, and friendly uncertainty."
tags: [math, python, bayesian]
draft: false
---

Suppose a model predicts a value $y$ from an input $x$. In a Bayesian view, the parameters are uncertain, so we care about the posterior:

$$
p(\theta \mid D) \propto p(D \mid \theta)\,p(\theta).
$$

The predictive mean is often easier to explain than a single magical number. I can approximate it with repeated stochastic forward passes:

```python
import numpy as np

def monte_carlo_mean(model, x, samples=32):
    """Keep dropout on and average several predictions."""
    predictions = [model(x, training=True) for _ in range(samples)]
    return np.mean(np.stack(predictions), axis=0)
```

The mean gives the center of the forecast. The spread of those samples is a small, useful signal that says: “the model is not sure here.”
