import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PDF = OUT_DIR / "DriveSure-Technologies-Used.pdf"


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


backend_pkg = load_json(ROOT / "backend" / "package.json")
frontend_pkg = load_json(ROOT / "frontend" / "package.json")

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="Times-Bold",
        fontSize=28,
        leading=34,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F294D"),
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSub",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=13,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=18,
    )
)
styles.add(
    ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading1"],
        fontName="Times-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#2563A0"),
        spaceBefore=12,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="SubTitle",
        parent=styles["Heading2"],
        fontName="Times-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0F294D"),
        spaceBefore=8,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Body12",
        parent=styles["BodyText"],
        fontName="Times-Roman",
        fontSize=12,
        leading=17,
        alignment=TA_LEFT,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontName="Times-Roman",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=4,
    )
)


def p(text, style="Body12"):
    return Paragraph(text, styles[style])


def bullet(text):
    return p(f"&bull; {text}", "Body12")


def tech_table(rows, widths=(1.65 * inch, 2.15 * inch, 2.15 * inch)):
    data = [[p("<b>Technology</b>"), p("<b>Used For</b>"), p("<b>Project Relevance</b>")]]
    for row in rows:
        data.append([p(str(row[0])), p(str(row[1])), p(str(row[2]))])
    table = Table(data, colWidths=list(widths), repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF1F8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F294D")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9CA3AF")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def dependency_rows(pkg):
    rows = []
    for name, version in sorted(pkg.get("dependencies", {}).items()):
        rows.append([name, version])
    for name, version in sorted(pkg.get("devDependencies", {}).items()):
        rows.append([f"{name} (dev)", version])
    data = [[p("<b>Package</b>"), p("<b>Version</b>")]]
    for name, version in rows:
        data.append([p(name), p(version)])
    table = Table(data, colWidths=[3.8 * inch, 2.0 * inch], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF1F8")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9CA3AF")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 9)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(doc.leftMargin, A4[1] - 0.45 * inch, "DriveSure - Technologies Used")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


story = []
story.append(Spacer(1, 0.55 * inch))
story.append(p("DriveSure", "CoverTitle"))
story.append(p("Technologies Used in the Car Insurance Company Project", "CoverSub"))
story.append(
    p(
        "This PDF summarizes the frontend, backend, database, reporting, security, deployment, and development technologies used in the DriveSure project.",
        "CoverSub",
    )
)
story.append(Spacer(1, 0.25 * inch))
story.append(
    tech_table(
        [
            ["Project Name", "DriveSure", "Full-stack car insurance company management system."],
            ["Domain", "Car Insurance", "Customer, vehicle, policy, claim, payment, report, and security workflows."],
            ["Architecture", "MERN Stack", "React frontend, Express backend, MongoDB database, and Node.js runtime."],
            ["Repository Evidence", "package.json, README, routes, models, utilities", "Technology list is based on files present in the project workspace."],
        ]
    )
)
story.append(PageBreak())

story.append(p("1. Technology Stack Overview", "SectionTitle"))
story.append(
    p(
        "DriveSure uses a MERN-style architecture with React on the client side, Node.js and Express.js on the server side, and MongoDB Atlas as the database. The application also includes utilities for authentication, upload handling, reporting, email notifications, security auditing, pagination, PDF generation, invoice generation, and CSV export.",
    )
)
story.append(
    tech_table(
        [
            ["React 18", "Frontend user interface", "Builds dashboard screens, forms, protected routes, customer portal, and module pages."],
            ["Vite", "Frontend build tool", "Provides fast development server and optimized frontend build output."],
            ["Tailwind CSS", "Styling framework", "Supports responsive dashboard UI, layout utilities, spacing, colors, and component styling."],
            ["Node.js", "Backend runtime", "Runs the server-side JavaScript application."],
            ["Express.js", "Backend API framework", "Defines REST routes for auth, customers, vehicles, policies, claims, payments, reports, security, and notifications."],
            ["MongoDB Atlas", "Cloud database", "Stores insurance records using flexible document collections."],
            ["Mongoose", "ODM layer", "Defines schemas, validation rules, ObjectId relationships, and model operations."],
        ]
    )
)

