from django.db import models


class Tags(models.Model):
    id = models.IntegerField(primary_key=True)
    tag = models.TextField()

    class Meta:
        managed = False
        db_table = 'public"."tags'


class UserRole(models.Model):
    id = models.IntegerField(primary_key=True)
    role = models.TextField()

    class Meta:
        managed = False
        db_table = 'public"."user_role'

class RoleTag(models.Model):
    id = models.IntegerField(primary_key=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, db_column='role')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, db_column='tag')

    class Meta:
        managed = False
        db_table = 'public"."role_tag'


class News(models.Model):
    body = models.TextField()
    header = models.TextField()
    id = models.IntegerField(primary_key=True)
    emo_color = models.TextField()
    news_date = models.DateTimeField()
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, db_column='tag')
    weight_tag = models.FloatField()


    def tag_name(self):
        return self.tag.tag
    class Meta:
        managed = False
        db_table = 'public"."news'


class NewsAll(models.Model):
    body = models.TextField()
    id = models.IntegerField(primary_key=True)
    news_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'public"."all_news'
