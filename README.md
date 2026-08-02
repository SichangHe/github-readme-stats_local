# GitHub readme stats

`deploy.sh` downloads a locally generated language-card SVG to a candidate file.
`process_svg.py` accepts only well-formed cards with the expected content, changes
the title to “Most Owned Languages,” then atomically replaces the published SVG.
Rejected responses leave the published image untouched.

Run the regression checks with `python3 -m unittest`.
