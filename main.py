#import Flask
from flask import Flask, render_template,request,session,flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, BooleanField, DateTimeField,
                    RadioField, TextField, TextAreaField)
from wtforms.validators import DataRequired
import glob
import numpy as np
import json
from collections import deque #container with max size
import yaml
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer


app= Flask(__name__)
app.config['SECRET_KEY'] ='minerva'

class InfoForm(FlaskForm):

    models = SelectField('Choose a model?', choices = [('Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch', 'Aerobic batch growth of Saccahomyces cerevisiae'),
                                                       ('Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch', 'Aerobic fed batch growth of Saccahomyces cerevisiae'),
                                                       ('Rx_Fermentation_MSucciniciproducens_Glucose_Anaerobic_Batch','Anaerobic growth of MSucciniciproducens in glucose'),
                                                       ('Rx_Fermentation_CGlutamicum_Glucose_Aerobic_Batch', 'Aerobic batch growth of Corynebacterium glutamicum'),
                                                       ('Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch', 'Aerobic batch growth of Escherichia coli by acetate cycling'),
                                                       ('Rx_Fermentation_MonodHerbert_Aerobic', 'Aerobic model of Monod')
                                                       ])


def create_plot(modelInUse):
    f = modelInUse()
    f.solve()
    t = f.solve()[0]
    C = f.solve()[1]
    graphJson= f.create_plot(t, C)
    return graphJson

def add_noise(modelInUse):
    f = modelInUse()
    f.solve()
    t = f.solve()[0]
    C = f.solve()[1]
    graphJson_noise= f.add_noise(t, C)
    return graphJson_noise

def parameter_to_Change(modelInUse):
    f=modelInUse()
    dictParameter = f.dict()
    # form=InfoForm()
    # parameters = SelectField('Choose a parameter to change?', choices=[([x for x in dictParameter], [dictParameter[x] for x in dictParameter])])
    # parametertoChange = form.parameters.data
    return dictParameter

#Render the index page IT IS THE DECORATOR
@app.route('/')
#What the page
def index():
    return render_template('fermproc.html')

@app.route('/rules')
def rules():
    return render_template('fermproc-rules.html')

@app.route('/howtomodels')
def howtomodels():
    return render_template('howtomodels.html')

@app.route('/model_library', methods=['GET', 'POST'])
def model_library():
    form = InfoForm()
    if request.method == 'POST':
        modelInUse = form.models.data
        if modelInUse == 'Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch':
            from static.models.Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch import \
                SCerevisiae_Fedbatch as modelInUse
        if modelInUse == 'Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch':
            from static.models.Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch import \
                SCerevisiae_Aero as modelInUse
            print(modelInUse)
        if modelInUse == 'Rx_Fermentation_MSucciniciproducens_Glucose_Anaerobic_Batch':
            from static.models.Rx_Fermentation_MSucciniciproducens_Glucose_Anaerobic_Batch import \
                MSucciniciproducens_anae as modelInUse
        if modelInUse == 'Rx_Fermentation_MonodHerbert_Aerobic':
            from static.models.Rx_Fermentation_MonodHerbert_Aerobic import Monod_Herbert as modelInUse
        if modelInUse == 'Rx_Fermentation_CGlutamicum_Glucose_Aerobic_Batch':
            from static.models.Rx_Fermentation_CGlutamicum_Glucose_Aerobic_Batch import \
                CGlutamicum_aerobic as modelInUse
        if modelInUse == 'Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch':
            from static.models.Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch import Ecoli_Aero as modelInUse
            print(modelInUse)
        graph = create_plot(modelInUse)
        return render_template('fermproc-plot.html', form=form, plot=graph)
    return render_template('fermproc-modellibrary.html',form=form)

