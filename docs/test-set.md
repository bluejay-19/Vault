# Vault - Frank AI Exam Set & Evaluation Approach 

## Exam Set (Test Scenarios)

These are test scenarios for validating Frank's roast logic against real spending data patterns. Each scenario describes a data condition and what Frank's response should correctly reflect.
 
1. **Normal month, clear biggest category** — User spent across 5 categories with one clearly dominant (e.g. Rent 50%+). Frank should correctly name that category as the biggest. 

2. **Overspent badly** — Total spent significantly exceeds budget (e.g. 130% of budget). Frank should call out the overspend with the correct percentage.

3. **Underspent / doing well** — Total spent is well under budget (e.g. 60% of budget). Frank's tone should reflect genuine (if backhanded) approval, not a generic roast.

4. **Tied categories** — Two categories have identical or near-identical totals. Frank should handle this gracefully, not just arbitrarily pick one without acknowledging the closeness.

5. **Zero-spend category** — One or more categories are $0 for the month. Frank should not reference a $0 category as notable or "biggest."

6. **Negative net savings** — User withdrew from savings this month. Frank should acknowledge this distinctly from simply "low savings."

7. **High income, low spending** — Large gap between income and spend. Frank should recognize this as a strong month, not roast generically.

8. **First month, no comparison data** — Only one month of data exists. Frank should not reference "last month" or trends that don't exist.

9. **Extreme/unrealistic values** — A category with an implausibly large number (e.g. $999,999). Frank's response should remain coherent and not break formatting.

10. **Minimal data — one category only** — User only logged spending in a single category. Frank should still produce a coherent roast without referencing categories that have no data.

11. **Budget exactly met** — Total spent equals budget exactly (100%). Frank should note this as "right on the edge," not "over" or "under."

12. **Very small total spend** — User logged a near-empty month (e.g. $40 total). Frank should not generate a roast implying heavy spending.

13. **Multiple months, improving trend** — Spending has decreased month over month across 3+ months. Frank should be able to reference positive trend direction.

14. **Multiple months, worsening trend** — Spending has increased steadily. Frank should call out the trend, not just the single month.

15. **Category name edge case** — A less common category present (e.g. "Medical" or "Subscriptions"). Frank should reference it naturally, not awkwardly.

16. **Income missing or zero** — Edge case where income field is 0 (possibly unemployed user, or data entry skipped). Frank's response should not divide-by-zero or break when calculating ratios involving income.

17. **Net savings far exceeds income** — Data inconsistency (more saved than earned). Frank shouldn't break, even on logically odd input.

18. **All categories roughly equal** — Spending evenly spread, no single dominant category. Frank should note the lack of a clear "problem area" rather than forcing one.

19. **Re-roast / "Another roast" button** — Same data, second generation. Response should be meaningfully different in wording from the first, not a near-duplicate.

20. **Currency/number formatting check** — Large numbers (e.g. $12,450.75) should be referenced by Frank in a readable way, not as raw unformatted floats.
