# Hesn-AI
**Closing the Critical Gap Between Emergency Resuscitation and Legal Accountability.**

---

## Executive Summary
In high-pressure medical environments, specifically during **Code Blue** (Cardiac Arrest) events, clinical teams are entirely focused on life-saving interventions. This intensity often results in fragmented or retrospective documentation, leading to critical inaccuracies in medication dosages, intervention timestamps, and provider identification. 

**Hesn-AI** is a multidisciplinary solution integrated into the **Crash Cart** workflow. It utilizes real-time AI transcription and voice biometrics to capture every verbal order and action, creating a legally admissible, timestamped, and verified audit trail without manual intervention.

## The Problem: The Documentation Vacuum
- **Clinical Risk:** Reliance on human memory post-event leads to "recall bias," compromising patient safety and future care quality.
- **Legal Vulnerability:** Incomplete or delayed records are legally interpreted as professional negligence or a breach of the "Duty of Care." 
- **Regulatory Non-compliance:** Current manual logging struggles to meet the rigorous standards required by health authorities and judicial auditors during malpractice inquiries.

## The Solution: How Hesn-AI Works
1. **Seamless Capture:** The system captures natural verbal commands during the crisis (e.g., "Starting CPR," "Administering 1mg Epinephrine").
2. **Biometric Verification:** Uses voice-print analysis to authenticate the provider, ensuring each entry is tied to a specific, verified individual.
3. **Automated Ledger:** Speech is instantly converted to text and logged into a chronological digital ledger integrated with the Patient’s Electronic Health Record (EHR).
4. **Smart Reports:** Generates comprehensive summaries including total duration, total dosages, and sequence of shocks for clinical debriefing and legal filing.

## Multidisciplinary Impact
- **Medical Teams (Doctors & Nurses):** Eliminates the cognitive load of manual scribing, allowing 100% focus on the patient while ensuring actions are legally protected.
- **Healthcare Facilities:** Minimizes malpractice risks, ensures regulatory compliance, and provides high-fidelity data for risk management.
- **Regulatory & Judicial Bodies:** Establishes a transparent, "gold standard" audit trail for any legal inquiries or quality audits.
- **Patients:** Enhances safety through precision and ensures their medical journey is documented with absolute integrity.

## Technical Architecture
- **Interface:** Built with **NiceGUI** (Python) for high-performance, low-latency interaction.
- **Core Engine:** **OpenAI Whisper (ASR)** for high-accuracy medical transcription.
- **Security:** **NumPy & SciPy** driven Signal Processing for biometric identity verification.

## Deployment
1. **Install Dependencies:**
   ```bash
   pip install nicegui openai numpy scipy
