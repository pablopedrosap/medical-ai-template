"""
Synthetic Medical Data Generator
---------------------------------
Generates realistic medical records for testing the AI pipeline.

NO REAL PATIENT DATA - All synthetic, generated with GPT-4o.

Usage:
    python generate_synthetic_data.py --count 10 --output sample_medical_records.json
    python generate_synthetic_data.py --count 50 --report_types praxis,vdc --complexity medium
"""

import argparse
import json
import random
from typing import List, Dict, Literal
from datetime import datetime, timedelta
from pathlib import Path

# Synthetic patient templates
PATIENT_NAMES = ["Patient A", "Patient B", "Patient C", "Patient D", "Patient E"]
OCCUPATIONS = ["Teacher", "Engineer", "Nurse", "Driver", "Accountant", "Chef", "Lawyer"]
MEDICAL_CONDITIONS = [
    "Hypertension", "Type 2 Diabetes", "Hyperlipidemia", "Asthma",
    "Osteoarthritis", "Depression", "GERD", "Hypothyroidism"
]

SURGICAL_HISTORY = [
    "Appendectomy", "Cholecystectomy", "Hernia repair",
    "Knee arthroscopy", "Cesarean section", "Tonsillectomy"
]

MEDICATIONS = [
    "Metformin", "Lisinopril", "Atorvastatin", "Metoprolol",
    "Omeprazole", "Levothyroxine", "Albuterol", "Sertraline"
]

# Medical episode templates
EPISODES_VDC = [
    {
        "chief_complaint": "Motor vehicle accident with whiplash injury",
        "diagnosis": "Cervical sprain, grade 2",
        "treatment": "Conservative management with NSAIDs and physical therapy",
        "expected_injury_days": 45,
        "expected_disability_points": 3
    },
    {
        "chief_complaint": "Fall from height resulting in ankle fracture",
        "diagnosis": "Bimalleolar ankle fracture",
        "treatment": "ORIF with plate and screws",
        "expected_injury_days": 90,
        "expected_disability_points": 8
    },
    {
        "chief_complaint": "Workplace injury - crush injury to hand",
        "diagnosis": "Multiple metacarpal fractures, soft tissue injury",
        "treatment": "Surgical fixation, hand therapy",
        "expected_injury_days": 120,
        "expected_disability_points": 12
    }
]

EPISODES_PRAXIS = [
    {
        "chief_complaint": "Chest pain",
        "diagnosis": "Acute coronary syndrome",
        "treatment": "PCI with stent placement",
        "allegation": "Delayed diagnosis of ACS",
        "lex_artis_met": True,
        "reasoning": "Patient presented with atypical symptoms; standard workup performed"
    },
    {
        "chief_complaint": "Abdominal pain",
        "diagnosis": "Appendicitis with perforation",
        "treatment": "Emergent appendectomy",
        "allegation": "Delayed surgical intervention",
        "lex_artis_met": False,
        "reasoning": "8-hour delay in CT scan despite peritonitis signs"
    },
    {
        "chief_complaint": "Postoperative infection",
        "diagnosis": "Surgical site infection, deep",
        "treatment": "Antibiotics, debridement",
        "allegation": "Improper sterile technique",
        "lex_artis_met": True,
        "reasoning": "Infection rate within expected range for procedure type"
    }
]


def generate_patient_demographics() -> Dict:
    """Generate realistic patient demographics."""
    age = random.randint(25, 75)
    sex = random.choice(["M", "F"])

    return {
        "patient_id": f"SYNTH-{random.randint(1000, 9999)}",
        "age": age,
        "sex": sex,
        "occupation": random.choice(OCCUPATIONS)
    }


def generate_medical_history() -> List[str]:
    """Generate realistic medical history."""
    num_conditions = random.randint(1, 4)
    conditions = random.sample(MEDICAL_CONDITIONS, num_conditions)

    # Add diagnosis years
    return [
        f"{condition} (diagnosed {random.randint(2015, 2023)})"
        for condition in conditions
    ]


