import logging

from flask import Flask, render_template, jsonify, request
from db import get_projects, add_projects , get_responses, submit_response

app = Flask(__name__)



@app.route('/projects', methods = ['POST','GET'])
def projects():
  if request.method == 'POST':
    if not request.is_json:
      return jsonify({"msg":"Missing Json Data in Request"}), 400
      # return jsonify(request.form)
    
    add_projects(request.get_json())
    return 'Your Survey Was Created'
  
  return get_projects()
  
 
@app.route('/responses', methods=['POST','GET'])
def user_responses():
  if request.method == 'POST':
    if not request.is_json:
      return jsonify({"msg":"Missing Json Data in Request"}), 400
    
    submit_response(request.get_json())
    return 'Thanks for submitting your Response, Success!'
  
  return get_responses()
   
@app.route('/')
def hello():
  user_email = request.headers.get('X-Goog-Authenticated-User-Email')
  user_id = request.headers.get('X-Goog-Authenticated-User-ID')
  
  page = render_template('index.html', email=user_email, id=user_id)
  return page

# @app.errorhandler(500)
# def server_error(e):
#     logging.exception('An error occurred during a request.')
#     return """
#     An internal error occurred: <pre>{}</pre>
#     See logs for full stacktrace.
#     """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run()
# [END gae_flex_python_static_files]
