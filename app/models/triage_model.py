import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

MODEL_PATH = 'model.pkl'
ENCODERS_PATH = 'encoders.pkl'

VARIABLES = [
    'dificultadRespirar', 'dolorPecho', 'perdidaConciencia', 
    'sangradoNasal', 'fiebreAlta', 'dolorAbdominal',
    'nauseasVomitos', 'dolorCabeza', 'mareos', 'tosPersistente',
    'embarazo', 'presionAlta', 'diabetes', 'hipertension',
    'dislipidemia', 'obesidad', 'cancer', 'cirugiaReciente'
]

URGENCY_LEVELS = {
    1: {"color": "Rojo", "atencion": "Inmediata", "tiempo": "0 min"},
    2: {"color": "Naranja", "atencion": "Muy urgente", "tiempo": "≤10 min"},
    3: {"color": "Amarillo", "atencion": "Urgente", "tiempo": "≤60 min"},
    4: {"color": "Verde", "atencion": "Poco urgente", "tiempo": "≤120 min"},
    5: {"color": "Azul", "atencion": "No urgente", "tiempo": "≤240 min"}
}

class TriageModel:
    def __init__(self):
        self.model = None
        self.encoders = None
        self.variables = VARIABLES
        self.load_or_train()

    def load_or_train(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(ENCODERS_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.encoders = joblib.load(ENCODERS_PATH)
        else:
            self.train_model()

    def train_model(self):
        np.random.seed(42)
        data = {var: np.random.choice(['Si', 'No'], 3000, p=[0.25, 0.75]) for var in VARIABLES}
        conditions = [
            (data['perdidaConciencia'] == 'Si') | 
            ((data['dificultadRespirar'] == 'Si') & (data['dolorPecho'] == 'Si')),
            (data['dificultadRespirar'] == 'Si') | 
            (data['dolorPecho'] == 'Si') | 
            (data['sangradoNasal'] == 'Si'),
            (data['fiebreAlta'] == 'Si') | 
            (data['dolorAbdominal'] == 'Si') | 
            (data['dolorCabeza'] == 'Si'),
            (data['mareos'] == 'Si') | 
            (data['tosPersistente'] == 'Si') | 
            (data['nauseasVomitos'] == 'Si')
        ]

        df = pd.DataFrame(data)
        df['nivel'] = np.select(conditions, [1, 2, 3, 4], default=5)

        self.encoders = {var: LabelEncoder().fit(['Si', 'No']) for var in VARIABLES}
        for var in VARIABLES:
            df[var] = self.encoders[var].transform(df[var])

        self.model = RandomForestClassifier(n_estimators=200, max_depth=10, class_weight='balanced')
        self.model.fit(df[VARIABLES], df['nivel'])

        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.encoders, ENCODERS_PATH)

    def predict(self, patient_data):
        encoded_data = [self.encoders[var].transform([patient_data[var]])[0] for var in self.variables]
        return int(self.model.predict([encoded_data])[0])

triage = TriageModel()