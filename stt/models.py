from django.db import models

# Create your models here.

# 긴급 구조 신고 전화기록
class EmergencyCalls(models.Model):
    
    date = models.DateTimeField(auto_now_add=True, verbose_name="신고 날짜")
    category = models.CharField(max_length=255, verbose_name="사건 분류")
    location = models.CharField(max_length=255, verbose_name="사건 발생 장소")
    details = models.TextField(verbose_name="구체적인 현장 상태", null=True)
    address_name = models.CharField(max_length=255, verbose_name="추정 주소", null=True)
    place_name = models.CharField(max_length=255, verbose_name="추정 장소", null=True)
    phone_number = models.CharField(max_length=20, verbose_name="전화번호", null=True)
    lat = models.FloatField(verbose_name="위도", null=True)
    lng = models.FloatField(verbose_name="경도", null=True)
    
    def __str__(self):
        return f"{self.date} - {self.category} at {self.location}"

    class Meta:
        ordering = ['-date']

# 전체 신고 전화기록
class CallLogs(models.Model):
    EMERGENCY_CHOICES = [
        ('emergency', '구급'),
        ('non_emergency', '비구급'),
    ]

    date = models.DateTimeField(auto_now_add=True, verbose_name="신고 날짜")
    category = models.CharField(max_length=255, verbose_name="사건 분류")
    location = models.CharField(max_length=255, verbose_name="사건 발생 장소")
    details = models.TextField(verbose_name="구체적인 현장 상태", null=True)
    address_name = models.CharField(max_length=255, verbose_name="추정 주소", null=True)
    place_name = models.CharField(max_length=255, verbose_name="추정 장소", null=True)
    phone_number = models.CharField(max_length=20, verbose_name="전화번호", null=True)
    full_text = models.TextField(verbose_name="전체 신고 기록", null=True)
    is_duplicate = models.BooleanField(default=False, verbose_name="중복 신고 여부")
    emergency_type = models.CharField(max_length=15, choices=EMERGENCY_CHOICES, verbose_name="구급 여부")
    audio_file = models.FileField(upload_to='audio_files/', verbose_name="음성 파일", null=True)
    lat = models.FloatField(verbose_name="위도", null=True)
    lng = models.FloatField(verbose_name="경도", null=True)

    def __str__(self):
        return f"{self.date} - {self.category} at {self.location}"

    class Meta:
        ordering = ['-date']