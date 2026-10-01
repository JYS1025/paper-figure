# Visual reference review

Viewed [DiffPool Figure 1](https://arxiv.org/html/1806.08804v4#S1.F1) before drafting. Irregular community hulls, explicit nodes, colored membership and shrinking graph cardinality carry the explanation. The composition is organized by the graph transformation rather than repeated generic module boxes.

Use an original eight-node graph and an explicit 8 × 3 assignment matrix. Connect color to repeated letter IDs so identity survives grayscale. The toy example uses hard assignments for legibility; DiffPool itself learns soft assignments. The pooled adjacency is computed from the stipulated original graph; diagonal mass counts internal edges twice and is not silently discarded. Reuse no source artwork.
