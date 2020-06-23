@task(name="update_related_articles_async")
def update_related_articles_async():

    #Collect list of article texts
    articles = Article.objects.filter(published=True)
    texts = []

    for article in articles:
        texts.append(article.content.replace("~~~", ""))

    #Attain similarity matrix
    tfidf = TfidfVectorizer().fit_transform(texts)
    pairwise_similarity = tfidf * tfidf.T

    #For each article, save the id's of the top 3 similar articles, other than itself
    for i, similarities in enumerate(pairwise_similarity.toarray()):

        most_similar_articles = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:4]
        similar_article_ids = []

        for j in most_similar_articles:

            if (articles[i].id != articles[j].id):

                similar_article_ids.append(articles[j].id)

        #Save ids to related articles field
        save_string = ""

        for id in similar_article_ids:
            save_string += str(id) + ","

        articles[i].related_article_ids = save_string
        Article.objects.filter(id=articles[i].id).update(related_article_ids=save_string)

    return
