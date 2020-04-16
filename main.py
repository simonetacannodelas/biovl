import Flask
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
from utils.model_library_variables import models as model_variables

app= Flask(__name__)
app.config['SECRET_KEY'] ='minerva'

global_model_state = dict()

class global_model:

    def __init__(self):
        self.global_model_state = dict()

    def get_global_model_state(self):
        return self.global_model_state

    def select_variable(self):
        self.global_model_state['model'] = model
        self.global_model_state['model_variable_param'] = model_variable_param
        return model, model_variable_param

    def update_model_param_and_get_updated_graph(self, variable_param, new_value):
        print('variable_param : {}'.format(variable_param))
        print('new_value : {}'.format(new_value))

        current_model = self.global_model_state['model']()

        if not hasattr(current_model, 'update_param_value'):
            print("Current Model does not contain a function 'update_param_value'.")
            return

        current_model.update_param_value(variable_param, new_value)
        current_model.solve()
        t = current_model.solve()[0]
        C = current_model.solve()[1]

        graphJson = current_model.create_plot(t, C)

        return graphJson

    def add_noise(self):
        # global_model_state['model'] = modelInUse()

        f = self.global_model_state['model']
        f.solve()
        t = f.solve()[0]
        C = f.solve()[1]
        graphJson_noise = f.add_noise(t, C)
        return graphJson_noise

    def parameter_to_Change(self):
        # global_model_state['model'] = modelInUse()
        f = self.global_model_state['model']()
        dictParameter = f.dict()['description']
        # form=InfoForm()
        # parameters = SelectField('Choose a parameter to change?', choices=[([x for x in dictParameter], [dictParameter[x] for x in dictParameter])])
        # parametertoChange = form.parameters.data
        return dictParameter



class InfoForm(FlaskForm):

    models = SelectField('Choose a model?', choices = [('Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch', 'Aerobic batch growth of Saccahomyces cerevisiae'),
                                                       ('Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch', 'Aerobic fed batch growth of Saccahomyces cerevisiae'),
                                                       ('Rx_Fermentation_MSucciniciproducens_Glucose_Anaerobic_Batch','Anaerobic growth of MSucciniciproducens in glucose'),
                                                       ('Rx_Fermentation_CGlutamicum_Glucose_Aerobic_Batch', 'Aerobic batch growth of Corynebacterium glutamicum'),
                                                       ('Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch', 'Aerobic batch growth of Escherichia coli by acetate cycling'),
                                                       ('Rx_Fermentation_MonodHerbert_Aerobic', 'Aerobic model of Monod')
                                                       ])

#Display of variables
class ModelVariablesForm(FlaskForm):
    model_name = ""
    model_variable_param = SelectField('Choose a variable', choices=[])

#create object of the class for the model
global_model_object = global_model()
global_model_state = global_model_object.global_model_state
print(global_model_state)

def create_plot(model):
    if model== 'Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch':
        from static.models.Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch import \
            SCerevisiae_Fedbatch as modelInUse
        f = modelInUse()
        f.solve()
        t = f.solve()[0]
        C = f.solve()[1]
        graphJson = f.create_plot(t, C)
    if model == 'Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch':
        from static.models.Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch import \
            SCerevisiae_Aero as modelInUse
        f = modelInUse()
        f.solve()
        t = f.solve()[0]
        C = f.solve()[1]
        graphJson = f.create_plot(t, C)
    if model== 'Rx_Fermentation_MSucciniciproducens_Glucose_Anaerobic_Batch':
        from static.models.Rx_Fermentation_MSucciniciproducens_Glucose_Anaerobic_Batch import \
            MSucciniciproducens_anae as modelInUse
        f = modelInUse()
        f.solve()
        t = f.solve()[0]
        C = f.solve()[1]
        graphJson = f.create_plot(t, C)
    if model== 'Rx_Fermentation_MonodHerbert_Aerobic':
        from static.models.Rx_Fermentation_MonodHerbert_Aerobic import Monod_Herbert as modelInUse
        f = modelInUse()
        f.solve()
        t = f.solve()[0]
        C = f.solve()[1]
        graphJson = f.create_plot(t, C)
    if model == 'Rx_Fermentation_CGlutamicum_Glucose_Aerobic_Batch':
        from static.models.Rx_Fermentation_CGlutamicum_Glucose_Aerobic_Batch import \
            CGlutamicum_aerobic as modelInUse
        f = modelInUse()
        f.solve()
        t = f.solve()[0]
        C = f.solve()[1]
        graphJson = f.create_plot(t, C)
    if model == 'Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch':
        from static.models.Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch import Ecoli_Aero as modelInUse
        f = modelInUse()
        f.solve()
        t = f.solve()[0]
        C = f.solve()[1]
        graphJson = f.create_plot(t, C)
    return graphJson

