from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_job_to_db, delete_job_from_db

# Cria uma instância do Flask
app = Flask(__name__)

# Define a rota principal da aplicação e exibe todos os jobs
@app.route("/")
def hello_daniel():
  jobs = load_jobs_from_db()
  return render_template('home.html', 
                         jobs=jobs)


# Cria um novo job
@app.route("/job/create", methods=['post'])
def apply_to_job():
  data = request.form
  add_job_to_db(data)
  jobs = load_jobs_from_db()
  return render_template('home.html', 
                         application=data,
                         jobs=jobs)

# Exclui um job
@app.route("/job/delete/<id>", methods=['post'])
def delete_job(id):
  delete_job_from_db(id)  
  jobs = load_jobs_from_db()
  return render_template('home.html', 
                         id=id, jobs=jobs)


if __name__ == '__main__':
  app.run(host='0.0.0.0',  debug=True, port=8080)