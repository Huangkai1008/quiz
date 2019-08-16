from quiz.model.topic import Topic, Article


def create_topic(**attrs):
    """
    创建专栏/主题
    :param attrs:
    :return:
    """
    topic = Topic(**attrs)
    topic.create()
    return topic


def create_article(topic_id, **attrs):
    """
    创建文章
    :param topic_id:
    :param attrs:
    :return:
    """
    article = Article(topic_id=topic_id, **attrs)
    article.create()
    return article
