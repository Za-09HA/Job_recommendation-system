from django.core.management.base import BaseCommand
from jobs.models import JobListing

SAMPLE_JOBS = [
    {
        "title": "Python Django Developer",
        "company": "Systems Limited",
        "description": "Systems Limited is Pakistan's largest IT company seeking a Python Django Developer to join our growing team in Lahore.\n\nResponsibilities:\n- Develop and maintain Django-based web applications\n- Build RESTful APIs consumed by frontend and mobile teams\n- Write clean, well-documented code\n- Collaborate with cross-functional teams\n\nWe offer competitive salary, health insurance, and a great work culture!",
        "required_skills": "Python, Django, REST API, PostgreSQL, Git, HTML, CSS, JavaScript",
        "location": "Lahore, Pakistan",
        "job_type": "full_time",
        "category": "backend",
        "experience_required": "1_2",
        "salary_min": 80000, "salary_max": 150000,
    },
    {
        "title": "React.js Frontend Developer",
        "company": "Netsol Technologies",
        "description": "Netsol Technologies is a global IT company headquartered in Lahore. We're looking for a skilled React developer to build modern web interfaces.\n\nYou will:\n- Build responsive React applications\n- Integrate with backend REST APIs\n- Optimize performance and accessibility\n- Work in an agile environment",
        "required_skills": "React, JavaScript, TypeScript, HTML, CSS, Git, REST API",
        "location": "Lahore, Pakistan",
        "job_type": "full_time",
        "category": "frontend",
        "experience_required": "1_2",
        "salary_min": 80000, "salary_max": 140000,
    },
    {
        "title": "Full Stack Developer (MERN)",
        "company": "Arbisoft",
        "description": "Arbisoft is one of Pakistan's top software companies, partner of Airbnb and edX. Join our Lahore team as a Full Stack MERN developer.\n\nStack:\n- Backend: Node.js, Express\n- Frontend: React.js\n- Database: MongoDB, PostgreSQL\n- DevOps: Docker, AWS",
        "required_skills": "React, Node.js, MongoDB, Express, JavaScript, Docker, AWS, Git",
        "location": "Lahore, Pakistan",
        "job_type": "full_time",
        "category": "fullstack",
        "experience_required": "3_5",
        "salary_min": 150000, "salary_max": 250000,
    },
    {
        "title": "Data Scientist",
        "company": "10Pearls",
        "description": "10Pearls is a leading digital transformation company. We need a Data Scientist to build ML models and analytics solutions for global clients.\n\nResponsibilities:\n- Build and deploy machine learning models\n- Analyze large datasets\n- Create data visualizations\n- Work with clients on AI solutions",
        "required_skills": "Python, Machine Learning, scikit-learn, TensorFlow, pandas, numpy, SQL, Tableau",
        "location": "Karachi, Pakistan",
        "job_type": "full_time",
        "category": "data",
        "experience_required": "3_5",
        "salary_min": 180000, "salary_max": 300000,
    },
    {
        "title": "Mobile App Developer (Flutter)",
        "company": "Folio3 Software",
        "description": "Folio3 is a global technology company with offices in Karachi. Join our mobile team to build Flutter applications for international clients.\n\nRequirements:\n- Strong Flutter and Dart skills\n- Firebase integration experience\n- REST API integration\n- iOS and Android publishing experience",
        "required_skills": "Flutter, Dart, Firebase, REST API, iOS, Android, Git",
        "location": "Karachi, Pakistan",
        "job_type": "full_time",
        "category": "mobile",
        "experience_required": "1_2",
        "salary_min": 100000, "salary_max": 180000,
    },
    {
        "title": "DevOps Engineer",
        "company": "TRG Pakistan",
        "description": "TRG is one of Pakistan's largest tech conglomerates. We need a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines.\n\nKey Responsibilities:\n- Manage AWS cloud infrastructure\n- Build CI/CD pipelines using Jenkins/GitHub Actions\n- Container orchestration with Kubernetes\n- Monitor and improve system performance",
        "required_skills": "AWS, Docker, Kubernetes, CI/CD, Linux, Terraform, Python, Git",
        "location": "Karachi, Pakistan",
        "job_type": "full_time",
        "category": "devops",
        "experience_required": "3_5",
        "salary_min": 200000, "salary_max": 350000,
    },
    {
        "title": "Junior Python Developer (Fresh Graduate)",
        "company": "Contour Software",
        "description": "Contour Software is a Karachi-based subsidiary of Constellation Software Inc. We welcome fresh graduates to join our growing team.\n\nYou will learn:\n- Python and Django development\n- REST API design\n- Database design and optimization\n- Agile methodologies\n\nGreat opportunity for fresh graduates!",
        "required_skills": "Python, Django, SQL, Git, HTML, CSS",
        "location": "Karachi, Pakistan",
        "job_type": "full_time",
        "category": "backend",
        "experience_required": "fresher",
        "salary_min": 60000, "salary_max": 90000,
    },
    {
        "title": "UI/UX Designer",
        "company": "Zones IT Solutions",
        "description": "Zones is a global IT company with a major office in Islamabad. Looking for a UI/UX designer to create beautiful user experiences.\n\nYou will:\n- Design UI/UX for web and mobile apps using Figma\n- Conduct user research and usability testing\n- Create wireframes, prototypes, and design systems\n- Collaborate with frontend developers",
        "required_skills": "Figma, Adobe XD, UI Design, UX Research, Prototyping, CSS, HTML",
        "location": "Islamabad, Pakistan",
        "job_type": "full_time",
        "category": "design",
        "experience_required": "1_2",
        "salary_min": 80000, "salary_max": 140000,
    },
    {
        "title": "Cybersecurity Analyst",
        "company": "NetSol Technologies",
        "description": "Join our security team to protect our infrastructure and client systems from cyber threats.\n\nResponsibilities:\n- Monitor security events and respond to incidents\n- Conduct vulnerability assessments\n- Implement security controls and policies\n- Security awareness training",
        "required_skills": "Cybersecurity, Linux, Networking, SIEM, Penetration Testing, Python, Firewall",
        "location": "Lahore, Pakistan",
        "job_type": "full_time",
        "category": "cybersecurity",
        "experience_required": "1_2",
        "salary_min": 100000, "salary_max": 180000,
    },
    {
        "title": "Machine Learning Engineer",
        "company": "Afiniti",
        "description": "Afiniti is a world leader in AI-based enterprise technology, headquartered in Islamabad. Join our AI team to build cutting-edge ML solutions.\n\nYou will:\n- Design and train deep learning models\n- Deploy models to production\n- Work with large-scale data pipelines\n- Research and implement new ML techniques",
        "required_skills": "Python, TensorFlow, PyTorch, Machine Learning, Deep Learning, SQL, Docker, AWS",
        "location": "Islamabad, Pakistan",
        "job_type": "full_time",
        "category": "data",
        "experience_required": "3_5",
        "salary_min": 250000, "salary_max": 450000,
    },
    {
        "title": "Backend Developer (Node.js) - Internship",
        "company": "Tkxel",
        "description": "Tkxel is an award-winning software company in Lahore. This internship is perfect for computer science students looking for real-world experience.\n\nYou will learn:\n- Node.js and Express.js development\n- REST API design\n- MongoDB database\n- Agile development practices\n\nPaid internship with potential for full-time offer!",
        "required_skills": "Node.js, JavaScript, MongoDB, REST API, Git, HTML, CSS",
        "location": "Lahore, Pakistan",
        "job_type": "internship",
        "category": "backend",
        "experience_required": "fresher",
        "salary_min": 25000, "salary_max": 40000,
    },
    {
        "title": "Software Engineer (.NET)",
        "company": "Inbox Business Technologies",
        "description": "Inbox Business Technologies is one of Pakistan's leading IT companies based in Islamabad. We need .NET developers to build enterprise solutions.\n\nRequirements:\n- Strong C# and .NET Core skills\n- SQL Server experience\n- Azure cloud knowledge\n- Enterprise application development",
        "required_skills": "C#, .NET Core, SQL Server, Azure, Git, REST API, HTML, CSS",
        "location": "Islamabad, Pakistan",
        "job_type": "full_time",
        "category": "backend",
        "experience_required": "1_2",
        "salary_min": 90000, "salary_max": 160000,
    },
]

class Command(BaseCommand):
    help = 'Seeds the database with Pakistani company job listings'

    def handle(self, *args, **kwargs):
        count = 0
        for job_data in SAMPLE_JOBS:
            obj, created = JobListing.objects.get_or_create(
                title=job_data['title'],
                company=job_data['company'],
                defaults=job_data
            )
            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {obj.title} @ {obj.company}'))
            else:
                self.stdout.write(f'  · Already exists: {obj.title}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Done! Created {count} new Pakistani company job listings.'))
