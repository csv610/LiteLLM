#!/usr/bin/env python3
"""
Script to generate contract.md files for all recognizer modules with clear specifications and FAQs.
"""

import sys
from pathlib import Path

# Module configurations for contract generation
MODULE_CONFIGS = {
    "clinical_sign": {
        "name": "Clinical Sign Identifier",
        "description": "Identifies whether a given name is a recognized clinical sign in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes established clinical examination signs",
            "Identifies signs documented in major medical textbooks",
            "Validates signs used in clinical practice",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide detailed examination techniques",
            "Does not offer diagnostic guidance",
            "Cannot assess sign severity or urgency",
            "Limited to documented signs in training data"
        ],
        "failure_conditions": [
            "Ambiguous or poorly described signs",
            "Recently discovered signs not in literature",
            "Signs with multiple naming conventions",
            "Non-standard or made-up sign names"
        ],
        "examples": {
            "will_work": ["Babinski sign", "Kernig sign", "McMurray test", "Phalen test"],
            "may_fail": ["babsinki sign", "unknown test", "my made up sign", "vague symptom"]
        }
    },
    "disease": {
        "name": "Disease Identifier",
        "description": "Identifies whether a given name is a recognized disease in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes established diseases and disorders",
            "Identifies conditions documented in major medical databases",
            "Validates diseases listed in ICD-10/ICD-11",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide disease prognosis or treatment",
            "Does not offer diagnostic criteria",
            "Cannot assess disease severity or staging",
            "Limited to documented diseases in training data"
        ],
        "failure_conditions": [
            "Very rare or newly discovered diseases",
            "Diseases with multiple naming variants",
            "Experimental or research-only conditions",
            "Non-standard disease names"
        ],
        "examples": {
            "will_work": ["diabetes mellitus", "hypertension", "asthma", "coronary artery disease"],
            "may_fail": ["newly discovered syndrome", "rare genetic disorder", "experimental condition", "vague complaint"]
        }
    },
    "genetic_variant": {
        "name": "Genetic Variant Identifier",
        "description": "Identifies whether a given name is a recognized genetic variant in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes documented genetic mutations",
            "Identifies variants in major genetic databases",
            "Validates genetic nomenclature standards",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide clinical significance",
            "Does not offer inheritance patterns",
            "Cannot assess pathogenicity",
            "Limited to documented variants in training data"
        ],
        "failure_conditions": [
            "Novel or newly discovered variants",
            "Complex multi-gene variants",
            "Non-standard genetic nomenclature",
            "Variants with multiple naming systems"
        ],
        "examples": {
            "will_work": ["BRCA1 mutation", "cystic fibrosis ΔF508", "Huntington CAG repeat", "Factor V Leiden"],
            "may_fail": ["novel variant", "complex rearrangement", "non-standard name", "unpublished mutation"]
        }
    },
    "imaging_finding": {
        "name": "Imaging Finding Identifier",
        "description": "Identifies whether a given name is a recognized imaging finding in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes radiological findings",
            "Identifies imaging signs documented in radiology literature",
            "Validates common imaging terminology",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide imaging protocols",
            "Does not offer differential diagnosis",
            "Cannot assess finding severity",
            "Limited to documented findings in training data"
        ],
        "failure_conditions": [
            "Rare or specialized imaging findings",
            "Modality-specific terminology",
            "New imaging techniques",
            "Non-standard radiology terms"
        ],
        "examples": {
            "will_work": ["pulmonary nodule", "ground glass opacity", "brain tumor", "pulmonary embolism"],
            "may_fail": ["rare finding", "new technique", "vague description", "non-standard term"]
        }
    },
    "lab_unit": {
        "name": "Laboratory Unit Identifier",
        "description": "Identifies whether a given name is a recognized laboratory unit in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes standard laboratory units",
            "Identifies SI-compliant measurements",
            "Validates common lab terminology",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide reference ranges",
            "Does not offer unit conversions",
            "Cannot assess clinical significance",
            "Limited to documented units in training data"
        ],
        "failure_conditions": [
            "Specialized or rare lab units",
            "Non-standard abbreviations",
            "Research-only measurements",
            "Incorrectly formatted units"
        ],
        "examples": {
            "will_work": ["mg/dL", "cells/μL", "mmol/L", "U/L"],
            "may_fail": ["rare unit", "non-standard format", "research measurement", "incorrect abbreviation"]
        }
    },
    "medical_abbreviation": {
        "name": "Medical Abbreviation Identifier",
        "description": "Identifies whether a given name is a recognized medical abbreviation in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes common medical abbreviations",
            "Identifies standard medical acronyms",
            "Validates widely used abbreviations",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide full terminology expansion",
            "Does not offer context-dependent meanings",
            "Cannot resolve ambiguous abbreviations",
            "Limited to documented abbreviations in training data"
        ],
        "failure_conditions": [
            "Specialty-specific abbreviations",
            "Institution-specific acronyms",
            "Newly created abbreviations",
            "Ambiguous short forms"
        ],
        "examples": {
            "will_work": ["COPD", "MRI", "ECG", "CBC"],
            "may_fail": ["hospital-specific", "new abbreviation", "ambiguous acronym", "specialty-specific"]
        }
    },
    "medical_coding": {
        "name": "Medical Coding Identifier",
        "description": "Identifies whether a given name is a recognized medical coding system in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes major coding systems",
            "Identifies standard medical terminologies",
            "Validates coding classifications",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide specific codes",
            "Does not offer coding guidelines",
            "Cannot perform code assignment",
            "Limited to documented systems in training data"
        ],
        "failure_conditions": [
            "Specialized coding systems",
            "Country-specific classifications",
            "New or experimental coding systems",
            "Non-standard terminologies"
        ],
        "examples": {
            "will_work": ["ICD-10", "CPT", "SNOMED CT", "LOINC"],
            "may_fail": ["specialty system", "new coding", "country-specific", "experimental classification"]
        }
    },
    "medical_condition": {
        "name": "Medical Condition Identifier",
        "description": "Identifies whether a given name is a recognized medical condition in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes medical conditions and disorders",
            "Identifies health states documented in literature",
            "Validates condition terminology",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide condition management",
            "Does not offer treatment guidelines",
            "Cannot assess condition severity",
            "Limited to documented conditions in training data"
        ],
        "failure_conditions": [
            "Newly described conditions",
            "Controversial diagnoses",
            "Cultural-specific conditions",
            "Non-standard terminology"
        ],
        "examples": {
            "will_work": ["hypertension", "diabetes", "asthma", "arthritis"],
            "may_fail": ["new condition", "controversial diagnosis", "cultural syndrome", "vague complaint"]
        }
    },
    "medical_device": {
        "name": "Medical Device Identifier",
        "description": "Identifies whether a given name is a recognized medical device in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes medical devices and equipment",
            "Identifies FDA-approved devices",
            "Validates device terminology",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide device specifications",
            "Does not offer usage instructions",
            "Cannot assess device safety",
            "Limited to documented devices in training data"
        ],
        "failure_conditions": [
            "New or experimental devices",
            "Country-specific devices",
            "Research equipment",
            "Non-standard device names"
        ],
        "examples": {
            "will_work": ["pacemaker", "ventilator", "CT scanner", "infusion pump"],
            "may_fail": ["experimental device", "new equipment", "research tool", "non-standard name"]
        }
    },
    "medical_pathogen": {
        "name": "Medical Pathogen Identifier",
        "description": "Identifies whether a given name is a recognized medical pathogen in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes disease-causing organisms",
            "Identifies documented pathogens",
            "Validates microbiological nomenclature",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide treatment guidelines",
            "Does not offer transmission information",
            "Cannot assess pathogen virulence",
            "Limited to documented pathogens in training data"
        ],
        "failure_conditions": [
            "Newly discovered pathogens",
            "Rare or regional organisms",
            "Non-standard nomenclature",
            "Research-only microorganisms"
        ],
        "examples": {
            "will_work": ["Staphylococcus aureus", "E. coli", "influenza virus", "SARS-CoV-2"],
            "may_fail": ["new pathogen", "rare organism", "non-standard name", "research microbe"]
        }
    },
    "medical_procedure": {
        "name": "Medical Procedure Identifier",
        "description": "Identifies whether a given name is a recognized medical procedure in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes medical procedures and surgeries",
            "Identifies documented interventions",
            "Validates procedure terminology",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide technique details",
            "Does not offer procedural guidelines",
            "Cannot assess procedure risks",
            "Limited to documented procedures in training data"
        ],
        "failure_conditions": [
            "New or experimental procedures",
            "Specialty-specific interventions",
            "Regional technique variations",
            "Non-standard procedure names"
        ],
        "examples": {
            "will_work": ["appendectomy", "coronary artery bypass", "hip replacement", "colonoscopy"],
            "may_fail": ["experimental procedure", "new technique", "specialty-specific", "non-standard name"]
        }
    },
    "medical_specialty": {
        "name": "Medical Specialty Identifier",
        "description": "Identifies whether a given name is a recognized medical specialty in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes medical specialties and subspecialties",
            "Identifies documented medical fields",
            "Validates specialty terminology",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide scope of practice",
            "Does not offer training requirements",
            "Cannot assess specialty overlap",
            "Limited to documented specialties in training data"
        ],
        "failure_conditions": [
            "New or emerging specialties",
            "Country-specific specialties",
            "Research-only fields",
            "Non-standard specialty names"
        ],
        "examples": {
            "will_work": ["cardiology", "neurology", "pediatrics", "anesthesiology"],
            "may_fail": ["new specialty", "country-specific", "research field", "non-standard name"]
        }
    },
    "medical_supplement": {
        "name": "Medical Supplement Identifier",
        "description": "Identifies whether a given name is a recognized medical supplement in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes dietary supplements and nutraceuticals",
            "Identifies documented supplements",
            "Validates supplement terminology",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide dosage information",
            "Does not offer efficacy data",
            "Cannot assess supplement safety",
            "Limited to documented supplements in training data"
        ],
        "failure_conditions": [
            "New or experimental supplements",
            "Region-specific products",
            "Research compounds",
            "Non-standard supplement names"
        ],
        "examples": {
            "will_work": ["vitamin D", "omega-3 fatty acids", "probiotics", "ginkgo biloba"],
            "may_fail": ["new supplement", "regional product", "research compound", "non-standard name"]
        }
    },
    "medical_symptom": {
        "name": "Medical Symptom Identifier",
        "description": "Identifies whether a given name is a recognized medical symptom in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes documented medical symptoms",
            "Identifies symptom terminology",
            "Validates symptom descriptions",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide diagnostic guidance",
            "Does not offer symptom management",
            "Cannot assess symptom severity",
            "Limited to documented symptoms in training data"
        ],
        "failure_conditions": [
            "Vague or poorly described symptoms",
            "Cultural-specific symptom expressions",
            "New or rare symptom presentations",
            "Non-standard symptom terminology"
        ],
        "examples": {
            "will_work": ["chest pain", "headache", "nausea", "shortness of breath"],
            "may_fail": ["vague complaint", "cultural symptom", "rare presentation", "non-standard term"]
        }
    },
    "medical_test": {
        "name": "Medical Test Identifier",
        "description": "Identifies whether a given name is a recognized medical test in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes medical tests and diagnostics",
            "Identifies documented laboratory tests",
            "Validates test terminology",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide test interpretation",
            "Does not offer reference ranges",
            "Cannot assess test accuracy",
            "Limited to documented tests in training data"
        ],
        "failure_conditions": [
            "New or experimental tests",
            "Specialty-specific diagnostics",
            "Research-only tests",
            "Non-standard test names"
        ],
        "examples": {
            "will_work": ["CBC", "MRI", "ECG", "blood glucose test"],
            "may_fail": ["experimental test", "specialty-specific", "research diagnostic", "non-standard name"]
        }
    },
    "medical_vaccine": {
        "name": "Medical Vaccine Identifier",
        "description": "Identifies whether a given name is a recognized medical vaccine in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes documented vaccines",
            "Identifies approved immunizations",
            "Validates vaccine terminology",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide vaccination schedules",
            "Does not offer efficacy data",
            "Cannot assess vaccine safety",
            "Limited to documented vaccines in training data"
        ],
        "failure_conditions": [
            "New or experimental vaccines",
            "Country-specific vaccines",
            "Research immunizations",
            "Non-standard vaccine names"
        ],
        "examples": {
            "will_work": ["influenza vaccine", "MMR", "COVID-19 vaccine", "hepatitis B vaccine"],
            "may_fail": ["experimental vaccine", "country-specific", "research immunization", "non-standard name"]
        }
    },
    "medication_class": {
        "name": "Medication Class Identifier",
        "description": "Identifies whether a given name is a recognized medication class in medical literature",
        "purpose": "Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs",
        "capabilities": [
            "Recognizes drug classes and categories",
            "Identifies documented medication groups",
            "Validates pharmacological terminology",
            "Provides confidence levels for recognition"
        ],
        "limitations": [
            "Cannot provide specific drug information",
            "Does not offer prescribing guidelines",
            "Cannot assess drug interactions",
            "Limited to documented classes in training data"
        ],
        "failure_conditions": [
            "New or experimental drug classes",
            "Country-specific classifications",
            "Research compounds",
            "Non-standard medication names"
        ],
        "examples": {
            "will_work": ["beta blockers", "NSAIDs", "statins", "antibiotics"],
            "may_fail": ["experimental class", "country-specific", "research compound", "non-standard name"]
        }
    }
}

