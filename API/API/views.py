import datetime

from rest_framework import views, mixins, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from bertopic import BERTopic
from API.models import News, NewsAll, RoleTag, Tags, UserRole


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'body', 'header', 'emo_color', 'news_date', 'weight_tag', 'tag_name')


class NewsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        role = query_params.get('role')
        if role:
            role_id = UserRole.objects.filter(role=role).first()
            rt = RoleTag.objects.filter(role=role_id).values_list('tag', flat=True)
            qs = News.objects.filter(tag__id__in=rt).order_by('-weight_tag')
            return qs
        return super().get_queryset()


def clusters_of_news(docs):
    model = BERTopic(language="russian", diversity=0.2)
    text = []
    for d in docs:
        text.append(d)
    topics, probs = model.fit_transform(text)
    return model


class BestNews(views.APIView):
    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        start_date = query_params.get('start_date')
        end_date = query_params.get('end_date')
        custer_num = query_params.get('custer_num')
        if not start_date and end_date:
            return Response(status=400)
        start_date = datetime.datetime.strptime(start_date, "%d%m%Y").date()
        end_date = datetime.datetime.strptime(end_date, "%d%m%Y").date()
        news = NewsAll.objects.filter(news_date__range=[start_date, end_date]).values_list('body', flat=True)
        model_ready = clusters_of_news(news)
        if custer_num:
            return Response(model_ready.get_topic(int(custer_num)))
        return Response(model_ready.topic_labels_)
