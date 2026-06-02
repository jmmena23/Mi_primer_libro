````markdown
# Central Limit Theorem

The Central Limit Theorem (CLT) states that the distribution of sample means approximates a normal distribution as the sample size gets larger, regardless of the population's actual distribution shape, provided the variance is finite.

## Mathematical Expression

Let $X_1, X_2, \dots, X_n$ be a random sample of size $n$ drawn from a population with mean $\mu$ and variance $\sigma^2$. Then, the random variable:

$$
Z = \frac{\bar{X} - \mu}{\frac{\sigma}{\sqrt{n}}}
$$ (eq-clt)

converges in distribution to a standard normal $N(0,1)$ as $n \to \infty$.

```{admonition} Important
:class: important

The sample size $n$ is generally considered large enough to apply the CLT when $n \ge 30$.
```

````
