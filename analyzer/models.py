from django.db import models

class ResumeAnalysis(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=64, blank=True)  # for duplicate detection
    score = models.IntegerField(null=True)
    profile_summary = models.TextField(blank=True)
    strengths = models.JSONField(default=list)
    weaknesses = models.JSONField(default=list)
    missing_areas = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    keywords = models.JSONField(default=list)
    section_scores = models.JSONField(default=dict)
    jd_match_score = models.IntegerField(null=True, blank=True)
    jd_match_details = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.filename} — {self.score}/100"
