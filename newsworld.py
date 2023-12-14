from flask import Flask, render_template, request
from newsapi import NewsApiClient

app = Flask(__name__)
app.debug = True
newsapi = NewsApiClient(api_key='651f6abc0842473dad925297b3363f20')

@app.route('/')
def introduction():
    return render_template('introduction.html')


@app.route('/search', methods=['GET', 'POST'])
def search_news():
    if request.method == 'POST':
        keywords = request.form['keywords']
        num_results = int(request.form['num_results'])
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        language_code = request.form['language']
        show_source = 'show_source' in request.form
        show_author = 'show_author' in request.form
        show_description = 'show_description' in request.form
        show_published_at = 'show_published_at' in request.form
        sort_by = request.form['sort_by']


        # Call NewsAPI to get search results
        search_results = newsapi.get_everything(q=keywords, from_param=start_date, to=end_date,
                                                 language=language_code, sort_by=sort_by, page_size=num_results)

        return render_template('search_results.html', keywords=keywords, results=search_results['articles'],
                               show_source=show_source, show_author=show_author,
                               show_description=show_description, show_published_at=show_published_at)

    return render_template('search.html')


@app.route('/trends', methods=['GET', 'POST'])
def view_trends():
    if request.method == 'POST':
        country = request.form['country']
        category = request.form['category']
        show_source = 'show_source' in request.form
        show_author = 'show_author' in request.form
        show_description = 'show_description' in request.form
        show_published_at = 'show_published_at' in request.form

        # Call NewsAPI to get top headlines
        trends_results = newsapi.get_top_headlines(country=country, category=category, language='en')

        return render_template('trends_results.html', country=country, category=category,
                                results=trends_results['articles'], show_source=show_source,
                                show_author=show_author, show_description=show_description,
                                show_published_at=show_published_at)

    return render_template('trends.html')



if __name__ == '__main__':
    app.run()
