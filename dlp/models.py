from django.db import models

class Pattern(models.Model):
    name = models.CharField(max_length=100)
    regex = models.TextField()

    def __str__(self):
        return self.name

class Message(models.Model):
    slack_ts = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    file_name = models.CharField(max_length=255)
    content = models.TextField()
    pattern = models.ForeignKey(Pattern, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.content}"
