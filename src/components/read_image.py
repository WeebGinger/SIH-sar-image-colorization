import os
import cv2
import numpy as np

def process_images(base_path, images_per_category=500):
    categories = ['agri', 'barrenland', 'grassland', 'urban']
    images = []
    labels = []

    for category in categories:
        category_path = os.path.join(base_path, category, 's2')
        if not os.path.exists(category_path):
            print(f"Warning: Path {category_path} does not exist. Skipping.")
            continue

        image_files = [f for f in os.listdir(category_path) if f.lower().endswith(('.png'))]
        
        # Take the first 500 images
        selected_files = image_files[:images_per_category]
        
        for filename in selected_files:
            img_path = os.path.join(category_path, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            
            if img is not None:
                images.append(img)
                labels.append(category)
            else:
                print(f"Warning: Could not read image {img_path}")

        print(f"Processed {len(selected_files)} images from {category}")

    return np.array(images), np.array(labels)

def save_arrays(images, labels, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    np.save(os.path.join(save_path, 'images_full.npy'), images)
    np.save(os.path.join(save_path, 'labels_full.npy'), labels)
    print(f"Arrays saved in {save_path}")

def main():
    base_path = '/Users/ginger/Developer/python/Projects/sar-colorization/Data/v_2'  # Replace with the actual path
    save_path = '/Users/ginger/Developer/python/Projects/sar-colorization/Data'  # Replace with the path where you want to save the arrays
    images_per_category = 4000  # Set the number of images to select from each category
    
    images, labels = process_images(base_path, images_per_category)

    print(f"Total images processed: {len(images)}")
    print(f"Shape of the image array: {images.shape}")
    print(f"Shape of the labels array: {labels.shape}")
    print(f"Unique labels: {np.unique(labels)}")
    print(f"Number of images per category:")
    for category in np.unique(labels):
        print(f"  {category}: {np.sum(labels == category)}")

    # Save the arrays
    save_arrays(images, labels, save_path)

if __name__ == "__main__":
    main()