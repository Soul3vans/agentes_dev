---
name: iron-verify
description: Force existence verification before claiming files, functions, endpoints or dependencies exist. Use whenever an agent is about to assert something about the repository or runtime. Reduces hallucinations.
---

# IRON Verify

Prevent hallucinations about the codebase.

## Hard rules

- Before asserting that a file, directory, function, class, endpoint or dependency exists, propose a concrete verification command (ls, find, grep, cat package.json, etc.).
- Only after real nion-cli output may the claim become KNOWN.
- If verification is not possible, label the claim REQUIRES_VERIFICATION or UNKNOWN.
- Never invent paths, signatures or libraries.

## Procedure

1. Identify the claim that needs verification.
2. Propose the exact command.
3. Wait for real output.
4. Relabel the claim as KNOWN, INFERRED, UNKNOWN or REQUIRES_VERIFICATION.
