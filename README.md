# Blaque Baux Buttress

**Inversion G — can a convex tail hedge let LEVERED momentum compound to higher wealth than unlevered?**

> **Not investment advice.** Educational/research software. See [DISCLAIMER](DISCLAIMER.md) and [LICENSE](LICENSE).

```bash
python3 research/buttress_1.py   # needs Alpaca data keys in the environment
```

**Inversion G** (mirror of `bankroll`, which *sells* options). *Buy* convexity — a tail hedge (TAIL ETF) funded by running ~1.5× momentum (MTUM) — and ask whether the convexity curbs drawdowns enough that hedge-funded leverage beats unlevered momentum. No single-name options → TAIL proxies the OTM-put sleeve (2017+).

## Finding (null for alpha / Sharpe-neutral insurance)
| book | Sharpe | CAGR | maxDD | terminal |
|---|---|---|---|---|
| MTUM 1.0× | +0.79 | +16% | −34% | 4.0× |
| MTUM 1.5× (naked) | +0.79 | +23% | −48% | 6.8× |
| 1.35× MTUM + 0.15 TAIL | +0.80 | +20% | −41% | 5.6× |

- **Sharpe-neutral:** hedged +0.80 ≈ unlevered +0.79 — convexity added no risk-adjusted edge (strong alt fails).
- **But no drag-disaster either:** hedged CAGR +20% > unlevered +16% — the put carry did *not* destroy returns (strong null fails).
- **Higher terminal is just leverage**, bought with a bigger drawdown; vs naked 1.5× the hedge trims maxDD (−48→−41%) and repairs skew at little Sharpe cost.

## Verdict
**NULL for alpha / CONDITIONAL insurance.** The tail hedge is ~Sharpe-neutral — it lets you carry leverage with a contained drawdown, but it does *not* manufacture risk-adjusted alpha. It mirrors `bankroll` from the other side: selling tails earns carry with a fat tail, buying tails pays carry for a repaired tail — a risk *choice*, not an edge. Real OTM puts + a crash-rich sample = `buttress_2`.

## Status
**Research.** Honest inversion/negative test — the hypothesis checked against the data and the proxy's limits named. Alpaca SIP daily total return. No live capital.