def generate_contract_content(module_key, config):
    """Generate contract content for a module."""
    
    name = config["name"]
    description = config["description"]
    purpose = config["purpose"]
    capabilities = config["capabilities"]
    limitations = config["limitations"]
    failure_conditions = config["failure_conditions"]
    examples = config["examples"]
    
    # Generate FAQs based on module type
    faqs = generate_faqs(module_key, config)
    
    contract_content = f"""# {name} - Legal and Ethical Binding Contract

## LEGAL NOTICE AND BINDING AGREEMENT

**IMPORTANT**: This document constitutes a legally and ethically binding agreement between the user ("User") and the providers of this medical AI software ("Provider"). By using this {name} module, the User explicitly agrees to all terms, conditions, limitations, and responsibilities outlined in this contract.

**Effective Date**: {Path(__file__).stat().st_mtime if 'Path' in globals() else "Current Date"}
**Risk Classification**: HIGH-RISK MEDICAL AI SYSTEM
**Regulatory Compliance**: This software is classified as a medical device/software and may be subject to healthcare regulations.

---

## 1. PARTIES AND DEFINITIONS

**1.1 Provider**: The developers, maintainers, and distributors of this medical AI software.

**1.2 User**: Any individual, healthcare professional, or organization that uses this {name} module.

**1.3 Medical AI System**: This {name} module designed for medical terminology identification.

**1.4 Medical Decision**: Any clinical judgment, diagnosis, treatment decision, or patient care action.

---

## 2. OVERVIEW AND PURPOSE

**2.1 Description**: {description}

**2.2 Primary Purpose**: {purpose}

**2.3 Classification**: This module is classified as a **PRELIMINARY IDENTIFICATION TOOL** only.

**2.4 Intended Use**: Quick filtering of medical terminology to reduce computational costs and minimize AI hallucinations.

**2.5 EXCLUDED USES**: This module is NOT intended for:
- Clinical diagnosis or medical decision-making
- Patient care or treatment planning
- Emergency medical situations
- Substitute for professional medical judgment
- Legal or regulatory medical determinations

---

## 3. CAPABILITIES AND LIMITATIONS

### 3.1 What This Module CAN Correctly Do:

{chr(10).join(f"- {capability}" for capability in capabilities)}

### 3.2 What This Module CANNOT Do:

{chr(10).join(f"- {limitation}" for limitation in limitations)}

### 3.3 Failure Conditions - When This Module MAY FAIL:

{chr(10).join(f"- {condition}" for condition in failure_conditions)}

---

## 4. LEGAL OBLIGATIONS AND WARRANTIES

### 4.1 Provider Warranties:

The Provider warrants that:
- This module performs as described in Section 3.1
- The software is provided "AS IS" without any additional warranties
- The module is not intended for clinical decision-making
- All limitations and failure conditions are accurately disclosed

### 4.2 Provider DISCLAIMERS:

The Provider explicitly disclaims:
- Any warranty of fitness for medical purposes
- Any warranty of accuracy for clinical use
- Any warranty of suitability for patient care
- Liability for any medical decisions made using this software

### 4.3 User Acknowledgments:

By using this module, the User acknowledges and agrees that:
- This software is not a medical device for diagnosis or treatment
- The User will not rely on this software for medical decisions
- The User will verify all medical information through authoritative sources
- The User assumes full responsibility for any use of this software

---

## 5. ETHICAL OBLIGATIONS

### 5.1 User Ethical Responsibilities:

The User MUST:
- Use this module only as a preliminary identification tool
- Verify all medical terminology through authoritative medical sources
- Consult qualified healthcare professionals for all medical decisions
- Never use this software for emergency medical situations
- Report any misuse or adverse outcomes to appropriate authorities

### 5.2 Professional Use Requirements:

Healthcare professionals MUST:
- Maintain professional standards of care
- Use clinical judgment independent of this software
- Document verification of all medical information
- Follow all applicable medical regulations and standards
- Obtain informed consent when appropriate

### 5.3 Prohibited Uses:

The User is strictly prohibited from:
- Using this module for patient diagnosis or treatment
- Relying on this software for emergency medical care
- Making medical decisions based solely on this software
- Representing this software as a medical diagnostic tool
- Using this software in violation of medical regulations

---

## 6. LIABILITY AND INDEMNIFICATION

### 6.1 Limitation of Liability:

The Provider shall not be liable for:
- Any medical decisions made using this software
- Patient harm or adverse outcomes
- Errors or inaccuracies in module outputs
- Consequential, special, or punitive damages
- Any professional malpractice claims

### 6.2 User Indemnification:

The User agrees to indemnify and hold harmless the Provider from:
- Any claims arising from the User's use of this software
- Medical decisions made using this software
- Violation of these terms and conditions
- Professional malpractice related to software use

### 6.3 Risk Allocation:

The User acknowledges and accepts:
- All risks associated with using medical AI software
- Responsibility for verifying all medical information
- Full liability for medical decisions made
- The experimental nature of AI-based medical tools

---

## 7. COMPLIANCE AND REGULATORY REQUIREMENTS

### 7.1 Regulatory Compliance:

The User agrees to comply with:
- All applicable medical device regulations
- Healthcare privacy laws (HIPAA, GDPR, etc.)
- Professional medical standards and guidelines
- Local and national medical regulations
- Institutional review board requirements

### 7.2 Data Protection:

The User must ensure:
- Patient data privacy and confidentiality
- Compliance with healthcare data regulations
- Appropriate data handling and storage
- Secure transmission of medical information

### 7.3 Documentation Requirements:

The User must maintain:
- Records of software use in clinical contexts
- Documentation of verification processes
- Evidence of professional oversight
- Compliance with medical record standards

---

## 8. EXAMPLES AND EXPECTATIONS

### 8.1 Will Work Correctly:

{chr(10).join(f"- {example}" for example in examples["will_work"])}

### 8.2 May Fail - User Verification Required:

{chr(10).join(f"- {example}" for example in examples["may_fail"])}

### 8.3 User Action Requirements:

When results are uncertain or critical:
- STOP using the software for medical decisions
- VERIFY through authoritative medical sources
- CONSULT qualified healthcare professionals
- DOCUMENT verification process

---

## 9. TERM AND TERMINATION

### 9.1 Term:

This agreement remains in effect as long as the User uses this software.

### 9.2 Termination:

The Provider may terminate this agreement if:
- The User violates these terms and conditions
- The software is used for prohibited purposes
- Regulatory requirements necessitate termination
- Public safety concerns arise

### 9.3 Survival:

Obligations related to liability, confidentiality, and regulatory compliance survive termination.

---

## 10. DISPUTE RESOLUTION

### 10.1 Governing Law:

This agreement shall be governed by applicable medical device and healthcare regulations.

### 10.2 Dispute Resolution:

Disputes shall be resolved through:
- Good faith negotiation between parties
- Mediation by qualified medical legal experts
- Arbitration as required by medical device regulations
- Court proceedings only as last resort

### 10.3 Regulatory Reporting:

Both parties agree to:
- Report adverse events to appropriate authorities
- Comply with medical device reporting requirements
- Cooperate with regulatory investigations
- Maintain required documentation

---

## 11. USER FREQUENTLY ASKED QUESTIONS (FAQs)

{chr(10).join(f"### Q{i+1}: {faq['question']}\n\n**A**: {faq['answer']}\n" for i, faq in enumerate(faqs))}

---

## 12. SIGNATURE AND ACKNOWLEDGMENT

### 12.1 Electronic Agreement:

By using this {name} module, the User electronically signs this agreement and acknowledges:

- **I have read and understand this entire contract**
- **I agree to all terms, conditions, and limitations**
- **I understand this is not a medical diagnostic tool**
- **I will verify all medical information through authoritative sources**
- **I will consult healthcare professionals for medical decisions**
- **I accept full responsibility for my use of this software**
- **I understand the risks and limitations outlined herein**

### 12.2 Binding Effect:

This electronic agreement is legally binding and enforceable. The User's continued use of this software constitutes acceptance of all terms and conditions.

### 12.3 Professional Acknowledgment:

Healthcare professionals acknowledge that:
- Use of this software must comply with professional standards
- Clinical judgment remains the User's professional responsibility
- Patient welfare is the primary consideration
- Professional liability remains with the healthcare provider

---

## 13. CONTACT AND REPORTING

### 13.1 Technical Support:
- Report technical issues through project channels
- Document software behavior and error conditions
- Provide detailed information about failures

### 13.2 Medical Safety Reporting:
- Report adverse events to appropriate medical authorities
- Follow institutional incident reporting procedures
- Document patient safety concerns appropriately

### 13.3 Regulatory Compliance:
- Report regulatory violations or concerns
- Cooperate with medical device regulatory requirements
- Maintain compliance documentation

---

## 14. FINAL ACKNOWLEDGMENT

**THIS IS A LEGALLY AND ETHICALLY BINDING AGREEMENT**

By using this {name} module, you acknowledge that:
- Medical AI carries inherent risks and limitations
- This software is not a substitute for professional medical judgment
- You are legally responsible for your use of this software
- Patient safety and professional standards must be maintained
- Violation of these terms may result in legal consequences

**WARNING**: Failure to comply with these terms may result in patient harm, professional liability, regulatory action, and legal consequences.

---

**© 2024 Medical AI Software Provider**  
**All Rights Reserved**  
**This document is protected by copyright and intellectual property laws**

**IMPORTANT**: This contract is subject to change without notice. Continued use of the software constitutes acceptance of any modifications.
"""
    
    return contract_content