def generate_surgical_history() -> List[str]:
    """Generate realistic surgical history."""
    if random.random() < 0.3:  # 30% have no surgical history
        return []

    num_surgeries = random.randint(1, 3)
    surgeries = random.sample(SURGICAL_HISTORY, min(num_surgeries, len(SURGICAL_HISTORY)))

    return [
        f"{surgery} ({random.randint(2010, 2022)})"
        for surgery in surgeries
    ]


def generate_medications() -> List[str]:
    """Generate realistic medication list."""
    if random.random() < 0.2:  # 20% take no regular medications
        return []

    num_meds = random.randint(1, 5)
    return random.sample(MEDICATIONS, min(num_meds, len(MEDICATIONS)))


def generate_episode_vdc() -> Dict:
    """Generate body damage assessment episode."""
    template = random.choice(EPISODES_VDC)
    base_date = datetime.now() - timedelta(days=random.randint(30, 365))

    return {
        "date": base_date.strftime("%Y-%m-%d"),
        "location": random.choice(["Hospital General", "Clinic San José", "Emergency Room"]),
        "chief_complaint": template["chief_complaint"],
        "diagnosis": template["diagnosis"],
        "treatment": template["treatment"],
        "expected_injury_days": template["expected_injury_days"],
        "expected_disability_points": template["expected_disability_points"],
        "evolution": "Patient improved with treatment, residual limitations persist.",
        "current_status": "Stable, ongoing rehabilitation"
    }


def generate_episode_praxis() -> Dict:
    """Generate malpractice episode."""
    template = random.choice(EPISODES_PRAXIS)
    base_date = datetime.now() - timedelta(days=random.randint(180, 730))

    return {
        "date": base_date.strftime("%Y-%m-%d"),
        "location": random.choice(["Hospital Universitario", "Private Clinic", "Emergency Department"]),
        "chief_complaint": template["chief_complaint"],
        "diagnosis": template["diagnosis"],
        "treatment": template["treatment"],
        "allegation": template["allegation"],
        "lex_artis_met": template["lex_artis_met"],
        "expected_conclusion": (
            "Standard of care was met. No malpractice identified."
            if template["lex_artis_met"]
            else "Deviation from standard of care identified."
        ),
        "reasoning": template["reasoning"]
    }


def generate_document_text(episode: Dict, demographics: Dict, med_history: List[str]) -> str:
    """Generate realistic medical document text."""

    doc_text = f"""EMERGENCY ROOM REPORT

Date: {episode['date']}
Location: {episode['location']}

PATIENT INFORMATION
Patient ID: {demographics['patient_id']}
Age: {demographics['age']} years
Sex: {demographics['sex']}
Occupation: {demographics['occupation']}

CHIEF COMPLAINT
{episode['chief_complaint']}

MEDICAL HISTORY
"""

    for condition in med_history:
        doc_text += f"- {condition}\n"

    doc_text += f"""
DIAGNOSIS
{episode['diagnosis']}

TREATMENT
{episode['treatment']}

EVOLUTION
{episode.get('evolution', 'Patient responded to treatment.')}

CURRENT STATUS
{episode.get('current_status', 'Stable')}
"""

    return doc_text


def generate_expected_report_vdc(demographics: Dict, episode: Dict, med_history: List[str]) -> Dict:
    """Generate expected VDC report structure."""

    return {
        "type": "vdc",
        "sections": {
            "antecedentes_medicos": f"{demographics['age']}-year-old {demographics['sex']} with history of: {', '.join(med_history)}",
            "cronologia": f"Injury occurred on {episode['date']} with diagnosis of {episode['diagnosis']}",
            "lesiones_secuelas": f"Residual limitations from {episode['diagnosis']}",
            "valoracion_dias": {
                "dias_impedimento": episode["expected_injury_days"],
                "puntos_secuela": episode["expected_disability_points"]
            },
            "conclusiones": "Assessment of body damage per Spanish legal tables (VDC)."
        }
    }


