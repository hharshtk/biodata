from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, BiodataForm
from .models import BiodataProfile
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from io import BytesIO
from django.http import HttpResponse
import os
from django.conf import settings

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def create_biodata(request):
    biodata, created = BiodataProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = BiodataForm(request.POST, request.FILES, instance=biodata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Biodata saved successfully!')
            return redirect('view_biodata')
    else:
        form = BiodataForm(instance=biodata)

    return render(request, 'profiles/create_biodata.html', {'form': form})

@login_required
def view_biodata(request):
    try:
        biodata = BiodataProfile.objects.get(user=request.user)
        return render(request, 'profiles/view_biodata.html', {'biodata': biodata})
    except BiodataProfile.DoesNotExist:
        messages.warning(request, 'Please create your biodata first.')
        return redirect('create_biodata')

@login_required
def download_pdf(request):
    try:
        biodata = BiodataProfile.objects.get(user=request.user)
    except BiodataProfile.DoesNotExist:
        messages.warning(request, 'Please create your biodata first.')
        return redirect('create_biodata')

    # Create the PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1
    )
    elements.append(Paragraph("Marriage Biodata", title_style))

    # Add photo if exists
    if biodata.photo:
        img_path = os.path.join(settings.MEDIA_ROOT, biodata.photo.name)
        if os.path.exists(img_path):
            img = Image(img_path, width=150, height=200)
            elements.append(img)
            elements.append(Spacer(1, 20))

    # Personal Information
    elements.append(Paragraph("Personal Information", styles['Heading2']))
    elements.append(Paragraph(f"Name: {biodata.user.get_full_name()}", styles['Normal']))
    elements.append(Paragraph(f"Gender: {biodata.get_gender_display()}", styles['Normal']))
    elements.append(Paragraph(f"Date of Birth: {biodata.date_of_birth}", styles['Normal']))
    elements.append(Paragraph(f"Height: {biodata.height} cm", styles['Normal']))
    elements.append(Paragraph(f"Marital Status: {biodata.marital_status}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Education and Career
    elements.append(Paragraph("Education and Career", styles['Heading2']))
    elements.append(Paragraph(f"Education: {biodata.education}", styles['Normal']))
    elements.append(Paragraph(f"Occupation: {biodata.occupation}", styles['Normal']))
    elements.append(Paragraph(f"Annual Income: {biodata.annual_income}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Family Information
    elements.append(Paragraph("Family Information", styles['Heading2']))
    elements.append(Paragraph(f"Father's Name: {biodata.father_name}", styles['Normal']))
    elements.append(Paragraph(f"Father's Occupation: {biodata.father_occupation}", styles['Normal']))
    elements.append(Paragraph(f"Mother's Name: {biodata.mother_name}", styles['Normal']))
    elements.append(Paragraph(f"Mother's Occupation: {biodata.mother_occupation}", styles['Normal']))
    elements.append(Paragraph(f"Number of Siblings: {biodata.siblings}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # Create response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{biodata.user.get_full_name()}_biodata.pdf"'
    response.write(pdf)

    return response
