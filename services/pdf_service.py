from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import datetime


def generate_project_report(project, tasks=None, releases=None):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height - 40, f'Project Report: {project.name}')
    c.setFont('Helvetica', 10)
    c.drawString(40, height - 60, f'Generated: {datetime.utcnow().isoformat()} UTC')

    y = height - 100
    c.setFont('Helvetica-Bold', 12)
    c.drawString(40, y, 'Description:')
    y -= 16
    c.setFont('Helvetica', 10)
    text = c.beginText(40, y)
    for line in (project.description or '').splitlines():
        text.textLine(line)
    c.drawText(text)
    y = text.getY() - 20

    if tasks:
        c.setFont('Helvetica-Bold', 12)
        c.drawString(40, y, 'Tasks:')
        y -= 16
        c.setFont('Helvetica', 10)
        for t in tasks:
            if y < 80:
                c.showPage()
                y = height - 40
            c.drawString(48, y, f'- {t.title} [{t.status}]')
            y -= 14

    if releases:
        y -= 10
        c.setFont('Helvetica-Bold', 12)
        c.drawString(40, y, 'Releases:')
        y -= 16
        c.setFont('Helvetica', 10)
        for r in releases:
            if y < 80:
                c.showPage()
                y = height - 40
            c.drawString(48, y, f'- {r.version} on {r.release_date} [{r.status}]')
            y -= 14

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def generate_task_report(task):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont('Helvetica-Bold', 14)
    c.drawString(40, height - 40, f'Task Report: {task.title}')
    c.setFont('Helvetica', 10)
    c.drawString(40, height - 60, f'Status: {task.status}  Progress: {task.progress}%')
    y = height - 100
    c.setFont('Helvetica-Bold', 12)
    c.drawString(40, y, 'Description:')
    y -= 16
    c.setFont('Helvetica', 10)
    text = c.beginText(40, y)
    for line in (task.description or '').splitlines():
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def generate_release_report(release):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont('Helvetica-Bold', 14)
    c.drawString(40, height - 40, f'Release Report: {release.version}')
    c.setFont('Helvetica', 10)
    c.drawString(40, height - 60, f'Project ID: {release.project_id}  Status: {release.status}')
    y = height - 100
    c.setFont('Helvetica-Bold', 12)
    c.drawString(40, y, 'Release Notes:')
    y -= 16
    c.setFont('Helvetica', 10)
    text = c.beginText(40, y)
    for line in (release.notes or '').splitlines():
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
