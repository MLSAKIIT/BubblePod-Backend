from flask import Flask, redirect, url_for, request
import run
app = Flask(__name__)
  
  
@app.route('/bubblepod/entry/',methods = ['POST'])
def get_data():
    content = request.get_json()
    run.store_data(content)
    return content


@app.route('/bubblepod/similar/',methods = ['POST'])
def send_data():
    content = request.get_json()
    output = run.retrieve_data(content)    
    return output
    
  
if __name__ == '__main__':
   app.run(debug = True)