@app.route('/update_current_model_param_value', methods=['GET', 'POST'])
def update_current_model_param_value(global_model_object):
    if request.method == 'POST':

        print(request.form)
        print(request.data)

        form_data = request.form.to_dict()
        variable_param = form_data.get('model_variable_param', None)
        new_value = form_data.get('new_value', None)

        if variable_param is None : print("variable_param is None from form_data"); return {}
        if new_value is None: print("new_value is None from form_data"); return {}


        return global_model_object.update_model_param_and_get_updated_graph(variable_param, new_value)

    return {}

# def update_model_param_and_get_updated_graph(variable_param, new_value):
#     print('variable_param : {}'.format(variable_param))
#     print('new_value : {}'.format(new_value))
#
#     global global_model_state
#
#     current_model = global_model_state['model']()
#
#     if not hasattr(current_model, 'update_param_value'):
#         print("Current Model does not contain a function 'update_param_value'.")
#         return
#
#     current_model.update_param_value(variable_param, new_value)
#     current_model.solve()
#     t = current_model.solve()[0]
#     C = current_model.solve()[1]
#
#     graphJson = current_model.create_plot(t, C)
#
#     return graphJson


# def create_plot(modelInUse):
#     global global_model_state
#     # global_model_state['model'] = modelInUse()
#     f = global_model_state['model']()
#     f.solve()
#     t = f.solve()[0]
#     C = f.solve()[1]
#     graphJson= f.create_plot(t, C)
#     return graphJson

# def add_noise(modelInUse):
#     global global_model_state
#     # global_model_state['model'] = modelInUse()
#
#     f = global_model_state['model']
#     f.solve()
#     t = f.solve()[0]
#     C = f.solve()[1]
#     graphJson_noise= f.add_noise(t, C)
#     return graphJson_noise
#
# def parameter_to_Change(modelInUse):
#     global global_model_state
#     # global_model_state['model'] = modelInUse()
#
#     f = global_model_state['model']()
#     dictParameter = f.dict()
#     # form=InfoForm()
#     # parameters = SelectField('Choose a parameter to change?', choices=[([x for x in dictParameter], [dictParameter[x] for x in dictParameter])])
#     # parametertoChange = form.parameters.data
#     return dictParameter

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
    if request.method == "GET":
        return render_template('fermproc-modellibrary.html', form=form)


@app.route('/model_library_select_variable', methods=['GET', 'POST'])
def model_library_select_variable():

    #global global_model_state

    data = request.form.to_dict()
    selected_model_name = data['models']

    global_model_state['model_name'] = selected_model_name
    global_model_state['model'] = get_model_from_model_name(selected_model_name)

    variables = model_variables.get(selected_model_name, [])
    variables_form = ModelVariablesForm()
    variables_form.model_name = selected_model_name
    for variable_name, description in variables.items():
        variables_form.model_variable_param.choices.append((variable_name, description))

    return render_template('fermproc-modellibrary-select-variable.html', form=variables_form, selected_model_name=selected_model_name)

