# Teorema del Límite Central

El Teorema del Límite Central (TLC) establece que la distribución de las medias muestrales de una población con varianza finita se aproxima a una distribución normal a medida que el tamaño de la muestra aumenta, independientemente de la forma de la distribución de la población original.

## Expresión Matemática

Sea $X_1, X_2, \dots, X_n$ una muestra aleatoria de tamaño $n$ extraída de una población con media $\mu$ y varianza $\sigma^2$. Entonces, la variable aleatoria:

$$
Z = \frac{\bar{X} - \mu}{\frac{\sigma}{\sqrt{n}}}
$$ (eq-tlc)

converge en distribución a una normal estándar $N(0,1)$ cuando $n \to \infty$.

```{admonition} Importante
:class: important

El tamaño de la muestra $n$ suele considerarse suficientemente grande para aplicar el TLC cuando $n \ge 30$.
```
