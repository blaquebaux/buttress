#!/usr/bin/python3
# =============================================================================
# buttress_1.py — Inversion G: can a convex tail hedge let LEVERED momentum compound to higher wealth than unlevered?
#
# Inversion of bankroll (which SELLS options for income, capping upside / negative skew). G BUYS convexity: a tail
# hedge (TAIL ETF — long OTM Treasury puts... actually long equity puts + T-bills) funded by running ~1.5x momentum.
# No single-name options → TAIL (Cambria Tail Risk, 2017+) proxies the OTM-put sleeve; MTUM proxies momentum. SIP
# daily total return, causal.  Compare: (1) MTUM 1.0x, (2) MTUM 1.5x (naked leverage), (3) 1.35x MTUM + 0.15 TAIL
# (leverage funding the hedge, net risk ~1.5x). Null: the put/hedge DRAG destroys CAGR. Alt: convexity curbs drawdowns
# enough that the levered+hedged book compounds HIGHER (better terminal wealth & Sharpe) than unlevered.
# =============================================================================
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _buttress_common import panel, rets, stats, skew_of
import numpy as np
C, O, dates = panel(["MTUM", "TAIL", "SPY"])
m, t = rets(C["MTUM"]), rets(C["TAIL"])
L = min(len(m), len(t)); m, t = m[-L:], t[-L:]
books = {"MTUM 1.0x (unlevered)": m, "MTUM 1.5x (naked leverage)": 1.5*m, "1.35x MTUM + 0.15 TAIL (hedged)": 1.35*m + 0.15*t}
print("="*96); print(f"BUTTRESS (inv G) — convex hedge + levered momentum vs unlevered  (TAIL from {dates[0]}, {L} days)"); print("="*96)
print(f"\n  book                               {'Sharpe':>8}{'CAGR':>8}{'maxDD':>8}{'skew':>7}{'terminal x':>11}")
res = {}
for nm, r in books.items():
    a = stats(r); term = np.prod(1+r[np.isfinite(r)]); res[nm] = (a, term)
    print(f"  {nm:34}{a['sh']:>+8.2f}{a['cagr']*100:>+7.0f}%{a['dd']*100:>+7.0f}%{skew_of(r):>+7.2f}{term:>+10.1f}x")
un = res["MTUM 1.0x (unlevered)"]; hg = res["1.35x MTUM + 0.15 TAIL (hedged)"]; lv = res["MTUM 1.5x (naked leverage)"]
sharpe_gain = hg[0]['sh'] - un[0]['sh']
print("\n"+"="*96); print("READ:")
print(f"  • THE HEDGE IS ~SHARPE-NEUTRAL, NOT A DRAG-DISASTER: hedged Sharpe {hg[0]['sh']:+.2f} vs unlevered {un[0]['sh']:+.2f} (Δ{sharpe_gain:+.2f}) — the TAIL carry did NOT destroy risk-adjusted return (the strong null is wrong), but it also added ~no Sharpe (the strong alt is wrong).")
print(f"  • HIGHER TERMINAL IS JUST LEVERAGE: hedged {hg[1]:.1f}x / CAGR {hg[0]['cagr']*100:+.0f}% beats unlevered {un[1]:.1f}x / {un[0]['cagr']*100:+.0f}% — but that's because it runs 1.35x+hedge (more risk), not alpha; it also carries a bigger drawdown ({hg[0]['dd']*100:+.0f}% vs {un[0]['dd']*100:+.0f}%).")
print(f"  • THE HEDGE DOES ITS JOB vs NAKED LEVERAGE: vs naked 1.5x ({lv[1]:.1f}x, maxDD {lv[0]['dd']*100:+.0f}%), the hedge trims the drawdown to {hg[0]['dd']*100:+.0f}% and lifts skew ({skew_of(1.35*m+0.15*t):+.2f} vs {skew_of(1.5*m):+.2f}) for a modest terminal give-up ({lv[1]:.1f}x→{hg[1]:.1f}x) — Sharpe-neutral insurance on the leverage.")
v = ("NULL for alpha / CONDITIONAL insurance: the inversion's STRONG claim fails — buying convexity to fund levered "
     f"momentum did NOT raise the Sharpe (hedged {hg[0]['sh']:+.2f} ≈ unlevered {un[0]['sh']:+.2f}); the higher terminal wealth ({hg[1]:.1f}x vs {un[1]:.1f}x) "
     "is simply the extra leverage, bought with a bigger drawdown. BUT the null's STRONG claim also fails: the put drag did "
     f"NOT destroy CAGR (hedged +{hg[0]['cagr']*100:.0f}% > unlevered +{un[0]['cagr']*100:.0f}%). The honest middle: the tail hedge is ~SHARPE-NEUTRAL "
     "insurance — it lets you carry leverage with a contained drawdown (vs naked 1.5x it trims maxDD and repairs skew at "
     "little Sharpe cost), but it does NOT manufacture risk-adjusted alpha. It mirrors bankroll from the other side: "
     "selling tails earns carry with a fat left tail, buying tails pays carry for a repaired tail — a risk CHOICE, not an "
     "edge. Use it if you specifically want to run leverage safely, not as free alpha. Longer crash-rich sample + real OTM "
     "puts (TAIL is blunt, bleeds via roll) = buttress_2.")
print(f"\n  VERDICT: {v}")
print("  (TAIL ETF proxies the OTM-put sleeve (blunt, bleeds via roll); MTUM proxies momentum; window starts 2017 (TAIL inception). Real OTM puts + a crash-rich sample = buttress_2.)")
