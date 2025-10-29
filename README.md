# 🧠 AI Literacy Lab

> *Fluency sounds like truth until you test it.*

AI Literacy Lab is an open-source, audit-ready course that teaches humans to think critically about large language model outputs.  
Every lesson is falsifiable; every example is reproducible offline.

---

## 📘 Structure

| Folder | Purpose |
|:--|:--|
| 00_Environment_Setup | Build a local LLM container (no external APIs). |
| 01-07 Modules | Step-by-step lessons from fluency illusion → ethics. |
| sandbox/ | Reproducible failure demos with verification scripts. |
| resources/ | Key academic papers and readings. |
| .github/workflows/ | Continuous verification pipeline. |

---

## 🚀 Quick Start

```bash
cd 00_Environment_Setup
docker-compose up --build
# runs local LLM and executes pytest demos
```

Check results under /sandbox/; each verify.py asserts both the failure and the fix.

⸻

🧩 Curriculum Summary

See syllabus.md for detailed timeline and outcomes.
Highlights:
1. Plausibility ≠ Truth: token probability ≠ epistemic verification.
2. Prompt as Experiment: design falsifiable questions.
3. Verification as Practice: run reproducible cross-checks.
4. Ethics as Boundary: understand when not to trust the machine.

⸻

🧰 Contributing

Open 08_Community/CONTRIBUTING.md for the full style guide.
Every pull request must include:
- A runnable demo in /sandbox/
- A verification log (pytest output)
- A Verification Check section in the lesson README

⸻

📜 License

MIT — free to fork, teach, and modify.
Please retain attribution and cite original sources where used.

⸻

🔗 References

See /resources/reading_list.md for foundational research:
Bender et al. (2021), Raji et al. (2022), Lin et al. (2022), and others.

⸻

“Verify or Perish.”

---
