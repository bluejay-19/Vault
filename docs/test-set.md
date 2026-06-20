# Vault - Frank AI Exam Set & Evaluation Approach 

## Exam Set (Test Scenarios)

These are test scenarios for validating Frank's roast logic against real spending data patterns. Each scenario describes a data condition and what Frank's response should correctly reflect.
 
1. **Normal month, clear biggest category** — User spent across 5 categories with one clearly dominant (e.g. Rent 50%+). Frank should correctly name that category as the biggest. - PASS (Test 1: Rent correctly identified)

2. **Overspent badly** — Total spent significantly exceeds budget (e.g. 130% of budget). Frank should call out the overspend with the correct percentage. - PASS (Test 1: correctly flagged $495 over budget)

3. **Underspent / doing well** — Total spent is well under budget (e.g. 60% of budget). Frank's tone should reflect genuine (if backhanded) approval, not a generic roast. - PASS (Test 4: mathematically correct, but tone can be affected by cumulative test data poisoning)

4. **Tied categories** — Two categories have identical or near-identical totals. Frank should handle this gracefully, not just arbitrarily pick one without acknowledging the closeness. - PASS (Test 2: Food/transport both surfaced, no false tie-break issue)

5. **Zero-spend category** — One or more categories are $0 for the month. Frank should not reference a $0 category as notable or "biggest." - PASS (Test 2: Rent/Entertinment $0, not referenced as biggest)

6. **Negative net savings** — User withdrew from savings this month. Frank should acknowledge this distinctly from simply "low savings."

7. **High income, low spending** — Large gap between income and spend. Frank should recognize this as a strong month, not roast generically.

8. **First month, no comparison data** — Only one month of data exists. Frank should not reference "last month" or trends that don't exist. - PASS ( Test 3: "No previous data" shown correctly)

9. **Extreme/unrealistic values** — A category with an implausibly large number (e.g. $999,999). Frank's response should remain coherent and not break formatting. - PASS functionality (no crash, correct math), FAIL COSMETICALLY (see donut cahrt bug note below)

10. **Minimal data — one category only** — User only logged spending in a single category. Frank should still produce a coherent roast without referencing categories that have no data.

11. **Budget exactly met** — Total spent equals budget exactly (100%). Frank should note this as "right on the edge," not "over" or "under." - PASS (Test 6: $200 spent = $2000 budger, no crash; minor note Frank's wording leans "over" rather than "exactly on target" - low priority prompt tweak)

12. **Very small total spend** — User logged a near-empty month (e.g. $40 total). Frank should not generate a roast implying heavy spending. - PASS ( Test 3: $35 total, Frank didn't imply heavy spending)

13. **Multiple months, improving trend** — Spending has decreased month over month across 3+ months. Frank should be able to reference positive trend direction.

14. **Multiple months, worsening trend** — Spending has increased steadily. Frank should call out the trend, not just the single month.

15. **Category name edge case** — A less common category present (e.g. "Medical" or "Subscriptions"). Frank should reference it naturally, not awkwardly.

16. **Income missing or zero** — Edge case where income field is 0 (possibly unemployed user, or data entry skipped). Frank's response should not divide-by-zero or break when calculating ratios involving income.

17. **Net savings far exceeds income** — Data inconsistency (more saved than earned). Frank shouldn't break, even on logically odd input.

18. **All categories roughly equal** — Spending evenly spread, no single dominant category. Frank should note the lack of a clear "problem area" rather than forcing one.

19. **Re-roast / "Another roast" button** — Same data, second generation. Response should be meaningfully different in wording from the first, not a near-duplicate.

20. **Currency/number formatting check** — Large numbers (e.g. $12,450.75) should be referenced by Frank in a readable way, not as raw unformatted floats. - PASS (partially observed, large numbers displayed corectly with commas (e.g. $1,000,510.00), no formatting bugs seen)

### Bugs
BUGS FOUND:
1. Donut chart label overlap — when category values are extremely small 
   relative to the dominant category (e.g. <0.03%), their percentage labels 
   stack and overlap illegibly above the chart. Reproduced in Test 4. Fix: 
   filter/hide labels below a minimum threshold, or suppress labels for 
   slices under ~1%.

2. "vs Last Month" and "Net Savings to Date" can show extreme or misleading 
   values when test/real data has drastically different scales between 
   consecutive months (e.g. +43495.2%). Math is correct, but the UX reads 
   as broken to users. Consider capping displayed percentage or adding 
   a tooltip/disclaimer for outlier swings.

TESTING SUMMARY: 8 of 20 scenarios tested across 6 uploads on one test 
account. Remaining scenarios to be tested incrementally during Day 6 
bug triage.