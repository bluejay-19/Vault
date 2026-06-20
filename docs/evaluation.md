# Evaluation Approach 
**Method:** Manual + semi-structured review against the test scenarios above. For each test file/scenario, generate Frank's roast and check it against these pass/fail criteria:
 
1. **Accuracy** — Does Frank correctly reference the actual biggest category, correct over/under budget status, and correct direction of trend (when applicable)? Target: 100% across all scenarios — this is non-negotiable since wrong numbers undermine the whole app's credibility.

2. **No crashes / no broken output** — Does the app handle edge cases (zero income, tied categories, single month) without errors or nonsensical text? Target: 100%.

3. **Tone consistency** — Does the response stay in Frank's blunt, witty voice rather than reverting to generic AI assistant tone? Target: subjective pass/fail per response, aiming for consistent voice across all 20 scenarios.

4. **Actionability** — Does Frank's response end with one concrete, genuine piece of advice (not just a joke)? Target: present in 100% of responses.

**Process:** Run each of the 20 scenarios through the Upload → Dashboard flow using small test CSVs, screenshot or copy Frank's output, and mark pass/fail against the four criteria above. Document any failures and the prompt adjustments made to fix them.
 