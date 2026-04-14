import json

def cleanup():
    path = "data/source_of_truth.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Issue 1: Encoding corruption recursively
    def fix_encoding(obj):
        if isinstance(obj, str):
            obj = obj.replace("â€\"", "–")
            obj = obj.replace("â€“", "–")
            obj = obj.replace("â€”", "—")
            obj = obj.replace("â†'", "→")
            obj = obj.replace("â€™", "’") # Common quote issue
            obj = obj.replace("â€œ", "“")
            obj = obj.replace("â€", "”")
            return obj
        elif isinstance(obj, list):
            return [fix_encoding(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: fix_encoding(v) for k, v in obj.items()}
        return obj

    data = fix_encoding(data)

    # Issue 2: Citi highlights
    citi_bullets = [
        "Architected automated ETL pipelines (Python/Pandas) ingesting P95 telemetry from 6,000+ endpoints (BMC TrueSight/TSCO), replacing legacy manual processes.",
        "Designed optimized Oracle schemas for historical retention, enabling seasonal risk forecasting.",
        "Developed ML forecasting models (Prophet, scikit-learn) predicting capacity bottlenecks 6 months ahead with 90%+ accuracy, improving provisioning lead time.",
        "Built hybrid AWS/Oracle data platform: S3 landing zone for raw telemetry from 6,000+ endpoints, AWS Glue for ETL, and Redshift for ML forecasting workloads.",
        "Containerized Python ETL pipeline jobs on EC2/ECS, enabling scalable on-demand processing for capacity forecasting.",
        "Migrated heavy ML forecasting workloads (Prophet, scikit-learn) from on-prem Oracle to Redshift, enabling parallel forecasting at cloud scale.",
        "Integrated disparate monitoring feeds (TrueSight, CA Wily, AppDynamics) into unified Oracle reporting with executive dashboards.",
        "Identified underutilized infrastructure via data mining across 6,000+ endpoints, driving hardware consolidation and measurable cost savings.",
        "Managed dual APM environments (CA Wily 9.7/10.5, AppDynamics) and enterprise capacity planning across banking infrastructure.",
        "Developed interactive Streamlit/matplotlib/seaborn/plotly dashboards surfacing real-time capacity insights for senior stakeholders."
    ]

    for exp in data.get("experiences", []):
        if exp.get("company", "").upper() == "CITI":
            exp["highlights"] = citi_bullets
            
        # Issue 3: exclude_from_resume
        company_clean = exp.get("company", "").lower()
        if "simplex international" in company_clean or "humber college" in company_clean:
            exp["exclude_from_resume"] = True

    # Issue 4: Legacy skills
    legacy_skills_list = [
        "cobol", "microfocus cobol", "cvs", "clearcase", "star team", 
        "tso", "cics", "uss", "corba", "vb6", "vc++", "tuxedo", "jolt", 
        "maestro", "quickselect", "ps2pdf", "syncsort", "focus", 
        "amdocs cc", "mq series", "life ray portal", "mercury test director", 
        "ipcs", "semaphores", "locks", "uml", "rational rose", "awk", "sed"
    ]

    for skill in data.get("skills", []):
        name = skill.get("name", "").lower()
        if skill.get("years") is None:
            if name in legacy_skills_list:
                if name == "mq series" and skill.get("last_used") is not None:
                    pass
                else:
                    skill["legacy"] = True

    # Issue 5: Fix null years
    fixes = {
        "c": {"years": 15, "last_used": "2007"},
        "c#": {"years": 3, "last_used": "2011"},
        "postgresql": {"years": 3, "last_used": "2017"},
        "db2": {"years": 2, "last_used": "2008"},
        "mysql": {"years": 2, "last_used": "2010"},
        "jmx monitoring": {"years": 2, "last_used": "2011"},
        "appdynamics": {"years": 5, "last_used": "2025"},
        "matplotlib": {"years": 8, "last_used": "2025"},
        "seaborn": {"years": 6, "last_used": "2025"},
        "plotly": {"years": 6, "last_used": "2025"}
    }
    
    for skill in data.get("skills", []):
        name = skill.get("name", "").lower()
        if name in fixes and skill.get("years") is None:
            skill["years"] = fixes[name]["years"]
            skill["last_used"] = fixes[name]["last_used"]

    # Issue 6: Tighten professional summary long
    if "professional_summary" in data:
        data["professional_summary"]["long"] = "Senior Data Engineer and AI practitioner with 20+ years of enterprise IT experience spanning data engineering, cloud infrastructure, and performance engineering. Expert in Python/PySpark ETL pipeline design, AWS serverless architectures (Glue, Athena, S3, Bedrock), and ML-driven capacity forecasting (Prophet, scikit-learn). At Citi (Nov 2017–Dec 2025), built production pipelines ingesting telemetry from 6,000+ endpoints, migrated ML workloads to Redshift, and developed GenAI Text-to-SQL agents using Claude 3 Sonnet. Currently self-studying Databricks (Delta Lake, DLT, Unity Catalog), dbt, and Snowflake to bridge toward modern lakehouse roles. U.S. Citizen, no sponsorship required, based in Murphy, TX (Dallas–Fort Worth area)."

    # Issue 7: Project timeframe
    for p in data.get("projects", []):
        if p.get("name") == "Serverless Lakehouse Platform (AWS)" and p.get("timeframe") == "Recent":
            p["timeframe"] = "2025"

    # Issue 8: Preferred title
    if "personal_info" in data:
        data["personal_info"]["preferred_title"] = "Senior Data Engineer | AWS Data Platform & AI/ML Pipeline Specialist"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    cleanup()
