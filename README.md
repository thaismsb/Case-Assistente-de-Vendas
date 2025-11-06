# 🐾 Case Petlove – Assistente de Recomendação

Um projeto com **API Backend** e **interface Streamlit** para responder perguntas e gerar recomendações sobre produtos para pets usando IA.  

---

##  Rodando a aplicação localmente

###  Backend (API)
```bash
# Construir a imagem Docker
docker build --no-cache -t case_petlove_api .

# Parar containers antigos (se existirem)
docker stop $(docker ps -q --filter "ancestor=case_petlove_api") 2>/dev/null || true

# Executar o container
docker run --rm -p 8080:8000 --env-file .env case_petlove_api
```

---

###  Streamlit (Interface visual no com biblioteca python)
```bash
python -m uvicorn app.main:app --reload
```

> **Sobre o Streamlit:**  
>O Streamlit é uma biblioteca Python de código aberto que facilita a criação e o compartilhamento de aplicativos web personalizados para machine learning e ciência de dados.
>Ele permite construir interfaces visuais simples e rápidas para interagir com modelos de IA e dados em tempo real.
---

##  Executando os testes
```bash
python -m pytest -v
```

---

## Variáveis de ambiente (.env)

O arquivo `.env.example` serve como modelo do `.env`.  
Como as chaves reais são **sensíveis**, as credenciais estão hospedadas na AWS.  

Você pode acessar a rota diretamente via **cURL**:
```bash
curl -s -X POST \
  http://petlove-backend-dev.us-west-2.elasticbeanstalk.com/api/question-and-answer \
  -H 'Content-Type: application/json' \
  -d '{"message":"ração para gato siamês"}'
```

 *Exemplo de pergunta e resposta:*  
 <img width="1423" height="473" alt="image" src="https://github.com/user-attachments/assets/e3a794d2-005a-4150-888a-beb95178ba26" />

  

---

## Interface Streamlit

Também foi desenvolvida uma interface visual simples usando **Streamlit**, conectada ao backend.

A página está disponível em:  
👉 [http://petlove-assistente-dev.us-west-2.elasticbeanstalk.com/](http://petlove-assistente-dev.us-west-2.elasticbeanstalk.com/)

 *Imagem do chat:*  
 <img width="1844" height="920" alt="image" src="https://github.com/user-attachments/assets/45e6ddc1-7cb7-4c9a-b01d-e2b1ed23b2b5" />


---

## 🧩 Tecnologias Utilizadas

- 🐍 **Python**
- ⚙️ **FastAPI**
- 🧱 **Docker**
- 🌈 **Streamlit**
- 🧪 **Pytest**
- ☁️ **AWS Elastic Beanstalk**

---

## 💡 Sobre o Projeto

Este projeto demonstra a integração entre **modelo de linguagem natural**, **API escalável em FastAPI** e **frontend interativo com Streamlit** — ideal para aplicações que envolvem recomendação e suporte automatizado com IA.
