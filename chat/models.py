from django.db import models

class History(models.Model):
    chat_time = models.DateTimeField()
    query = models.TextField()
    answer = models.TextField()
    sim1 = models.FloatField()
    sim2 = models.FloatField()
    sim3 = models.FloatField()

    def __str__(self):
        return self.chat_time.strftime('%Y-%m-%d %H:%M:%S')