def generate_faqs(module_key, config):
    """Generate FAQs specific to each module type."""
    
    base_faqs = [
        {
            "question": "What does this module actually do?",
            "answer": f"This module quickly tells you if a medical term is recognized in medical literature. It's like a fast check before using more expensive AI tools."
        },
        {
            "question": "Can I use this for medical diagnosis?",
            "answer": "No. This module only identifies if a term is recognized - it does not provide diagnosis, treatment, or medical advice. Always consult healthcare professionals."
        },
        {
            "question": "How accurate is this module?",
            "answer": f"The module provides confidence levels but is not 100% accurate. It may fail with new, rare, or non-standard terms. Always verify important information."
        },
        {
            "question": "When might this module give wrong answers?",
            "answer": f"This module may fail with very new terms, rare conditions, non-standard names, or experimental procedures. Check the failure conditions above."
        },
        {
            "question": "What should I do if I'm not sure about the result?",
            "answer": "Verify the term through authoritative medical sources like textbooks, medical databases, or consult healthcare professionals."
        }
    ]
    
    # Add module-specific FAQs
    if module_key == "disease":
        base_faqs.extend([
            {
                "question": "Does this tell me if I have a disease?",
                "answer": "No. This only identifies if a disease name is recognized in medical literature. It cannot diagnose any medical condition."
            },
            {
                "question": "Can this recommend treatments?",
                "answer": "No. This module only identifies disease names and provides no treatment, prognosis, or medical recommendations."
            }
        ])
    elif module_key == "medical_symptom":
        base_faqs.extend([
            {
                "question": "Does this tell me what's causing my symptoms?",
                "answer": "No. This only identifies if a symptom is recognized in medical literature. It cannot determine causes or provide diagnosis."
            },
            {
                "question": "Should I use this for medical emergencies?",
                "answer": "No. For medical emergencies, contact emergency services immediately. This tool is not for emergency medical situations."
            }
        ])
    elif module_key == "lab_unit":
        base_faqs.extend([
            {
                "question": "Does this provide normal lab values?",
                "answer": "No. This only identifies if a laboratory unit is recognized. It does not provide reference ranges or interpret lab results."
            },
            {
                "question": "Can this convert between units?",
                "answer": "No. This module only identifies units but does not perform conversions or calculations."
            }
        ])
    elif module_key == "medical_pathogen":
        base_faqs.extend([
            {
                "question": "Does this diagnose infections?",
                "answer": "No. This only identifies if a pathogen name is recognized. It cannot diagnose infections or provide treatment."
            },
            {
                "question": "Can this tell me if I need antibiotics?",
                "answer": "No. This module only identifies pathogen names and provides no treatment recommendations or medical advice."
            }
        ])
    
    return base_faqs[:8]  # Return 5-8 FAQs

def create_contract_file(module_key, config):
    """Create contract.md file for a module."""
    recognizers_dir = Path(__file__).parent
    module_dir = recognizers_dir / module_key
    
    # Create contract file
    contract_file = module_dir / "contract.md"
    
    contract_content = generate_contract_content(module_key, config)
    
    with open(contract_file, 'w') as f:
        f.write(contract_content)
    
    return contract_file

def main():
    """Generate contract.md files for all recognizer modules."""
    print("Generating contract.md files for all recognizer modules...")
    
    created_files = []
    
    for module_key, config in MODULE_CONFIGS.items():
        print(f"Creating contract for {module_key}...")
        
        contract_file = create_contract_file(module_key, config)
        created_files.append(contract_file)
        print(f"✓ Created {contract_file}")
    
    print(f"\n✅ Generated {len(created_files)} contract files")
    print("\nAll contract files include:")
    print("- Clear capability specifications")
    print("- Detailed limitations and failure conditions")
    print("- Examples of when it works and fails")
    print("- 5-8 user-focused FAQs with simple answers")
    print("- Reliability statements and risk warnings")
    print("- User responsibility guidelines")
    print("- Professional medical disclaimers")

if __name__ == "__main__":
    main()
