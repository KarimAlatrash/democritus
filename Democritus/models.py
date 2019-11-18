from django.db import models
from django.forms import ValidationError
import re
import csv
from django.db.models import signals
from Democritus.GoogleAPI import create_new_poll, generate_id, delete_poll


def poll_created(sender, instance, created, *args, **kwargs):
    """Argument explanation:

           sender - The model class. (Poll)
           instance - The actual instance being saved.
           created - Boolean; True if a new record was created.

           *args, **kwargs - Capture the unneeded `raw` and `using`(1.3) arguments.
        """

    create_new_poll(instance, not created)


def poll_changed(sender, instance, *args, **kwargs):
    return


class StudentList(models.Model):
    def validate_list(self):
        try:
            readCSV = csv.reader([self.read().decode("utf-8")])
            for row in readCSV:
                for idx, email in enumerate(row):
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        raise ValidationError(u'The file contains a value that is not an email [' + str(idx) + ']')
                    if not email.endswith('tdsb.on.ca'):
                        raise ValidationError(u'The file contains a non-TDSB email [' + str(idx) + ']')
        except:
            raise ValidationError(u'The file is not in expected CSV format')

    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='uploaded_files', validators=[validate_list])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Poll(models.Model):
    POLL_TYPES = (('RK', 'Ranked'), ('CO', 'Choose One'), ('SA', 'Select All'))
    poll_type = models.CharField(max_length=2, choices=POLL_TYPES, default='RK')
    question_text = models.CharField(max_length=200)
    options = models.CharField(max_length=2000)
    start_date = models.DateTimeField('Start Time')
    end_date = models.DateTimeField('End Time')
    student_list = models.ForeignKey(StudentList, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, max_length=100, editable=False, default=generate_id())

    def __str__(self):
        return '(' + self.poll_type + ') ' + self.question_text


signals.post_save.connect(poll_created, sender=Poll)
signals.post_delete.connect(delete_poll, sender=Poll)
