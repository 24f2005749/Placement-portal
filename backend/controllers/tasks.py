import csv
import os
import smtplib
from datetime import UTC, date, datetime, timedelta
from email.message import EmailMessage

from celery import Celery
from celery.schedules import crontab
from flask import Flask

from controllers.config import Config
from controllers.database import db
from controllers.models import Application, Drive, Student, User


celery = Celery(
    "placement_portal",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

celery.conf.timezone = "Asia/Kolkata"
celery.conf.beat_schedule = {
    "daily-application-deadline-reminders": {
        "task": "controllers.tasks.send_daily_reminders",
        "schedule": crontab(
            hour=Config.DAILY_REMINDER_HOUR,
            minute=Config.DAILY_REMINDER_MINUTE
        )
    },
    "monthly-placement-activity-report": {
        "task": "controllers.tasks.send_monthly_activity_report",
        "schedule": crontab(hour=8, minute=0, day_of_month=1)
    }
}


def flask_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app


def send_email(to_email, subject, html):
    os.makedirs(Config.EXPORT_FOLDER, exist_ok=True)

    if not Config.MAIL_HOST:
        with open(os.path.join(Config.EXPORT_FOLDER, "mail.log"), "a", encoding="utf-8") as log:
            log.write(f"\nTo: {to_email}\nSubject: {subject}\n{html}\n")
        return

    message = EmailMessage()
    message["From"] = Config.MAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content("Please view this email in an HTML-capable client.")
    message.add_alternative(html, subtype="html")

    with smtplib.SMTP(Config.MAIL_HOST, Config.MAIL_PORT) as smtp:
        if Config.MAIL_USE_TLS:
            smtp.starttls()

        if Config.MAIL_USERNAME:
            smtp.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)

        smtp.send_message(message)


def format_date(value):
    return value.isoformat() if value else ""


def student_is_eligible(student, drive):
    if drive.eligibility_cgpa and student.cgpa < drive.eligibility_cgpa:
        return False

    if drive.eligibility_year and student.graduation_year != drive.eligibility_year:
        return False

    if drive.branches and student.branch not in drive.branches:
        return False

    return True


@celery.task(name="controllers.tasks.send_daily_reminders")
def send_daily_reminders():
    app = flask_app()

    with app.app_context():
        today = date.today()
        upcoming = today + timedelta(days=3)
        drives = Drive.query.filter(
            Drive.approval_status == "approved",
            Drive.status == "open",
            Drive.application_deadline >= today,
            Drive.application_deadline <= upcoming
        ).all()

        sent = 0

        for student in Student.query.join(User).filter(User.active == True).all():
            reminders = []

            for drive in drives:
                already_applied = Application.query.filter_by(
                    student_id=student.id,
                    drive_id=drive.id
                ).first()

                if not already_applied and student_is_eligible(student, drive):
                    reminders.append(drive)

            if not reminders:
                continue

            items = "".join(
                f"<li>{drive.company.company_name} - {drive.title} "
                f"(deadline: {format_date(drive.application_deadline)})</li>"
                for drive in reminders
            )
            send_email(
                student.user.email,
                "Upcoming placement application deadlines",
                f"<h2>Placement reminders</h2><p>Apply before the deadline:</p><ul>{items}</ul>"
            )
            sent += 1

        return {"students_notified": sent, "drives_checked": len(drives)}


@celery.task(name="controllers.tasks.send_monthly_activity_report")
def send_monthly_activity_report():
    app = flask_app()

    with app.app_context():
        today = date.today()
        first_this_month = today.replace(day=1)
        last_month_end = first_this_month - timedelta(days=1)
        first_last_month = last_month_end.replace(day=1)

        drives_conducted = Drive.query.filter(
            Drive.drive_date >= first_last_month,
            Drive.drive_date <= last_month_end
        ).count()

        applications = Application.query.filter(
            Application.applied_at >= datetime.combine(first_last_month, datetime.min.time(), tzinfo=UTC),
            Application.applied_at <= datetime.combine(last_month_end, datetime.max.time(), tzinfo=UTC)
        ).all()

        applied_students = len({application.student_id for application in applications})
        selected_students = len({
            application.student_id
            for application in applications
            if application.status == "selected"
        })

        html = f"""
        <h2>Monthly Placement Activity Report</h2>
        <p>Period: {first_last_month.isoformat()} to {last_month_end.isoformat()}</p>
        <table border="1" cellpadding="8" cellspacing="0">
            <tr><th>Metric</th><th>Count</th></tr>
            <tr><td>Drives conducted</td><td>{drives_conducted}</td></tr>
            <tr><td>Students applied</td><td>{applied_students}</td></tr>
            <tr><td>Students selected</td><td>{selected_students}</td></tr>
        </table>
        """

        send_email(Config.ADMIN_EMAIL, "Monthly placement activity report", html)

        return {
            "drives_conducted": drives_conducted,
            "students_applied": applied_students,
            "students_selected": selected_students
        }


@celery.task(name="controllers.tasks.export_student_applications")
def export_student_applications(student_id):
    app = flask_app()

    with app.app_context():
        student = Student.query.get(student_id)

        if not student:
            raise ValueError("Student not found")

        os.makedirs(Config.EXPORT_FOLDER, exist_ok=True)
        filename = f"student_{student.id}_applications_{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}.csv"
        path = os.path.join(Config.EXPORT_FOLDER, filename)

        applications = Application.query.filter_by(student_id=student.id).all()

        with open(path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                "Student ID",
                "Company Name",
                "Drive Title",
                "Application Status",
                "Applied At",
                "Interview Date",
                "Drive Date",
                "Application Deadline"
            ])

            for application in applications:
                writer.writerow([
                    student.id,
                    application.drive.company.company_name,
                    application.drive.title,
                    application.status,
                    format_date(application.applied_at),
                    format_date(application.interview_date),
                    format_date(application.drive.drive_date),
                    format_date(application.drive.application_deadline)
                ])

        send_email(
            student.user.email,
            "Your placement applications CSV is ready",
            f"<p>Your export is ready.</p><p>File: {filename}</p>"
        )

        return {"filename": filename}
