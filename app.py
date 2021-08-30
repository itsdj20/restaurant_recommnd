from flask import Flask, render_template, url_for, flash, redirect, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
lko_rest=pd.read_csv(r"C:\Users\DJ\Desktop\application\res_indore.csv")
app = Flask(__name__)

def searching(name,lko_rest=lko_rest):
    rest_selected=lko_rest[lko_rest["name"]==name]
    rest_list1 = rest_selected.copy().loc[:,['name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines']]
    rest_list = pd.DataFrame(rest_list1)
    rest_list = rest_list.reset_index()
    rest_list = rest_list.rename(columns={'index': 'res_id'})
    rest_list.drop('res_id', axis=1, inplace=True)
    rest_list = rest_list.T
    rest_list = rest_list
    ans = rest_list.to_dict()
    res = [value for value in ans.values()]
    return res

def fav(location,mini,maxi,cuisine,guest,favourite,lko_rest=lko_rest):
    

    cost = maxi + 200

    x = cost / guest
    y = mini / guest

    lko_rest1 = lko_rest.copy().loc[lko_rest['locality'] == location]

 

    lko_rest_locale = lko_rest1.copy()

    lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] <= x]
    lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] >= y]

    lko_rest_locale['Start'] = lko_rest_locale['cuisines'].str.find(cuisine)
    lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]

   
    
    favr = lko_rest.loc[lko_rest['name'] == favourite].drop_duplicates()
    favr = pd.DataFrame(favr)
    lko_rest3 = pd.concat([favr, lko_rest_cui])
    lko_rest3.drop('Start', axis=1, inplace=True)
    lko_rest3.drop_duplicates(subset="name", keep="first", inplace=True)
    lko_rest1 = lko_rest3.reset_index()
    from sklearn.feature_extraction.text import CountVectorizer

    count1 = CountVectorizer(stop_words='english')
    count_matrix = count1.fit_transform(lko_rest1['highlights'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    sim = list(enumerate(cosine_sim2[0]))
    sim = sorted(sim, key=lambda x: x[1], reverse=True)
    sim = sim[1:11]
    indi = [i[0] for i in sim]

    final = lko_rest1.copy().iloc[indi[0]]
    final = pd.DataFrame(final)
    final = final.T

    for i in range(1, len(indi)):
        final1 = lko_rest1.copy().iloc[indi[i]]
        final1 = pd.DataFrame(final1)
        final1 = final1.T
        final = pd.concat([final, final1])
    rest_list1 = final.copy().loc[:,['name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines']]
    rest_list = pd.DataFrame(rest_list1)
    rest_list = rest_list.reset_index()
    rest_list = rest_list.rename(columns={'index': 'res_id'})
    rest_list.drop('res_id', axis=1, inplace=True)
    rest_list = rest_list.T
    rest_list = rest_list
    ans = rest_list.to_dict()
    res = [value for value in ans.values()]
    return res



def rate(location,mini,maxi,cuisine,guest,lko_rest=lko_rest):
    
    cost = maxi + 200

    x = cost / guest
    y = mini / guest

    lko_rest1 = lko_rest.copy().loc[lko_rest['locality'] == location]
    lko_rest_locale = lko_rest1.copy()
    lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] <= x]
    lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] >= y]
    lko_rest_locale['Start'] = lko_rest_locale['cuisines'].str.find(cuisine)
    lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
    lko_rest_cui = lko_rest_cui.sort_values('aggregate_rating', ascending=False)
    rest_selected = lko_rest_cui.head(10)
    rest_list1 = rest_selected.copy().loc[:,['name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines']]
    rest_list = pd.DataFrame(rest_list1)
    rest_list = rest_list.reset_index()
    rest_list = rest_list.rename(columns={'index': 'res_id'})
    rest_list.drop('res_id', axis=1, inplace=True)
    rest_list = rest_list.T
    rest_list = rest_list
    ans = rest_list.to_dict()
    res = [value for value in ans.values()]
    return res



@app.route("/")
@app.route("/home")
def home():
    return render_template('Home.html')

@app.route("/explore")
def explore():
    return render_template('Search.html')

@app.route("/preference1")
def preference1():
    return render_template('preference1.html')

@app.route("/preference2")
def preference2():
    return render_template('preference2.html')
    
@app.route("/output", methods=['POST'])
def output():
    if request.method == 'POST':
        try:
            loc = request.form['loc']
            mini = int(request.form['min'])
            maxi =int(request.form['max'])
            cuisine = request.form['cuis']
            guest = int(request.form['guest'])
        except:
            name=(request.form['search'])
            return render_template('output.html', title='Search', restaurants=searching(name))
        try:
            favorite=request.form['ok']
            return render_template('output.html', title='Search', restaurants=fav(loc, mini, maxi, cuisine, guest, favorite))
        except:
            return render_template('output.html', title='Search', restaurants=rate(loc, mini, maxi, cuisine, guest))
        
    else:
        return redirect(url_for('explore'))


if __name__ == '__main__':
    app.run(debug=True)