# Drafting preflight regression controls

This file defines checks for the observed D3 failure. It does not replace blind evaluation.

## Required behavior

When notes contain a correlation coefficient but no p value, confidence interval, test direction, or explicit significance decision, the first draft must not add `유의한`, `유의미한`, `효과가 있다`, or `검증되었다`. It should either report the association without that claim or mark the missing inference `[확인 필요]`.

When a term or symbol has two supplied roles, the draft must state the roles separately and must not silently merge them.
