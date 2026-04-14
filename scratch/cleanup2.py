import json

def run_cleanup2():
    path = "data/source_of_truth.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Bullet data mapping based on company keywords
    updates = {
        "G6 HOSPITALITY": [
            "Managed Dynatrace AppMon/Synthetics monitoring for Brand.com and all critical hospitality systems.",
            "Led 'FAST' project: data-mined real-user performance metrics from Gomez Synthetic Monitoring to surface optimization recommendations adopted by engineering teams.",
            "Upgraded Dynatrace from 6.5 to 7.0 and enforced TLS 1.2 security — zero regression in production monitoring during cutover.",
            "Integrated HP Performance Center with Dynatrace, enabling unified load test + APM correlation.",
            "Implemented End-User Monitoring (EUM) and end-to-end transaction tracing across web and mobile.",
            "Participated in cloud migration planning to AWS, evaluating mobile monitoring tools and providing APM readiness assessment."
        ],
        "CA TECHNOLOGIES": [
            "Served as CA APM SME for TIAA-CREF, managing 50+ Enterprise Managers and 4,000–6,000 instrumented agents across the enterprise.",
            "Led large-scale CA APM upgrades (9.1 → 10.1) with zero unplanned downtime, coordinating cross-functional IT teams.",
            "Designed and implemented custom Management Modules — dashboards, alerts, SLA thresholds — adopted as standards across client environments.",
            "Built Perl/Ksh data-extraction scripts for automated performance reporting, replacing manual weekly exports.",
            "Provided sizing recommendations and Golden Image agent deployments, reducing onboarding time for new applications.",
            "Collaborated with J2EE/WebLogic performance teams to resolve bottlenecks identified via APM telemetry.",
            "Delivered client training programs and technical documentation adopted by internal CA and customer teams."
        ],
        "CORPUS": [
            "Developed high-availability multithreaded C++ billing interfaces using POSIX threads, mutex locks, semaphores, socket programming, and Marconi APIs — supporting telecom billing at Sprint scale.",
            "Delivered performance enhancements in C/C++/Pro*C/PL/SQL billing processes: reduced memory usage 75%, improved throughput 20%, and achieved 10x database performance via sequence optimization.",
            "Maintained and enhanced AMDOCS Flexible Bill Formatter, EDI interfaces, and Enabler/CSM/EMS modules across full billing lifecycle (invoicing, settlement, reporting).",
            "Reverse-engineered and documented undocumented AMDOCS PRM APIs to enable interface integration not supported by vendor.",
            "Designed interfaces using UML/Rational Rose; applied OO design patterns (Functors, Containers) to build reusable threading and socket utility libraries.",
            "Automated WebLogic/WebSphere system administration using Korn Shell scripting, eliminating manual deployment steps.",
            "Supervised test team using Mercury Test Director; led QA cycles and production bug triage for billing and CSM modules.",
            "Operated across HPUX, SunOS, and Linux environments; maintained code in CVS and ClearCase throughout 6-year engagement."
        ],
        "SABRE": [
            "Led migration of a high-throughput shopping engine from 200+ MySQL nodes to a 6-node Oracle RAC cluster — handling 10x the transaction volume of VISA.",
            "Optimized core transaction processing using C++ and OCCI, reducing physical hardware footprint by 95% while maintaining sub-second query latency.",
            "Built CPPUNIT testing framework in C++/OCCI/OCI to validate migration correctness across millions of transaction records.",
            "Automated schema conversion and data validation pipelines to ensure integrity throughout the phased migration cutover."
        ],
        "AT&T": [
            "Analyzed J2EE telecom web applications under load to identify optimal throughput limits and resource bottlenecks (JDBC connections, threads, heap memory, CPU, GC pressure).",
            "Installed and configured JMX Monitoring, Wily Introscope, and Thread Dump automation scripts for real-time visibility during load tests.",
            "Documented performance baselines and regression thresholds used by engineering teams for release gate decisions."
        ],
        "COMPUTER SCIENCE CORPORATION": [
            "Designed UML class/sequence diagrams and developed modules for the IRS CADE mainframe modernization project.",
            "Built CICS/MQ Series/XML messaging interfaces in VC++ with DB2 backend — adhering to government system architecture standards."
        ]
    }

    exps = data.get("experiences", [])
    for exp in exps:
        company = exp.get("company", "").upper()
        # Find matching rules
        for keyword, bullets in updates.items():
            if keyword in company:
                exp["highlights"] = bullets

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    run_cleanup2()
