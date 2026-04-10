from django.contrib import admin
from .models import ResumeAnalysis

@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    
    # Columns shown in the list view
    list_display = ['id', 'filename', 'score', 'score_badge', 'jd_match_score', 'uploaded_at']
    
    # Filter sidebar on the right
    list_filter = ['uploaded_at']
    
    # Search bar at the top
    search_fields = ['filename', 'profile_summary']
    
    # Clickable link on these columns
    list_display_links = ['id', 'filename']
    
    # Default ordering
    ordering = ['-uploaded_at']
    
    # How many records per page
    list_per_page = 20

    # All fields are read only — no editing
    readonly_fields = [
        'filename',
        'file_hash',
        'score',
        'profile_summary',
        'strengths',
        'weaknesses',
        'missing_areas',
        'suggestions',
        'keywords',
        'section_scores',
        'jd_match_score',
        'jd_match_details',
        'uploaded_at',
    ]

    # Group fields nicely in detail view
    fieldsets = (
        ('File Info', {
            'fields': ('filename', 'file_hash', 'uploaded_at')
        }),
        ('Score', {
            'fields': ('score',)
        }),
        ('Profile', {
            'fields': ('profile_summary',)
        }),
        ('Analysis', {
            'fields': (
                'strengths',
                'weaknesses',
                'missing_areas',
                'suggestions',
            )
        }),
        ('Keywords & Sections', {
            'fields': ('keywords', 'section_scores')
        }),
        ('Job Description Match', {
            'fields': ('jd_match_score', 'jd_match_details'),
            'classes': ('collapse',)  # collapsed by default
        }),
    )

    # Custom color badge for score column
    def score_badge(self, obj):
        from django.utils.html import format_html
        if obj.score is None:
            return '-'
        if obj.score >= 70:
            color = '#16a34a'
            bg = '#dcfce7'
        elif obj.score >= 40:
            color = '#d97706'
            bg = '#fef9c3'
        else:
            color = '#dc2626'
            bg = '#fee2e2'
        return format_html(
            '<span style="background:{};color:{};padding:4px 12px;'
            'border-radius:99px;font-weight:600;font-size:12px;">{}/100</span>',
            bg, color, obj.score
        )
    score_badge.short_description = 'Score Badge'

    # Disable add button — resumes only come from uploads
    def has_add_permission(self, request):
        return False