story.append(p("2. Frontend Technologies", "SectionTitle"))
story.append(
    p(
        "The frontend is located in the frontend folder and uses React with Vite. The route structure in src/App.jsx connects public pages such as login, register, reset password, email verification, customer login, and customer portal with protected application modules such as dashboard, customers, vehicles, policies, claims, payments, reports, security center, notifications, backups, and profile."
    )
)
story.append(
    tech_table(
        [
            ["React", "Component-based UI", "Used for pages, shared components, dashboard cards, upload controls, timeline views, forms, and protected route handling."],
            ["React DOM", "Browser rendering", "Mounts the React application into the web page."],
            ["React Router DOM", "Client-side routing", "Supports login, portfolio, customer portal, and protected dashboard navigation."],
            ["Axios", "HTTP client", "Connects frontend pages to backend REST APIs."],
            ["Lucide React", "Icon library", "Provides clean dashboard and action icons."],
            ["Tailwind CSS", "Utility-first styling", "Creates responsive layouts and modern interface styling."],
            ["Vercel Analytics", "Frontend analytics", "Supports usage and performance visibility when deployed."],
            ["Vercel Speed Insights", "Performance monitoring", "Helps monitor frontend speed and user experience."],
        ]
    )
)
story.append(p("Frontend package evidence", "SubTitle"))
story.append(dependency_rows(frontend_pkg))
story.append(PageBreak())

story.append(p("3. Backend Technologies", "SectionTitle"))
story.append(
    p(
        "The backend is located in the backend folder and is organized into config, controllers, middleware, models, routes, services, utilities, uploads, reports, seed.js, and server.js. The API layer uses Express routes and controller functions to manage insurance operations."
    )
)
story.append(
    tech_table(
        [
            ["Node.js", "Server runtime", "Executes the backend API server and utility scripts."],
            ["Express.js", "REST API framework", "Creates API endpoints for authentication, dashboard, customer, vehicle, policy, claim, payment, report, and security modules."],
            ["express-async-handler", "Async route handling", "Simplifies error handling in asynchronous controller functions."],
            ["CORS", "Cross-origin access", "Allows configured frontend origins to communicate with the backend API."],
            ["Morgan", "HTTP logging", "Logs backend requests for development and debugging."],
            ["dotenv", "Environment config", "Loads secrets, URLs, SMTP settings, database connection string, and security keys."],
            ["Nodemon", "Development restart tool", "Restarts the server automatically during local backend development."],
        ]
    )
)
story.append(p("Backend package evidence", "SubTitle"))
story.append(dependency_rows(backend_pkg))
story.append(PageBreak())

story.append(p("4. Database and Data Modeling", "SectionTitle"))
story.append(
    p(
        "MongoDB Atlas is used as the target database service. Mongoose models represent business collections such as User, Customer, Vehicle, Policy, Claim, Payment, PaymentPlan, Notification, LoginHistory, SecurityAlert, ActivityLog, SupportTicket, BackupSnapshot, Garage, Feedback, and MessageThread."
    )
)
story.append(
    tech_table(
        [
            ["MongoDB Atlas", "Cloud database hosting", "Stores application records with cloud accessibility and deployment compatibility."],
            ["Mongoose", "Schema and relationship modeling", "Defines ObjectId references, validation, enums, defaults, timestamps, and model methods."],
            ["Seed script", "Development data setup", "Creates sample data for testing and demonstration."],
            ["Relational SQL reference", "database/insurance.sql", "Provides an additional relational schema reference for academic documentation."],
        ]
    )
)
story.append(p("5. Authentication and Cyber Security Technologies", "SectionTitle"))
story.append(
    tech_table(
        [
            ["JWT", "Token-based authentication", "Protects API sessions and allows authenticated frontend requests."],
            ["bcryptjs", "Password hashing", "Hashes user passwords before storage and verifies login credentials securely."],
            ["Role-based access control", "Authorization design", "Restricts actions by roles such as admin, manager, agent, surveyor, and customer."],
            ["fieldCrypto utility", "Sensitive field encryption", "Supports encryption for sensitive data such as contact fields."],
            ["LoginHistory model", "Login monitoring", "Records login attempts and supports suspicious activity review."],
            ["SecurityAlert model", "Security dashboard", "Stores and displays security-related alerts."],
            ["riskScoring utility", "Fraud analysis", "Assists claim risk scoring using fraud indicators."],
        ]
    )
)
story.append(PageBreak())

