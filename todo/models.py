from django.db import models


class ToDo(models.Model):
    user = models.ForeignKey('auth.User', related_name='ToDo', on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    deadline = models.CharField(max_length=200, blank=True, null=True)
    is_done = models.IntegerField(verbose_name="Is Done", default=0)
    updated_at = models.DateField(auto_now=True, verbose_name="Updated At")
    created_at = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Created At")
    status = models.CharField(max_length=100, default='ok')

    def __str__(self):
        return self.user.username +' - '+self.task+' - '

    def as_json(self):
        return dict(
            global_id=self.id,
            task=self.task,
            description=self.description,
            deadline=self.deadline,
            is_done=self.is_done,
            updated_at=str(self.updated_at),
            created_at=str(self.created_at),
            status=self.status,
        )