def generate_expected_report_praxis(demographics: Dict, episode: Dict, med_history: List[str]) -> Dict:
    """Generate expected Praxis report structure."""

    return {
        "type": "praxis",
        "sections": {
            "antecedentes_medicos": f"{demographics['age']}-year-old {demographics['sex']} with relevant history: {', '.join(med_history[:2])}",
            "cronologia_hechos": f"Patient presented on {episode['date']} with {episode['chief_complaint']}",
            "analisis_lex_artis": episode["reasoning"],
            "conclusiones": episode["expected_conclusion"]
        }
    }


def generate_synthetic_case(
    report_type: Literal["vdc", "praxis"],
    complexity: Literal["simple", "medium", "complex"] = "medium"
) -> Dict:
    """Generate a complete synthetic medical case."""

    demographics = generate_patient_demographics()
    med_history = generate_medical_history()
    surgical_history = generate_surgical_history()
    medications = generate_medications()

    if report_type == "vdc":
        episode = generate_episode_vdc()
        expected_report = generate_expected_report_vdc(demographics, episode, med_history)
    else:  # praxis
        episode = generate_episode_praxis()
        expected_report = generate_expected_report_praxis(demographics, episode, med_history)

    # Generate document text
    document_text = generate_document_text(episode, demographics, med_history)

    # Add complexity-based variations
    if complexity == "complex":
        # Add more documents for complex cases
        num_additional_docs = random.randint(3, 7)
        documents = [
            {
                "type": "Emergency Room Report",
                "date": episode["date"],
                "text": document_text
            }
        ]

        # Add follow-up documents
        for i in range(num_additional_docs):
            follow_up_date = datetime.strptime(episode["date"], "%Y-%m-%d") + timedelta(days=7*(i+1))
            documents.append({
                "type": random.choice(["Follow-up Note", "Lab Report", "Imaging Report"]),
                "date": follow_up_date.strftime("%Y-%m-%d"),
                "text": f"Follow-up {i+1}: Patient progress noted. Continuing treatment plan."
            })
    else:
        documents = [
            {
                "type": "Emergency Room Report",
                "date": episode["date"],
                "text": document_text
            }
        ]

    return {
        "case_id": f"CASE-{random.randint(10000, 99999)}",
        "report_type": report_type,
        "complexity": complexity,
        "patient_demographics": demographics,
        "medical_history": med_history,
        "surgical_history": surgical_history,
        "medications": medications,
        "current_episode": episode,
        "documents": documents,
        "expected_report": expected_report,
        "metadata": {
            "generated_date": datetime.now().isoformat(),
            "synthetic": True,
            "version": "1.0"
        }
    }


def generate_dataset(
    count: int,
    report_types: List[str] = ["praxis", "vdc"],
    complexity: str = "medium",
    output_file: str = "sample_medical_records.json"
) -> List[Dict]:
    """Generate a dataset of synthetic medical cases."""

    dataset = []

    for i in range(count):
        report_type = random.choice(report_types)
        case = generate_synthetic_case(report_type, complexity)
        dataset.append(case)

        print(f"Generated case {i+1}/{count}: {case['case_id']} ({report_type}, {complexity})")

    # Save to file
    output_path = Path(__file__).parent / output_file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Dataset saved to {output_path}")
    print(f"Total cases: {count}")
    print(f"Report types: {', '.join(set(c['report_type'] for c in dataset))}")
    print(f"Complexity levels: {', '.join(set(c['complexity'] for c in dataset))}")

    return dataset


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic medical data for testing")
    parser.add_argument("--count", type=int, default=10, help="Number of cases to generate")
    parser.add_argument(
        "--report_types",
        type=str,
        default="praxis,vdc",
        help="Comma-separated report types (praxis, vdc)"
    )
    parser.add_argument(
        "--complexity",
        type=str,
        default="medium",
        choices=["simple", "medium", "complex"],
        help="Case complexity level"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="sample_medical_records.json",
        help="Output filename"
    )

    args = parser.parse_args()

    report_types = [rt.strip() for rt in args.report_types.split(",")]

    print(f"Generating {args.count} synthetic medical cases...")
    print(f"Report types: {report_types}")
    print(f"Complexity: {args.complexity}")
    print()

    generate_dataset(
        count=args.count,
        report_types=report_types,
        complexity=args.complexity,
        output_file=args.output
    )


if __name__ == "__main__":
    main()