@app.route('/simulator', methods=['GET', 'POST'])
def simulator():
    form = InfoForm()
    # if form.validate_on_submit():
    #     flash('You just selected a model!')
    #     return redirect(url_for('simulator'))
    if request.method == 'POST':
        modelInUse = form.models.data
        if modelInUse == 'Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch':
            from static.models.Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch import SCerevisiae_Fedbatch as modelInUse
            graph = create_plot(modelInUse)
            return render_template('fermproc-plot.html', form =form, plot = graph)
        if modelInUse == 'Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch':
            from static.models.Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch import SCerevisiae_Aero as modelInUse
            graph = create_plot(modelInUse)
            form = InfoForm()
            parameters = form.changeParameters(modelInUse)
            parametertoChange = form.parameters.data
            return render_template('fermproc-plot.html',form =form, plot=graph)
        if modelInUse == 'Rx_Fermentation_MSucciniciproducens_Glucose_Anaerobic_Batch':
            from static.models.Rx_Fermentation_MSucciniciproducens_Glucose_Anaerobic_Batch import MSucciniciproducens_anae as modelInUse
            graph = create_plot(modelInUse)
            return render_template('fermproc-plot.html',form =form, plot=graph)
        if modelInUse == 'Rx_Fermentation_MonodHerbert_Aerobic':
            from static.models.Rx_Fermentation_MonodHerbert_Aerobic import Monod_Herbert as modelInUse
            graph = create_plot(modelInUse)
            return render_template('fermproc-plot.html',form =form, plot=graph)
        if modelInUse == 'Rx_Fermentation_CGlutamicum_Glucose_Aerobic_Batch':
            from static.models.Rx_Fermentation_CGlutamicum_Glucose_Aerobic_Batch import CGlutamicum_aerobic as modelInUse
            graph = create_plot(modelInUse)
            return render_template('fermproc-plot.html',form =form, plot=graph)
        if modelInUse == 'Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch':
            from static.models.Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch import Ecoli_Aero as modelInUse
            graph = add_noise(modelInUse)
            return render_template('fermproc-plot.html',form =form, plot=graph)
    return render_template('fermproc_simulator.html', form=form)

@app.route('/plot', methods=['GET', 'POST'])
def plot(model):
    print("Under the void sky")
    graph=create_plot(modelInUse)
    form = InfoForm()
    parameters = form.changeParameters(modelInUse).data
    print(parameters)
    # if request.method == 'POST':
    #     explanation = form.explanation.data
    #     return render_template('fermproc-thankyou.html',form = explanation)

    return render_template('fermproc-plot.html', form =form, plot = graph)

@app.route("/test", methods = ['POST'])
def modelmodification():
    slider_change = request.form['slider_change']
    return slider_change

@app.route('/minigames')
def minigames():
    return render_template('fermproc-minigames.html')


@app.route('/test_scerevisiae')
def questionnaire_scerevisiae():
    return render_template('Scerevisiae-questionnarie.html')

@app.route('/answer_scerevisiae')
def answer_scerevisiae1():
    q1_ans = request.args.get('q1')
    print(q1_ans)
    if q1_ans == 'c3.1':
        answer = 'You are right. Saccharomyces cerevisiae will consume first the glucose by the oxidation pathway (in the bottom of the reactor), then the glucose by reduction (maybe in the middle of the reactor) and finally they will consume the ethanol after depletion of all glucose (in the top of the reactor). It is important to know that we are considering that our wee beasties have enough oxygen.'
    else:
        answer = 'Do not worry, it was a difficult question. You need to consider that microorganisms will consume first the glucose by the oxidation pathway (in the bottom of the reactor), then the glucose by reduction (maybe in the middle of the reactor) and finally they will consume the ethanol after depletion of all glucose (in the top of the reactor). It is important to know that we are considering that our wee beasties have enough oxygen.'
    return render_template('Scerevisiae-answer1.html',answer=answer)
@app.route('/answer_scerevisiae2')
def answer_scerevisiae2():
    q2_ans = request.args.get('q2')
    print(q2_ans)
    if q2_ans == 'c2.2':
        answer = 'You are right. Crabtree effect provides an important metabolic feature that increase the biomass, for example for beer production.'
    else:
        answer = 'Oh camon. You can do it better. And to do so I am leaving you here an article about Crabtree effect (R. H. De Deken, “The Crabtree Effect: A Regulatory System in Yeast,” J. Gen. Microbiol., vol. 44, no. 2, pp. 149–156, 1966.)'
    return render_template('Scerevisiae-answer2.html',answer=answer)
# def answer_scerevisiae2():
#     q1_ans = request.args.get('q1')
#     print(q1_ans)
#     if q1_ans == 'c2.2':
#         answer = 'Yes :) . '
#     else:
#         answer = 'You can do it better'
#     return render_template('Scerevisiae-answer2.html',answer=answer)

english_bot = ChatBot("Frosty")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train(yaml.load("/Users/simonetacanodelasheras/Desktop/Working_app/chatbot/data/english"))

@app.route("/frosty")
def frosty():
    return render_template("frosty.html")

@app.route("/frosty_answer")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ =='__main__':
    #set to False when you have production
    app.run(debug=True)
