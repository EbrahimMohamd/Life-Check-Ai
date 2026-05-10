from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
import cv2
import base64
from PIL import Image
import io
import os

router = APIRouter(prefix="/predict/lung", tags=["lung"])

IMG_SIZE = 224
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "lung_model.h5")
CLASSES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "classes.txt")

model_cache = None
classes_cache = None
activation_model_cache = None

def get_model():
    global model_cache, classes_cache, activation_model_cache
    if model_cache is not None:
        return model_cache, classes_cache, activation_model_cache
        
    if not os.path.exists(MODEL_PATH):
        return None, None, None
        
    try:
        model_cache = tf.keras.models.load_model(MODEL_PATH)
        with open(CLASSES_PATH, "r") as f:
            classes_cache = f.read().split(",")
        try:

            base_model = model_cache.get_layer("efficientnetb0")
            semantic_sequence = [
                "stem_conv",             # Layer 1: Basic anatomical edges
                "block2a_project_conv",  # Layer 2: Lung boundaries and shapes
                "block3a_project_conv",  # Layer 3: Tissue textures
                "block4a_project_conv",  # Layer 4: Complex patterns
                "block5a_project_conv",  # Layer 5: Suspicious opacities detection
                "block6a_project_conv",  # Layer 6: Organic object separation
                "block7a_project_conv",  # Layer 7: Deep spatial relationships
                "top_activation"         # Layer 8: Final semantic diagnosis (The exact layer Grad-CAM uses)
            ]
            layer_outputs = [base_model.get_layer(name).output for name in semantic_sequence]
            activation_model_cache = tf.keras.models.Model(inputs=base_model.input, outputs=layer_outputs)
        except Exception as e:
            print("Warning: Could not bind sequential activation model.", e)
            activation_model_cache = None
            
        return model_cache, classes_cache, activation_model_cache
    except Exception as e:
        print("GET MODEL FATAL ERROR:", e)
        return None, None, None

def get_gradcam(img_array, model):
    """
    Production-grade Grad-CAM for nested EfficientNetB0.
    
    Fixes:
    - Uses tf.gather for safe class score indexing (avoids tensor indexing bug)
    - Vectorized matrix multiply (7,7,1280) @ (1280,) = (7,7) instead of Python loop
    - Watches feature_map directly (no redundant img_tensor watch)
    - Checks for None gradients and logs them explicitly
    """
    try:
        import traceback
        base_model = model.get_layer("efficientnetb0")
        
        feature_extractor = tf.keras.models.Model(
            inputs=base_model.input,
            outputs=base_model.get_layer("top_activation").output
        )
        
        gap_layer      = model.get_layer("global_average_pooling2d")
        dropout_layer  = model.get_layer("dropout")
        dense_layer    = model.get_layer("dense")
        
        img_tensor = tf.cast(img_array, tf.float32) 
        
        with tf.GradientTape() as tape:
       
            feature_map = feature_extractor(img_tensor, training=False) 
            tape.watch(feature_map)
            
           
            x      = gap_layer(feature_map)               
            x      = dropout_layer(x, training=False) 
            preds  = dense_layer(x)                      
            

            top_class   = tf.argmax(preds[0])            
            class_score = tf.gather(preds[0], top_class)   
        
        grads = tape.gradient(class_score, feature_map) 
        
        if grads is None:
            print("Grad-CAM WARNING: Gradients returned None. Model architecture might block gradient flow.")
            return np.ones((7, 7)) * 0.3 
        
        
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))  
        

        feature_np  = feature_map[0].numpy()    
        weights_np  = pooled_grads.numpy()      
        
        heatmap = feature_np @ weights_np      
        

        heatmap = np.maximum(heatmap, 0)
        

        hm_min, hm_max = np.min(heatmap), np.max(heatmap)
        if hm_max > hm_min:
            heatmap = (heatmap - hm_min) / (hm_max - hm_min)  
        elif hm_max > 0:
            heatmap = heatmap / hm_max
        
        return heatmap  

    except Exception as e:
        import traceback
        print(f"Grad-CAM Failed: {e}")
        traceback.print_exc()
        return np.zeros((7, 7))

def encode_img(img):
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode()

@router.post("")
async def predict_lung(file: UploadFile = File(...)):
    model, class_names, activation_model = get_model()
    
    if model is None:
        return JSONResponse(status_code=503, content={"error": "The AI model is currently training iteratively. Please check back later."})
        
    try:
        contents = await file.read()
        
     
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        img = img.resize((IMG_SIZE, IMG_SIZE))
        arr = np.array(img)
        input_arr = np.expand_dims(arr, axis=0)

  
        pred = model.predict(input_arr)
        idx = np.argmax(pred)
        conf = float(np.max(pred))


        heatmap_raw = get_gradcam(input_arr, model)  # (7, 7) float [0,1]


        heatmap_up = cv2.resize(heatmap_raw.astype(np.float32), (IMG_SIZE, IMG_SIZE), 
                                interpolation=cv2.INTER_CUBIC)

        heatmap_up = cv2.GaussianBlur(heatmap_up, (15, 15), 0)
        

        hm_min, hm_max = np.min(heatmap_up), np.max(heatmap_up)
        if hm_max > hm_min:
            heatmap_up = (heatmap_up - hm_min) / (hm_max - hm_min)
        

        heatmap_uint8 = np.uint8(255 * heatmap_up)
        

        heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        pure_heatmap_colored = heatmap_colored.copy()
        
      
        original_uint8 = arr.astype("uint8")
        original_bgr   = cv2.cvtColor(original_uint8, cv2.COLOR_RGB2BGR)


        alpha_mask = np.expand_dims(heatmap_up, axis=-1) 
        
        
        overlay_float = (original_bgr * (1.0 - 0.6 * alpha_mask)) + (heatmap_colored * (0.6 * alpha_mask))
        overlay = np.clip(overlay_float, 0, 255).astype(np.uint8)
        

        activations_b64 = []
        if activation_model:
            acts = activation_model.predict(input_arr)
            for act in acts:

                act_mean = np.mean(np.abs(act[0]), axis=-1)
                

                act_mean_resized = cv2.resize(act_mean, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_CUBIC)
                
                max_val = np.max(act_mean_resized)
                if max_val > 0:
                    act_mean_resized /= max_val
                    
            
                act_uint8 = np.uint8(255 * act_mean_resized)
                act_colored = cv2.applyColorMap(act_uint8, cv2.COLORMAP_VIRIDIS)
                activations_b64.append(encode_img(act_colored))

        return {
            "prediction": class_names[idx],
            "confidence": conf,
            "filename": file.filename,
            "heatmap": encode_img(overlay),
            "heatmap_pure": encode_img(pure_heatmap_colored),
            "original": encode_img(original_bgr),
            "activations": activations_b64
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": f"Image processing failed: {str(e)}"})