from django.shortcuts import render, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .pdf_extractor import extract_text
from .ai_analyzer import analyze_resume
from .models import ResumeAnalysis
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
import os
import hashlib
import io

def get_file_hash(file):
    hasher = hashlib.md5()
    for chunk in file.chunks():
        hasher.update(chunk)
    file.seek(0)
    return hasher.hexdigest()

def index(request):
    return render(request, 'analyzer/index.html')

def analyze(request):
    if request.method != 'POST':
        return render(request, 'analyzer/index.html', {'error': 'Invalid request.'})

    uploaded_file = request.FILES.get('resume')
    if not uploaded_file:
        return render(request, 'analyzer/index.html', {'error': 'Please upload a file.'})

    allowed_extensions = ['.pdf', '.docx', '.doc']
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()

    if file_ext not in allowed_extensions:
        return render(request, 'analyzer/index.html', {
            'error': 'Unsupported file type. Please upload a PDF or DOCX file.'
        })

    job_description = request.POST.get('job_description', '').strip()

    try:
        # Check for duplicate file — show same result if already analyzed
        file_hash = get_file_hash(uploaded_file)
        existing = ResumeAnalysis.objects.filter(file_hash=file_hash).first()
        if existing:
            return render(request, 'analyzer/result.html', {
                'analysis': existing,
                'duplicate': True
            })

        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        resume_text = extract_text(file_path)
        result = analyze_resume(resume_text, job_description if job_description else None)

        analysis = ResumeAnalysis.objects.create(
            filename=uploaded_file.name,
            file_hash=file_hash,
            score=result.get('score', 0),
            profile_summary=result.get('profile_summary', ''),
            strengths=result.get('strengths', []),
            weaknesses=result.get('weaknesses', []),
            missing_areas=result.get('missing_areas', []),
            suggestions=result.get('suggestions', []),
            keywords=result.get('keywords', []),
            section_scores=result.get('section_scores', {}),
            jd_match_score=result.get('jd_match_score', None),
            jd_match_details=result.get('jd_match_details', {}),
        )

        os.remove(file_path)

        return render(request, 'analyzer/result.html', {'analysis': analysis})

    except ValueError as e:
        return render(request, 'analyzer/index.html', {'error': str(e)})
    except Exception as e:
        return render(request, 'analyzer/index.html', {'error': f'Analysis failed: {str(e)}'})


def download_pdf(request, analysis_id):
    analysis = get_object_or_404(ResumeAnalysis, id=analysis_id)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=20, textColor=colors.HexColor('#4F46E5'))
    story.append(Paragraph("AI Resume Analysis Report", title_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>File:</b> {analysis.filename}", styles['Normal']))
    story.append(Paragraph(f"<b>Analyzed on:</b> {analysis.uploaded_at.strftime('%B %d, %Y %I:%M %p')}", styles['Normal']))
    story.append(Spacer(1, 12))

    score_color = colors.HexColor('#16a34a') if analysis.score >= 70 else colors.HexColor('#d97706') if analysis.score >= 40 else colors.HexColor('#dc2626')
    score_style = ParagraphStyle('Score', parent=styles['Normal'], fontSize=16, textColor=score_color)
    story.append(Paragraph(f"<b>Overall Score: {analysis.score}/100</b>", score_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Profile Summary</b>", styles['Heading2']))
    story.append(Paragraph(analysis.profile_summary, styles['Normal']))
    story.append(Spacer(1, 12))

    if analysis.section_scores:
        story.append(Paragraph("<b>Section Scores</b>", styles['Heading2']))
        section_data = [['Section', 'Score']]
        for section, score in analysis.section_scores.items():
            section_data.append([section.replace('_', ' ').title(), f"{score}/100"])
        table = Table(section_data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f3f4f6'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Strengths</b>", styles['Heading2']))
    for s in analysis.strengths:
        story.append(Paragraph(f"• {s}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Areas for Improvement</b>", styles['Heading2']))
    for w in analysis.weaknesses:
        story.append(Paragraph(f"• {w}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Missing Areas</b>", styles['Heading2']))
    for m in analysis.missing_areas:
        story.append(Paragraph(f"• {m}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Suggestions</b>", styles['Heading2']))
    for s in analysis.suggestions:
        story.append(Paragraph(f"• {s}", styles['Normal']))
    story.append(Spacer(1, 12))

    if analysis.keywords:
        story.append(Paragraph("<b>Keywords Found</b>", styles['Heading2']))
        story.append(Paragraph(", ".join(analysis.keywords), styles['Normal']))
        story.append(Spacer(1, 12))

    if analysis.jd_match_score is not None:
        story.append(Paragraph("<b>Job Description Match</b>", styles['Heading2']))
        story.append(Paragraph(f"Match Score: {analysis.jd_match_score}/100", styles['Normal']))
        if analysis.jd_match_details:
            matched = analysis.jd_match_details.get('matched_skills', [])
            missing = analysis.jd_match_details.get('missing_skills', [])
            rec = analysis.jd_match_details.get('recommendation', '')
            if matched:
                story.append(Paragraph(f"Matched Skills: {', '.join(matched)}", styles['Normal']))
            if missing:
                story.append(Paragraph(f"Missing Skills: {', '.join(missing)}", styles['Normal']))
            if rec:
                story.append(Paragraph(f"Recommendation: {rec}", styles['Normal']))

    doc.build(story)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_analysis_{analysis.id}.pdf"'
    return response

def result_detail(request, analysis_id):
    analysis = get_object_or_404(ResumeAnalysis, id=analysis_id)
    return render(request, 'analyzer/result.html', {'analysis': analysis})

# Create your views here.
