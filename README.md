# Comijest

Comijest is a web application available at [comijest.com.pl](https://comijest.com.pl), developed as a student project and as a foundation for a bachelor’s thesis. Its purpose is to support users in the preliminary analysis of symptoms and suggest possible diseases based on medical data and machine learning models.

The application is informational only. It does not provide a medical diagnosis, does not replace a doctor, and should not be used as the sole basis for making health-related decisions.

## Project Purpose

The goal of Comijest is to combine a modern web application with an artificial intelligence module that analyzes symptoms described by the user. The project demonstrates how to build a complete system consisting of a frontend, backend, database, user authentication, deployment infrastructure, and Machine Learning experiments.

The intended user flow is that a user provides information about their symptoms, and the system returns the most likely disease suggestions or possible next steps. The result should be treated only as supportive information that may help the user decide whether to consult a medical professional.

## How the Application Works

The user interacts with a web interface built with Next.js. The frontend is responsible for presenting the application, informational pages, registration, login, and the intended symptom input flow.

The backend is built with Flask and acts as the API layer. It handles user management, login, authorization, roles, and communication with the MongoDB database. User data is validated, and passwords are hashed before being stored.

The Machine Learning part is developed as a separate research module. It covers medical data preparation, generation of text-based symptom descriptions, and testing of models that classify diseases based on symptoms. The project tests both classic machine learning models and transformer-based models, including BioClinicalBERT.

Nginx acts as a reverse proxy, routing user traffic to the frontend and application requests to the backend.

## Main System Components

- frontend application for users,
- backend API handling application logic,
- MongoDB database storing user data,
- Redis used, among other things, for rate limiting,
- Machine Learning module for data preparation and model testing,
- Nginx as a reverse proxy,
- Docker Compose for service orchestration,
- GitHub Actions for testing, builds, and deployment.

## Tech Stack

### Frontend

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS 4
- TanStack React Query
- Formik
- Yup
- Framer Motion
- next-themes
- Lenis
- Lucide React
- ESLint

### Backend

- Python 3.10
- Flask 3
- Flask-CORS
- Flask-JWT-Extended
- Flask-Limiter
- Flask-PyMongo / PyMongo
- Marshmallow
- Werkzeug
- Gunicorn
- python-dotenv
- pytest
- pytest-cov
- mongomock

### Machine Learning

- pandas
- scikit-learn
- PyTorch
- Hugging Face Transformers
- Hugging Face Datasets
- joblib
- matplotlib
- Logistic Regression
- Linear SVM
- Multinomial Naive Bayes
- BioClinicalBERT
- PubMedBERT
- RoBERTa

### Infrastructure / DevOps

- Docker
- Docker Compose
- Nginx
- MongoDB
- Redis
- GitHub Actions
- VPS deployment
- Let's Encrypt

## Local Setup

The easiest way to run the whole project locally is with Docker Compose.

Requirements:

- Docker
- Docker Compose

```bash
docker compose up --build
```

After startup, the application should be available locally at:

```text
http://localhost
```

Main services started locally:

- Next.js frontend,
- Flask backend,
- MongoDB,
- Redis,
- Nginx.

Alternatively, the frontend and backend can be started separately.

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app.app run --debug
```

The backend requires environment variables such as the MongoDB connection string and JWT secret.

Example:

```env
MONGO_DB_CONNECTION_STRING=mongodb://localhost:27017/comijest
JWT_SECRET=your-secret
```

## Data and Preprocessing

The data used in the Machine Learning part is not stored directly in the repository. It is downloaded and processed locally using scripts included in the project.

The main source of text data is a public Hugging Face dataset:

[SymptomsDisease246k](https://huggingface.co/datasets/fhai50032/SymptomsDisease246k)

The dataset contains text-disease pairs, where a symptom description is associated with a diagnostic label. The data is then cleaned, split into training and test sets, and transformed into a format used by classification models.

The data preparation process includes:

1. Downloading the dataset from Hugging Face Datasets.
2. Selecting columns corresponding to symptom text and disease label.
3. Removing repeated prefixes and suffixes from the text.
4. Cleaning disease labels.
5. Splitting the data into training and test sets.
6. Moving any labels that would appear only in the test set back into the training set.
7. Saving the processed data locally.
8. Transforming symptom lists into fuller patient-like descriptions.

The patient sentence generator uses language templates. Additional details are added to symptom descriptions, such as duration, severity, time of day, impact on daily functioning, and closing statements. Variant selection is deterministic and based on a hash of the input text, so the same input always generates the same description.

For example, a symptom list may be transformed into a sentence such as:

`For the last a week, I've been dealing with cough, nasal congestion, diminished vision...`

This makes the training data closer to how a real user might describe their symptoms in the application.

## AI Model Testing

The project tested two approaches to disease classification based on symptoms:

- classic machine learning models,
- transformer-based models using BERT/RoBERTa architectures.

Experiment results, saved models, tokenizers, reports, and training logs are generated locally and are not stored in the repository.

### Classic Models

For classic models, text symptom descriptions were converted into TF-IDF representations using unigrams and bigrams, with a limit of 20,000 features.

Three classifiers were tested:

- Logistic Regression,
- Linear SVM,
- Multinomial Naive Bayes.

The models were trained on the training set and evaluated on the test set. The main comparison metric was accuracy. This stage allowed quick evaluation of how well classic approaches perform on disease classification from textual symptom descriptions.

### Transformer Models

The second approach involved training language models on natural symptom descriptions. This was done using Hugging Face Transformers.

The project includes support for testing:

- BioClinicalBERT,
- PubMedBERT,
- RoBERTa.

Special focus was placed on BioClinicalBERT because it is a BERT-based model adapted to biomedical and clinical texts. This makes it suitable for the project, as the data concerns symptoms, diseases, and health-related descriptions.

The transformer training process includes:

1. Loading training and test data.
2. Encoding disease names as numeric labels.
3. Tokenizing text with a sequence length limit.
4. Creating PyTorch-compatible datasets.
5. Training the model as a sequence classifier.
6. Running evaluation during training.
7. Saving training and evaluation logs.
8. Saving loss and metric plots.
9. Saving the trained model, tokenizer, and label encoder.

Metrics used for transformer evaluation:

- accuracy,
- F1 macro,
- F1 weighted.

## Security

The application uses JWT-based authentication and authorization. Users are assigned roles, and access to data is restricted based on permissions.

User passwords are not stored in plain text. They are hashed before being saved to the database. The backend also validates input data, including email address, username, and password strength.

The backend additionally uses rate limiting to reduce the risk of abuse by limiting login attempts.

## Testing and Code Quality

The backend includes unit and integration tests covering key parts of the system, including login, registration, user roles, authorization, user operations, and service logic.

The frontend includes ESLint configuration and a Next.js build process. The repository also includes GitHub Actions workflows supporting testing, building, and deployment.

## Authors

- Maksymilian Janica - Backend
- Adrian Kwaśnik - Frontend / DevOps
- Arkadiusz Lorek - AI / Machine Learning

## License

The project is licensed under the MIT License.
