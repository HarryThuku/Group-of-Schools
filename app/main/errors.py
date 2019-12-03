from flask import render_template
from . import main
# General Application Data
from config import appData

@main.app_errorhandler(404)
def four_Ow_four(error):
    '''
    Function to render the 404 error page
    '''
    title = "fourOwfour."
    context = {
        'title' : title,
        'appData' : appData
    }
    return render_template('fourOwfour.html', context = context),404