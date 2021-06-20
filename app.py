from flask import Flask, render_template, url_for, request
import numpy as np
import pickle
from werkzeug.utils import redirect
from GameRec import make_recommendation
import settings

app  = Flask(__name__)

 


@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template ('index.html', recommendations = [])
    else:
        return render_template ('index.html')


@app.route('/recommend',methods=['POST', 'GET'])
def recommend():
     recommendation_list = []
     if (request.method == "POST"): 
        features = ""
        features = list((str (x) for x in request.form.values()))

        cosine_sim = make_recommendation(features)

        sim_scores = list(enumerate(cosine_sim[-1,:]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        for i in range(1, 13):
            indx = sim_scores[i][0]
            
            format_dec = "{:.2f}%".format((((sim_scores[i][1])+1.0)/2.0)*100.0)
            tmp = [settings.games['Name'].iloc[indx],settings.games['Genre'].iloc[indx],settings.games['Platform'].iloc[indx], settings.games['Year_of_Release'].iloc[indx], settings.games['Publisher'].iloc[indx],
            settings.games['Critic_Score'].iloc[indx], settings.games['User_Score'].iloc[indx], settings.games['Rating'].iloc[indx], format_dec]
            recommendation_list.append(tmp)
            

        headings = ("Game", "Genre", "Platform", "Year of release", "Publisher", "Critic score", "User score", "Rating", "Compatibility")
        return render_template('index.html', recommendations =  recommendation_list, headings = headings)   

        # recommendation_list.append(make_recommendation(features))
        # return render_template('index.html', recommendations =  recommendation_list)
     else :
         recommendation_list = []
         return render_template ('home')
         


# @app.route ("/<reco>")
# def prnt(reco):
#     return f"<h1>hiii</h1>"

@app.route ('/refresh',methods=['GET'])
def refresh():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)
    app.run(host='0.0.0.0')