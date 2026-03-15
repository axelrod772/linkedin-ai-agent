"""
Curated sample job postings for India. Used when live LinkedIn scraping returns no results.
Wide range of roles and locations so any resume can get a match.
"""

from __future__ import annotations

from typing import Any, Dict, List

def get_sample_jobs(search_term: str, location: str) -> List[Dict[str, Any]]:
    """
    Return 100+ diverse sample jobs from India. Injects search_term and location
    into a few entries; rest are fixed for variety so any resume gets hits.
    """
    loc = location or "India"
    jobs: List[Dict[str, Any]] = []

    # Template job entries: (title, company, city, description, date)
    templates = [
        # Software / Full-stack / Backend
        (
            "Software Engineer",
            "Flipkart",
            "Bangalore",
            "Build scalable e-commerce systems. Java, microservices, distributed systems. "
            "Experience with Spring Boot, Kafka, Cassandra. Work with product and design.",
            0,
        ),
        (
            "Senior Software Development Engineer",
            "Amazon India",
            "Bangalore",
            "Design and build large-scale distributed systems. Java or C++. Ownership of full lifecycle. "
            "Strong in data structures, algorithms, system design. Mentoring junior engineers.",
            1,
        ),
        (
            "Backend Engineer",
            "Razorpay",
            "Bangalore",
            "Payment infrastructure and APIs. Go or Python. PostgreSQL, Redis. "
            "Fintech experience a plus. Fast-paced startup environment.",
            0,
        ),
        (
            "Full Stack Developer",
            "Zomato",
            "Gurgaon",
            "React, Node.js, Python. Build consumer and restaurant-facing products. "
            "REST APIs, databases, cloud (AWS). Agile, cross-functional teams.",
            2,
        ),
        (
            "Software Engineer – Backend",
            "Swiggy",
            "Bangalore",
            "Scalable backend services for delivery and logistics. Java/Kotlin or Go. "
            "Event-driven systems, SQL/NoSQL. High traffic, low latency.",
            1,
        ),
        (
            "Staff Software Engineer",
            "Microsoft India",
            "Hyderabad",
            "Cloud and enterprise products. C#, .NET, Azure. Design, code review, technical leadership. "
            "Strong problem solving and communication.",
            3,
        ),
        (
            "Software Development Engineer II",
            "Google India",
            "Bangalore",
            "Build products used by billions. C++, Java, or Python. Distributed systems, ML infrastructure. "
            "BS/MS in CS or equivalent experience.",
            2,
        ),
        (
            "Backend Developer",
            "PhonePe",
            "Bangalore",
            "UPI and payments backend. Java, Go. High availability, fault tolerance. "
            "Kafka, databases, caching. Fintech and compliance awareness.",
            0,
        ),
        (
            "Senior Backend Engineer",
            "Freshworks",
            "Chennai",
            "SaaS product backend. Ruby on Rails or Go. PostgreSQL, Redis, Elasticsearch. "
            "REST and event-driven APIs. B2B product experience.",
            1,
        ),
        (
            "Full Stack Engineer",
            "Zoho",
            "Chennai",
            "Web applications for Zoho suite. JavaScript, TypeScript, React, Node or Java. "
            "Full product lifecycle. Remote-friendly.",
            2,
        ),
        (
            "Software Engineer",
            "Intuit India",
            "Bangalore",
            "Tax and accounting products. Java, microservices, AWS. Quality and testing. "
            "Collaboration with US teams. Financial domain helpful.",
            1,
        ),
        (
            "Backend Software Engineer",
            "ShareChat",
            "Bangalore",
            "Social and content platform at scale. Go, Python, Kafka, Cassandra. "
            "Recommendation systems, feed pipeline. Startup speed.",
            0,
        ),
        (
            "Senior Software Engineer",
            "Walmart Global Tech India",
            "Bangalore",
            "Retail and e-commerce platforms. Java, Spring, cloud. Large-scale systems. "
            "Agile, global collaboration.",
            2,
        ),
        (
            "Software Developer",
            "Accenture",
            "Mumbai",
            "Client projects across banking, retail, tech. Java, .NET, or cloud. "
            "Analysis, design, development, testing. Good communication.",
            1,
        ),
        (
            "Engineer – Backend",
            "Cred",
            "Bangalore",
            "Fintech product engineering. Python, Go, or Node. Databases, APIs, security. "
            "Consumer finance, rewards, payments.",
            0,
        ),
        # Frontend / Mobile
        (
            "Frontend Engineer",
            "Dunzo",
            "Bangalore",
            "React, TypeScript, responsive UIs. Build consumer and partner apps. "
            "Performance, accessibility, design systems.",
            1,
        ),
        (
            "React Developer",
            "InfoEdge (Naukri)",
            "Noida",
            "Job portal and recruitment products. React, Redux, modern JavaScript. "
            "SEO, performance, cross-browser.",
            2,
        ),
        (
            "Android Developer",
            "Paytm",
            "Noida",
            "Paytm Android app. Kotlin, Java, Android SDK. Payments, compliance, security. "
            "CI/CD, testing, release process.",
            0,
        ),
        (
            "iOS Developer",
            "Ola",
            "Bangalore",
            "Mobility app for riders and drivers. Swift, iOS frameworks. "
            "Maps, payments, real-time features. Quality and performance.",
            1,
        ),
        (
            "Frontend Developer",
            "Myntra",
            "Bangalore",
            "E-commerce frontend. React, Next.js, CSS. A/B tests, conversion, UX. "
            "Collaboration with design and backend.",
            2,
        ),
        # Data / ML / AI
        (
            "Data Scientist",
            "Jio",
            "Mumbai",
            "Analytics and ML for telecom and digital. Python, SQL, PyTorch/TensorFlow. "
            "Large-scale data, model deployment, business impact.",
            1,
        ),
        (
            "Machine Learning Engineer",
            "Adobe India",
            "Noida",
            "ML for Creative Cloud and Document Cloud. Python, C++, ML frameworks. "
            "Recommendation, search, NLP. Research to production.",
            2,
        ),
        (
            "AI Engineer",
            "TCS",
            "Chennai",
            "AI/ML solutions for enterprise clients. Python, NLP, computer vision. "
            "TensorFlow, PyTorch. Client-facing, problem solving.",
            1,
        ),
        (
            "Senior Data Engineer",
            "LinkedIn India",
            "Bangalore",
            "Data pipelines and analytics. Spark, Kafka, Airflow. SQL, data modeling. "
            "Collaboration with product and data science.",
            2,
        ),
        (
            "ML Engineer",
            "Walmart India",
            "Bangalore",
            "Recommendation and demand forecasting. Python, Spark, ML Ops. "
            "A/B testing, feature engineering, production models.",
            0,
        ),
        (
            "Data Analyst",
            "Deloitte India",
            "Hyderabad",
            "Analytics and reporting for clients. SQL, Excel, Tableau/Power BI. "
            "Requirements, dashboards, insights. Consulting delivery.",
            1,
        ),
        (
            "Business Analyst",
            "Capgemini",
            "Mumbai",
            "Requirements, process design, UAT. Agile, Jira, documentation. "
            "Client interaction, functional and technical bridge.",
            2,
        ),
        (
            "Data Scientist – NLP",
            "Samsung R&D India",
            "Bangalore",
            "NLP for devices and services. Python, transformers, LLMs. "
            "Research and productization. Publications a plus.",
            1,
        ),
        (
            "Computer Vision Engineer",
            "Zepto",
            "Mumbai",
            "CV for quick commerce: inventory, quality. Python, PyTorch, OpenCV. "
            "Real-time systems, edge deployment.",
            0,
        ),
        (
            "Analytics Engineer",
            "Udaan",
            "Bangalore",
            "Data warehouse and analytics. SQL, dbt, BigQuery/Redshift. "
            "Stakeholder reporting, self-serve analytics.",
            2,
        ),
        # DevOps / SRE / Cloud
        (
            "DevOps Engineer",
            "MediaTek India",
            "Bangalore",
            "CI/CD, Kubernetes, Terraform. AWS/GCP. Monitoring, on-call. "
            "Developer experience, reliability.",
            1,
        ),
        (
            "SRE",
            "Netflix India",
            "Bangalore",
            "Reliability and scale for streaming. Linux, cloud, automation. "
            "Incident response, postmortems, capacity planning.",
            2,
        ),
        (
            "Cloud Engineer",
            "HCL Technologies",
            "Noida",
            "Cloud migration and management. AWS/Azure, IaC, security. "
            "Client projects, documentation, best practices.",
            1,
        ),
        (
            "Platform Engineer",
            "Thoughtworks India",
            "Bangalore",
            "Developer platform and tooling. Kubernetes, APIs, observability. "
            "Agile, pair programming, continuous delivery.",
            0,
        ),
        # Product / QA / Support
        (
            "Product Manager",
            "OYO",
            "Gurgaon",
            "Own roadmap for hospitality products. Data-driven, user research. "
            "Engineering and design collaboration. Travel/hospitality interest.",
            1,
        ),
        (
            "Technical Product Manager",
            "Lenskart",
            "Gurgaon",
            "E-commerce and supply chain products. Technical background, APIs, analytics. "
            "Prioritization, specs, stakeholder management.",
            2,
        ),
        (
            "QA Engineer",
            "Tech Mahindra",
            "Pune",
            "Test design, automation, regression. Selenium, API testing, JIRA. "
            "Agile, release quality, defect tracking.",
            1,
        ),
        (
            "SDET",
            "Morgan Stanley",
            "Mumbai",
            "Test automation for financial platforms. Java, test frameworks, CI. "
            "Capital markets domain. Rigorous processes.",
            2,
        ),
        (
            "Support Engineer",
            "Zendesk India",
            "Bangalore",
            "Customer support and troubleshooting. SQL, APIs, logs. "
            "Documentation, escalation, customer communication.",
            0,
        ),
        # Design / UX
        (
            "UX Designer",
            "MakeMyTrip",
            "Gurgaon",
            "Travel booking experiences. Research, wireframes, prototypes. "
            "Figma, design systems, collaboration with product and engineering.",
            1,
        ),
        (
            "Product Designer",
            "Unacademy",
            "Bangalore",
            "EdTech product design. User research, flows, visual design. "
            "Mobile and web. Education sector interest.",
            2,
        ),
        (
            "UI Developer",
            "Mindtree",
            "Bangalore",
            "Front-end implementation from designs. HTML, CSS, JavaScript, React. "
            "Accessibility, performance, responsive design.",
            1,
        ),
        # Sales / Marketing / Operations
        (
            "Sales Engineer",
            "Salesforce India",
            "Hyderabad",
            "Pre-sales, demos, POCs. CRM, integrations, cloud. "
            "Technical sales, customer workshops.",
            0,
        ),
        (
            "Digital Marketing Manager",
            "Nykaa",
            "Mumbai",
            "Performance marketing, SEO, analytics. Campaigns, budgets, ROI. "
            "Beauty/lifestyle e-commerce. Team coordination.",
            1,
        ),
        (
            "Operations Manager",
            "Blinkit",
            "Gurgaon",
            "Quick commerce operations. Process, metrics, vendor coordination. "
            "Logistics, inventory, last-mile. On-ground and central teams.",
            2,
        ),
        # Finance / Consulting / Other
        (
            "Financial Analyst",
            "Goldman Sachs India",
            "Bangalore",
            "Financial modeling, reporting, risk. Excel, VBA, SQL. "
            "Attention to detail, compliance, team collaboration.",
            1,
        ),
        (
            "Consultant",
            "McKinsey India",
            "Mumbai",
            "Strategy and operations for top firms. Analysis, presentations, client work. "
            "Strong academics, problem solving, communication.",
            2,
        ),
        (
            "Java Developer",
            "Infosys",
            "Bangalore",
            "Enterprise applications for global clients. Java, Spring, databases. "
            "SDLC, testing, documentation. Willing to learn new technologies.",
            1,
        ),
        (
            "Python Developer",
            "Cognizant",
            "Chennai",
            "Python applications and scripting. Django/Flask, SQL, Linux. "
            "Client projects, agile, code quality.",
            0,
        ),
        (
            ".NET Developer",
            "L&T Infotech",
            "Mumbai",
            "Enterprise .NET applications. C#, ASP.NET, SQL Server. "
            "Design patterns, performance, security.",
            2,
        ),
        (
            "Node.js Developer",
            "Gojek India",
            "Bangalore",
            "Backend services for ride-hailing and payments. Node.js, TypeScript, PostgreSQL. "
            "Microservices, event-driven. Startup culture.",
            1,
        ),
        (
            "Golang Developer",
            "Postman",
            "Bangalore",
            "API platform backend. Go, distributed systems, APIs. "
            "Developer tools, scale, open source.",
            0,
        ),
        (
            "Ruby on Rails Developer",
            "Chargebee",
            "Chennai",
            "Subscription billing platform. Ruby, Rails, PostgreSQL. "
            "B2B SaaS, payments, integrations.",
            2,
        ),
        (
            "Site Reliability Engineer",
            "Atlassian India",
            "Bangalore",
            "Jira, Confluence reliability. Kubernetes, AWS, observability. "
            "On-call, automation, incident management.",
            1,
        ),
        (
            "Security Engineer",
            "Quick Heal",
            "Pune",
            "Product and infrastructure security. Threat modeling, pentesting. "
            "Secure SDLC, compliance, awareness.",
            0,
        ),
        (
            "Embedded Software Engineer",
            "Bosch India",
            "Bangalore",
            "Embedded C/C++ for automotive/industrial. RTOS, communication protocols. "
            "Hardware-software interface, testing.",
            2,
        ),
        (
            "Mobile Engineer – React Native",
            "Meesho",
            "Bangalore",
            "Cross-platform app for social commerce. React Native, JavaScript. "
            "Performance, native modules, releases.",
            1,
        ),
        (
            "Data Engineer",
            "Groww",
            "Bangalore",
            "Data pipelines for fintech. Python, Spark, Airflow, Redshift. "
            "Analytics, ML data, data quality.",
            0,
        ),
        (
            "BI Developer",
            "ICICI Bank",
            "Mumbai",
            "Reports and dashboards for banking. SQL, SSRS, Power BI. "
            "Data modeling, stakeholder requirements.",
            2,
        ),
        (
            "Automation Engineer",
            "Wipro",
            "Hyderabad",
            "Test and process automation. Selenium, Python, Jenkins. "
            "Regression, CI/CD, scripting.",
            1,
        ),
        (
            "Solution Architect",
            "Dell Technologies India",
            "Bangalore",
            "Solution design for enterprise. Cloud, storage, security. "
            "Presales, RFPs, technical leadership.",
            2,
        ),
        (
            "Technical Lead",
            "Persistent Systems",
            "Pune",
            "Lead delivery for software projects. Design, code review, mentoring. "
            "Java/Python, agile, client communication.",
            1,
        ),
        (
            "Graduate Trainee – Software",
            "L&T Technology Services",
            "Bangalore",
            "Trainee role in embedded/software. C, C++, basics of embedded. "
            "Learning, assignments, growth into full role.",
            0,
        ),
        (
            "Intern – Data Science",
            "JPMorgan Chase India",
            "Mumbai",
            "Data science intern. Python, ML, analytics. "
            "Mentorship, real projects, potential conversion.",
            0,
        ),
        (
            "Associate Consultant",
            "EY India",
            "Bangalore",
            "Consulting delivery. Analysis, slides, client support. "
            "Strong Excel, communication, teamwork.",
            1,
        ),
        (
            "Content Writer",
            "Byju's",
            "Bangalore",
            "EdTech content. Research, writing, SEO. "
            "Education sector, clarity, deadlines.",
            2,
        ),
        (
            "HR Recruiter",
            "Tata Consultancy Services",
            "Chennai",
            "Tech and non-tech hiring. Sourcing, screening, coordination. "
            "ATS, stakeholder management, metrics.",
            1,
        ),
        (
            "Customer Success Manager",
            "Zoho",
            "Chennai",
            "Customer onboarding and success. Product knowledge, communication. "
            "Retention, upsell, feedback loop.",
            0,
        ),
        (
            "Project Manager",
            "IBM India",
            "Gurgaon",
            "IT project delivery. Planning, risk, stakeholders. "
            "Agile/waterfall, reporting, team coordination.",
            2,
        ),
        (
            "Business Development Executive",
            "UpGrad",
            "Mumbai",
            "B2B/B2C for online education. Outreach, demos, closures. "
            "Targets, CRM, collaboration with marketing.",
            1,
        ),
        (
            "DevOps Lead",
            "SAP Labs India",
            "Bangalore",
            "CI/CD and platform for SAP products. Kubernetes, cloud, security. "
            "Team lead, standards, vendor tools.",
            2,
        ),
        (
            "Frontend Lead",
            "CleverTap",
            "Mumbai",
            "Lead frontend for analytics platform. React, architecture, team. "
            "Performance, design systems, hiring.",
            1,
        ),
        (
            "Senior Data Scientist",
            "InMobi",
            "Bangalore",
            "Ad tech ML. Python, Spark, recommendation systems. "
            "A/B tests, production models, scale.",
            0,
        ),
        (
            "iOS Lead",
            "Practo",
            "Bangalore",
            "Lead iOS for healthcare app. Swift, architecture, releases. "
            "Mentoring, app store, compliance.",
            2,
        ),
        (
            "Backend Lead",
            "Livspace",
            "Bangalore",
            "Backend for home interior platform. Java/Python, APIs, scale. "
            "Team lead, design, delivery.",
            1,
        ),
        (
            "Cloud Architect",
            "VMware India",
            "Bangalore",
            "Cloud and virtualization solutions. Design, migration, best practices. "
            "Customer workshops, RFPs.",
            2,
        ),
        (
            "ML Ops Engineer",
            "Fractal Analytics",
            "Mumbai",
            "ML model deployment and monitoring. Python, Docker, Kubernetes. "
            "ML pipelines, reproducibility, governance.",
            1,
        ),
        (
            "API Developer",
            "PayU",
            "Gurgaon",
            "Payment APIs and integrations. REST, security, documentation. "
            "Fintech, partner onboarding.",
            0,
        ),
        (
            "Game Developer",
            "Nazara Technologies",
            "Mumbai",
            "Mobile game development. Unity, C#. Gameplay, performance. "
            "Gaming passion, portfolio.",
            2,
        ),
        (
            "Blockchain Developer",
            "Polygon",
            "Bangalore",
            "Ethereum L2 and tooling. Solidity, TypeScript, Web3. "
            "Smart contracts, testing, documentation.",
            1,
        ),
        (
            "AR/VR Developer",
            "TCS Innovation Labs",
            "Bangalore",
            "AR/VR applications. Unity, C#, 3D. Research and productization. "
            "Prototyping, client demos.",
            0,
        ),
        (
            "Technical Writer",
            "Red Hat India",
            "Bangalore",
            "Documentation for open source products. Technical accuracy, clarity. "
            "Markdown, docs-as-code, community.",
            2,
        ),
        (
            "Scrum Master",
            "Vodafone Idea",
            "Pune",
            "Agile facilitation for IT squads. Ceremonies, metrics, impediments. "
            "Jira, stakeholder alignment.",
            1,
        ),
        (
            "Database Administrator",
            "Oracle India",
            "Hyderabad",
            "Oracle DB administration. Performance, backup, security. "
            "Scripting, monitoring, on-call.",
            0,
        ),
        (
            "Network Engineer",
            "Airtel",
            "Gurgaon",
            "Network design and operations. Routing, security, monitoring. "
            "Troubleshooting, vendor coordination.",
            2,
        ),
        (
            "Cybersecurity Analyst",
            "Wipro",
            "Bangalore",
            "SOC, threat detection, incident response. SIEM, forensics. "
            "Shift work, reporting, compliance.",
            1,
        ),
        (
            "Fresher – Software Engineer",
            "Cognizant",
            "Chennai",
            "Graduate hire. Training in Java/.NET/cloud. "
            "Assignments, certification, project allocation.",
            0,
        ),
        (
            "Trainee – Data Analyst",
            "KPMG India",
            "Mumbai",
            "Trainee in data and analytics. Excel, SQL, visualization. "
            "Learning, client support, growth.",
            0,
        ),
    ]

    date_strs = ["Today", "Yesterday", "2 days ago", "3 days ago", "1 week ago"]
    base = "https://www.linkedin.com/jobs/view/"

    for i, (title, company, city, desc, date_idx) in enumerate(templates):
        job_id = 290000000 + i
        jobs.append({
            "title": title,
            "company": company,
            "location": city,
            "description": desc,
            "link": f"{base}{job_id}",
            "date": date_strs[min(date_idx, len(date_strs) - 1)],
        })

    # Add more to reach 100+: duplicate with location/role variations
    extra = [
        ("Software Engineer", "EPAM India", "Hyderabad", "Full-stack or backend. Java, .NET, or Node. Client projects, agile.", 1),
        ("QA Automation Engineer", "Mindtree", "Bangalore", "Selenium, Java/Python, CI. Test design, regression, API testing.", 2),
        ("React Native Developer", "Innovaccer", "Noida", "Healthcare app. React Native, JavaScript. Cross-platform, performance.", 0),
        ("DevOps Engineer", "Nagarro", "Gurgaon", "CI/CD, Docker, K8s. AWS/Azure. Scripting, automation.", 1),
        ("Data Analyst", "Publicis Sapient", "Mumbai", "Analytics, SQL, Tableau. Client delivery, insights.", 2),
        ("Backend Engineer", "NoBroker", "Bangalore", "Real estate platform. Node/Java, databases, APIs.", 0),
        ("Frontend Developer", "BrowserStack", "Mumbai", "Product frontend. React, testing tools. Remote option.", 1),
        ("ML Engineer", "Cure.fit", "Bangalore", "Health and fitness ML. Python, recommendation, personalization.", 2),
        ("Product Manager", "Policybazaar", "Gurgaon", "Insurance products. Roadmap, data, cross-functional.", 0),
        ("Full Stack Developer", "Licious", "Bangalore", "E-commerce full stack. Node, React, cloud.", 1),
        ("Java Developer", "Virtusa", "Chennai", "Java, Spring Boot. Enterprise projects, client delivery.", 2),
        ("Python Developer", "Quantiphi", "Mumbai", "Data and ML pipelines. Python, GCP/AWS. Analytics projects.", 0),
        ("UX Researcher", "PhonePe", "Bangalore", "User research for payments. Methods, synthesis, stakeholder shareouts.", 1),
        ("SRE", "Directi", "Mumbai", "Reliability for web products. Linux, scripting, monitoring.", 2),
        ("Backend Developer", "Dealshare", "Bangalore", "E-commerce backend. Scale, performance. Startup.", 0),
        ("Data Engineer", "Rebel Foods", "Mumbai", "Data pipelines for cloud kitchens. SQL, Python, BI.", 1),
        ("Android Developer", "Meesho", "Bangalore", "Android for social commerce. Kotlin, Jetpack, performance.", 2),
        ("iOS Developer", "ShareChat", "Bangalore", "iOS app. Swift, UIKit/SwiftUI. Content, feed, performance.", 0),
        ("Technical Program Manager", "Microsoft India", "Hyderabad", "Cross-team programs. Planning, risk, delivery.", 1),
        ("Security Analyst", "TCS", "Mumbai", "Security operations, vulnerability management. SIEM, compliance.", 2),
        ("Data Scientist", "Ather Energy", "Bangalore", "EV and mobility analytics. Python, ML, forecasting.", 0),
        ("Software Engineer", "Hike", "Gurgaon", "Messaging and social. Backend or mobile. Scale, real-time.", 1),
        ("Backend Engineer", "Instamojo", "Bangalore", "Payments for SMBs. Python, Django, PostgreSQL.", 2),
        ("Frontend Engineer", "CleverTap", "Mumbai", "Marketing automation UI. React, dashboards, real-time.", 0),
        ("Data Analyst", "Swiggy", "Bangalore", "Supply and demand analytics. SQL, Python, experimentation.", 1),
        ("DevOps Engineer", "Reverie Labs", "Bangalore", "Biotech software infra. AWS, containers, automation.", 2),
        ("Full Stack Engineer", "Slice", "Bangalore", "Fintech for young users. Node, React, scale.", 0),
        ("ML Engineer", "InVideo", "Mumbai", "Video creation AI. Python, NLP, computer vision.", 1),
        ("Product Designer", "Razorpay", "Bangalore", "Fintech UX. Research, flows, design system.", 2),
        ("Java Developer", "SAP Labs", "Bangalore", "SAP product development. Java, enterprise patterns.", 0),
        ("Python Developer", "Icertis", "Pune", "Contract lifecycle. Python, Django, cloud.", 1),
        ("React Developer", "Delhivery", "Gurgaon", "Logistics dashboards. React, maps, real-time.", 2),
        ("QA Engineer", "BigBasket", "Bangalore", "E-commerce QA. Manual and automation, release.", 0),
        ("Technical Lead", "CitiusTech", "Mumbai", "Healthcare IT. Java/.NET, team lead, client.", 1),
        ("Data Engineer", "Dream11", "Mumbai", "Sports fantasy data. Pipelines, analytics, real-time.", 2),
    ]
    for i, (title, company, city, desc, date_idx) in enumerate(extra):
        job_id = 291000000 + i
        jobs.append({
            "title": title,
            "company": company,
            "location": city,
            "description": desc,
            "link": f"{base}{job_id}",
            "date": date_strs[min(date_idx, len(date_strs) - 1)],
        })

    # Ensure user's location appears in some jobs for relevance
    for j in jobs[: min(20, len(jobs))]:
        j["location"] = loc

    return jobs
