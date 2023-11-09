from sqlalchemy import create_engine, text
import os

# Obtém a string de conexão com o banco de dados do ambiente
db_connection_string = os.environ['DB_CONN']

# Cria uma conexão com o banco de dados
engine = create_engine(
  db_connection_string, 
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  })

# Carrega todos os jobs do banco de dados
def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from card"))
    results_as_dict = result.mappings().all()
    jobs = []
    for row in results_as_dict:
      jobs.append(row)
    return jobs

# Carrega um job específico do banco de dados
def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(
      text(f"SELECT * FROM card WHERE id = :val"),
      {"val": id}
    )
    rows = result.mappings().all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])

# Adiciona um job ao banco de dados
def add_job_to_db(data):
  with engine.connect() as conn:
    query = text("INSERT INTO card (card_title, card_description) VALUES (:card_title, :card_description);")

    conn.execute(query, 
                 {              
                  "card_title":data['card_title'],
                  "card_description":data['card_description']}              
    )

# Exclui um job do banco de dados
def delete_job_from_db(id):
  with engine.connect() as conn:
    conn.execute(
      text(f"delete from card WHERE id = :id"),
      {"id": id}
    )