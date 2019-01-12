from flask import render_template, make_response
from flask import Flask
from flask import request
import requests
import os

app = Flask(__name__)

app.config['GOOGLE_RECAPTCHA_SECRET'] = os.environ.get(
    'GOOGLE_RECAPTCHA_SECRET')

global_captcha_response = None


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        resp = request.data
        print("resp", resp)
        print("request", request)
        print("request.form", request.form)
        print("request.args", request.args)
        print("g-recaptcha-response", request.form['g-recaptcha-response'])

        captcha_response = request.form['g-recaptcha-response']

        if is_recaptcha_validated(captcha_response):
            print("user has validated captcha")
            resp = make_response(
                render_template('base.html', is_validated=True))
            resp.set_cookie(
                key='captcha_response', value=captcha_response, max_age=600)

            return resp
        else:
            print("user has not validated captcha")

    # Check cookie for the recaptcha value
    # resp = make_response(render_template('base.html',))
    #
    # resp.set_cookie(key='captcha_response', value='expiresin10s', max_age=10)
    #
    # return resp
    if 'captcha_response' in request.cookies:
        return render_template('base.html', is_validated=True)
    else:
        return render_template('base.html', is_validated=False)


def is_recaptcha_validated(captcha_response_string):
    print("GOOGLE_RECAPTCHA_SECRET:", app.config['GOOGLE_RECAPTCHA_SECRET'])
    data = {
        'secret': app.config['GOOGLE_RECAPTCHA_SECRET'],
        'response': captcha_response_string
    }
    resp = requests.post(
        'https://www.google.com/recaptcha/api/siteverify', data=data)

    data = resp.json()

    return data['success']


# @app.route('/set_cookie', methods=['GET', 'POST'])
# def index():
#     resp = make_response(render_template('base.html',))
#
#     resp.set_cookie(key='captcha_response', value='expiresin10s', max_age=10)
#
#     return resp

if __name__ == '__main__':
    app.run(debug=True)
