from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    #
    id = request.query.get("id")
    label = request.query.get("label")
    s = session()
    entry = s.query(News).get(id)
    #
    entry.label = label
    s.commit()
    if __name__ == "__main__":
        redirect("/news")


@route("/update")
def update_news():
    news_s = get_news("https://news.ycombinator.com/newest", n_pages=5)
    s = session()
    news_bd = s.query(News).all()
    news_bd = [(n.title, n.author) for n in news_bd]
    for new in news_s:
        if (new["title"], new["author"]) not in news_bd:
            news = News(
                title=new["title"], author=new["author"], url=new["url"], comments=new["comments"], points=new["points"]
            )
            s.add(news)
            s.commit()
    if __name__ == "__main__":
        redirect("/news")


@route("/classify")
def classify_news():  # type: ignore
    s = session()
    model = NaiveBayesClassifier(alpha=0.01)
    list_of_train = s.query(News).filter(News.label is not None).all()
    x_train = []
    y_train = []
    for i in list_of_train:
        x_train.append(i.title)
        y_train.append(i.label)
    model.fit(x_train, y_train)
    news = s.query(News).filter(News.label is None).all()
    x = [i.title for i in news]
    y = model.predict(x)
    for i in range(len(news)):
        news[i].label = y[i]
    s.commit()
    return sorted(news, key=lambda i: i.label)  # type: ignore


if __name__ == "__main__":
    run(host="localhost", port=8080)