@app.route('/model_library_view_model', methods=['GET', 'POST'])
def model_library_view_model():

    if request.method == 'POST':

        request_data = request.form.to_dict()
        print("request_data")
        print(request_data)

        #global global_model_state

        model_name = global_model_state.get('model_name')
        model_variable_param = request_data.get('model_variable_param')


        model = get_model_from_model_name(model_name)

        global_model_state['model'] = model
        global_model_state['model_variable_param'] = model_variable_param

        print("model is None")
        print(model is None)

        graph = create_plot(model)
        form = InfoForm()

        print("graph")
        print(str(graph))

        page_data = {
            'plot' : graph,
            'model_name' : model_name,
            'model_variable_param' : model_variable_param,
            'form' : form,
        }

        return render_template('fermproc-plot.html', **page_data)

    # if request.method == "GET":
    form = InfoForm()
    return render_template('fermproc-modellibrary-view-model.html', form=form)


@app.route("/view_timed_graph", methods=['GET', 'POST'])
def view_timed_graph():
    if request.method == 'POST':

        request_data = request.form.to_dict()
        print("request_data")
        print(request_data)

        plot = create_plot("")

        request_data['model_name'] = global_model_state['model_name']
        request_data['plot'] = plot

        return render_template('fermproc-view-timed-graph.html', **request_data)

    # if request.method == "GET":
    form = InfoForm()
    return render_template('fermproc-modellibrary-view-model.html', form=form)

@app.route('/get_timed_graphs_ajax')
def get_timed_graphs():
    graphs = []

    for i in range(5, 31, 5):
        t_end = i
        graph = update_model_param_and_get_updated_graph("t_end", t_end)
        graphs.append(graph)

        print("Added graph for t_end : {}".format(t_end))

    return {'graphs' : graphs}

@app.route('/timed_graph_popup_window')
def timed_graph_popup_window():

    selected_model_name = global_model_object['model_name']

    variables = model_variables.get(selected_model_name, [])
    variables_form = ModelVariablesForm()
    variables_form.model_name = selected_model_name
    for variable_name, description in variables.items():
        variables_form.model_variable_param.choices.append((variable_name, description))

    return render_template('fermproc-modellibrary-timed-graph-popup.html', form=variables_form,
                           selected_model_name=selected_model_name)



@app.route('/value_from_slider', methods=['GET', 'POST'])
def calculate_value_from_slider():

    form_data = request.form.to_dict()
    variable_param = form_data['variable_param']
    print('variable_param')
    print(variable_param)
    return {'value' : 5}

@app.route('/range_slider_test')
def range_slider():

    page_data = {
        'value': value,
        'slider_min_value': slider_min_value,
        'slider_max_value': slider_max_value,
        'slider_step_value': slider_step_value

    }

    return render_template('range-slider-test.html', **page_data)

def get_model_from_model_name(model_name):

    if model_name == 'Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch':
        from static.models.Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch import \
            SCerevisiae_Fedbatch as modelInUse
    if model_name == 'Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch':
        from static.models.Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch import \
            SCerevisiae_Aero as modelInUse
        # print(modelInUse)
    if model_name == 'Rx_Fermentation_MSucciniciproducens_Glucose_Anaerobic_Batch':
        from static.models.Rx_Fermentation_MSucciniciproducens_Glucose_Anaerobic_Batch import \
            MSucciniciproducens_anae as modelInUse
    if model_name == 'Rx_Fermentation_MonodHerbert_Aerobic':
        from static.models.Rx_Fermentation_MonodHerbert_Aerobic import Monod_Herbert as modelInUse
    if model_name == 'Rx_Fermentation_CGlutamicum_Glucose_Aerobic_Batch':
        from static.models.Rx_Fermentation_CGlutamicum_Glucose_Aerobic_Batch import \
            CGlutamicum_aerobic as modelInUse
    if model_name == 'Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch':
        from static.models.Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch import Ecoli_Aero as modelInUse
    print(model_name)
    return model_name

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
            graph = global_model().create_plot(modelInUse)
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
def plot(model_name):
    graph=global_model_object.create_plot(model_name)
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
trainer.train(yaml.load("chatbot/data/english"))

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