story.append(p("6. Reporting, Files, and Communication", "SectionTitle"))
story.append(
    tech_table(
        [
            ["PDFKit", "Server-side PDF generation", "Creates policy certificates, invoices, and operational PDF outputs."],
            ["jsPDF", "PDF creation utilities", "Supports browser/server report generation scenarios."],
            ["jsPDF AutoTable", "PDF tables", "Formats tabular report data inside PDFs."],
            ["CSV exporter utility", "CSV download", "Exports structured customer, policy, claim, payment, and report data."],
            ["Multer", "File upload handling", "Accepts claim evidence and document uploads."],
            ["Nodemailer", "Email notifications", "Supports verification emails, password resets, and alert communication."],
            ["Brevo API variables", "Deployment email fallback", "README documents Brevo variables for production transactional email."],
        ]
    )
)
story.append(p("7. Deployment and DevOps Technologies", "SectionTitle"))
story.append(
    tech_table(
        [
            ["Render", "Backend deployment", "render.yaml and README deployment variables support hosting the Express API."],
            ["Vercel", "Frontend deployment", "frontend/vercel.json supports frontend deployment configuration."],
            ["Netlify", "Alternative frontend deployment", "frontend/netlify.toml and public redirects support static hosting."],
            ["Postman", "API testing", "postman_collection.json documents and tests API workflows."],
            ["ESLint", "Code quality", "Checks frontend JavaScript and React code quality."],
            ["Git", "Version control", "Tracks source files and documentation changes in the repository."],
        ]
    )
)
story.append(PageBreak())

story.append(p("8. Module-to-Technology Mapping", "SectionTitle"))
story.append(
    tech_table(
        [
            ["Authentication", "React forms, Express routes, JWT, bcryptjs, Nodemailer", "Registration, login, reset password, verification, and secure sessions."],
            ["Customer Management", "React pages, Axios, Express controllers, Customer model", "Create, update, view, search, and manage customer details."],
            ["Vehicle Management", "Vehicle page, vehicle routes, Vehicle model", "Vehicle registration and customer-vehicle association."],
            ["Policy Management", "Policy page, PDFKit, Mongoose Policy model", "Policy creation, renewal, status tracking, and certificates."],
            ["Claims Management", "Multer, Claim model, riskScoring, upload middleware", "Claim submission, evidence upload, review, inspection, fraud scoring, and settlement."],
            ["Payment Management", "Payment model, invoiceGenerator, report utilities", "Premium collection, payment tracking, invoice generation, and payment reports."],
            ["Security Center", "LoginHistory, SecurityAlert, ActivityLog, security middleware", "Failed login review, audit logs, suspicious activity, and alerts."],
            ["Reports Dashboard", "PDFKit, jsPDF, AutoTable, CSV exporter", "Downloadable reports for business and academic review."],
        ],
        widths=(1.55 * inch, 2.35 * inch, 2.05 * inch),
    )
)
story.append(p("Conclusion", "SectionTitle"))
story.append(
    p(
        "The DriveSure project uses a practical and modern technology stack suitable for a B.Tech full-stack and cyber security project. The stack combines React-based user interfaces, Express REST APIs, MongoDB data modeling, secure authentication, upload handling, reporting tools, and deployment-ready configuration. Together, these technologies support a complete car insurance company management system."
    )
)

doc = SimpleDocTemplate(
    str(OUT_PDF),
    pagesize=A4,
    rightMargin=0.65 * inch,
    leftMargin=0.65 * inch,
    topMargin=0.75 * inch,
    bottomMargin=0.7 * inch,
    title="DriveSure Technologies Used",
    author="DriveSure Project Team",
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUT_PDF)
