"""
Model management for XSS detection.
"""

import os
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import kagglehub

# Configuration
MAX_SEQUENCE_LENGTH = 1000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.2
BATCH_SIZE = 32
EPOCHS = 5

def get_data_directory():
    """Get the directory where model data should be stored."""
    home_dir = os.path.expanduser("~")
    data_dir = os.path.join(home_dir, '.xss_detector')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def download_and_prepare_dataset():
    """Download the XSS dataset from Kaggle and prepare it for training."""
    print("Downloading dataset from Kaggle...")
    try:
        dataset_path = kagglehub.dataset_download("syedsaqlainhussain/cross-site-scripting-xss-dataset-for-deep-learning")
    except Exception as e:
        raise Exception(f"Failed to download dataset: {e}. Please ensure you have kagglehub installed and configured.")
    
    # Look for CSV file in the dataset path
    csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {dataset_path}")
        
    # Use the first CSV file found
    csv_path = os.path.join(dataset_path, csv_files[0])
    print(f"Using dataset file: {csv_path}")
    
    # Load the dataset
    df = pd.read_csv(csv_path)
    
    return df

def train_model(dataset=None):
    """
    Train an XSS detection model.
    
    Args:
        dataset: Optional pandas DataFrame. If not provided, will download from Kaggle.
        
    Returns:
        tuple: (model, tokenizer, max_sequence_length)
    """
    data_dir = get_data_directory()
    model_path = os.path.join(data_dir, 'xss_detection_model.h5')
    tokenizer_path = os.path.join(data_dir, 'tokenizer.pickle')
    
    if dataset is None:
        df = download_and_prepare_dataset()
    else:
        df = dataset
    
    # Preprocess
    texts = df['Sentence'].values
    labels = df['Label'].values
    
    # Tokenize the text
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    
    # Pad sequences
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=VALIDATION_SPLIT, random_state=42)
    
    # Build the model
    model = Sequential([
        Embedding(len(tokenizer.word_index) + 1, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH),
        Conv1D(128, 5, activation='relu'),
        GlobalMaxPooling1D(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    
    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    # Train the model
    model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(X_test, y_test))
    
    # Save the model and tokenizer
    model.save(model_path)
    with open(tokenizer_path, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    # Print model evaluation
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    print(classification_report(y_test, y_pred))
    
    return model, tokenizer, MAX_SEQUENCE_LENGTH

def load_xss_model():
    """
    Load the XSS detection model. If model does not exist, train it.
    
    Returns:
        tuple: (model, tokenizer, max_sequence_length)
    """
    data_dir = get_data_directory()
    model_path = os.path.join(data_dir, 'xss_detection_model.h5')
    tokenizer_path = os.path.join(data_dir, 'tokenizer.pickle')
    
    if os.path.exists(model_path) and os.path.exists(tokenizer_path):
        print("Loading existing model...")
        model = load_model(model_path)
        with open(tokenizer_path, 'rb') as handle:
            tokenizer = pickle.load(handle)
        return model, tokenizer, MAX_SEQUENCE_LENGTH
    else:
        print("No existing model found. Training new model...")
        return train_model()