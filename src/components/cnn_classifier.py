import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_data(images_path, labels_path):
    images = np.load(images_path)
    labels = np.load(labels_path)
    return images, labels

def preprocess_data(images, labels):
    # Normalize pixel values to be between 0 and 1
    images = images.astype('float32') / 255.0
    
    # Reshape images to include channel dimension
    images = images.reshape(images.shape[0], images.shape[1], images.shape[2], 1)
    
    # Encode labels
    le = LabelEncoder()
    labels_encoded = le.fit_transform(labels)
    
    # Convert to categorical
    labels_categorical = tf.keras.utils.to_categorical(labels_encoded)
    
    return images, labels_categorical, le

def create_model(input_shape, num_classes):
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (4, 4), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (5, 5), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model



def main():
    # Load data
    images_path = '/Users/ginger/Developer/python/Projects/sar-colorization/Data/images_full.npy'
    labels_path = '/Users/ginger/Developer/python/Projects/sar-colorization/Data/labels_full.npy'
    images, labels = load_data(images_path, labels_path)

    # Preprocess data
    images, labels, le = preprocess_data(images, labels)

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

    # Create and compile the model
    input_shape = X_train.shape[1:]
    num_classes = len(le.classes_)
    model = create_model(input_shape, num_classes)
    
    # Train the model
    history = model.fit(X_train, y_train, epochs=10, validation_split=0.2, batch_size=32)
    
    # Evaluate the model
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
    print(f'\nTest accuracy: {test_acc}')
    
    # Print classification report
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    
    from sklearn.metrics import classification_report, confusion_matrix
    print('\nClassification Report:')
    print(classification_report(y_true_classes, y_pred_classes, target_names=le.classes_))
    cm = confusion_matrix(y_true_classes, y_pred_classes, target_names=le.classes_)
    print()

    

if __name__ == "__main__":
    main()