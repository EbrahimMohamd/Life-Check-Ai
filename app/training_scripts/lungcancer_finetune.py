"""
LUNG CANCER FINE-TUNING SCRIPT (Phase 2)
=========================================
Unfreezes the top blocks of the frozen EfficientNetB0 backbone and retrains
with a very small learning rate so the model learns lung-specific features.

This significantly improves Grad-CAM heatmap localization accuracy.

Strategy:
  - Load pre-trained model (Phase 1 result)
  - Unfreeze last 50% of EfficientNetB0 (blocks 4, 5, 6, 7 + top conv)
  - Freeze all earlier layers to prevent catastrophic forgetting
  - Compile with lr=5e-6 (ultra-low to protect deeper weights)
  - Train with aggressive augmentation + EarlyStopping
"""

import tensorflow as tf
import numpy as np
import os

IMG_SIZE   = 224
BATCH_SIZE = 16   # smaller batch = more stable gradients during fine-tuning
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(BASE_DIR, "data", "lung cancer dataset")
MODEL_PATH = os.path.join(BASE_DIR, "models", "lung_model.h5")

print("=" * 60)
print("LUNG CANCER FINE-TUNING  — Phase 2")
print("=" * 60)

# ─────────────────────────────────────────
# 1. DATASET with Augmentation
# ─────────────────────────────────────────
print("\n[1/5] Loading dataset with augmentation pipeline...")

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

# Data augmentation (medical-safe — no extreme distortions)
augment = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.08),          # ±8 degrees
    tf.keras.layers.RandomZoom(0.1),
    tf.keras.layers.RandomContrast(0.15),
    tf.keras.layers.RandomBrightness(0.1),
], name="augmentation")

AUTOTUNE = tf.data.AUTOTUNE

train_ds = (train_ds
            .map(lambda x, y: (augment(x, training=True), y),
                 num_parallel_calls=AUTOTUNE)
            .cache()
            .shuffle(500)
            .prefetch(AUTOTUNE))

val_ds = val_ds.cache().prefetch(AUTOTUNE)

print("Dataset ready.")

# ─────────────────────────────────────────
# 2. LOAD EXISTING MODEL
# ─────────────────────────────────────────
print(f"\n[2/5] Loading Phase-1 model from: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)
model.summary()

# ─────────────────────────────────────────
# 3. UNFREEZE TOP LAYERS ONLY
# ─────────────────────────────────────────
print("\n[3/5] Unfreezing top EfficientNetB0 layers for fine-tuning...")

base_model = model.get_layer("efficientnetb0")
base_model.trainable = True   # Enable gradient flow

total_layers = len(base_model.layers)
# Freeze bottom 50% of layers, unfreeze top 50%
# This opens deeper layers (blocks 4 and 5) to learn specific medical patterns, maximizing Grad-CAM accuracy
FINE_TUNE_FROM = int(total_layers * 0.50)

for layer in base_model.layers[:FINE_TUNE_FROM]:
    layer.trainable = False

trainable_now = sum(1 for l in base_model.layers if l.trainable)
print(f"EfficientNetB0 total layers : {total_layers}")
print(f"Frozen layers               : {FINE_TUNE_FROM}")
print(f"Fine-tuning layers          : {total_layers - FINE_TUNE_FROM}")

# Total trainable params
total_trainable = sum(tf.size(w).numpy() for w in model.trainable_weights)
print(f"Total trainable parameters  : {total_trainable:,}")

# ─────────────────────────────────────────
# 4. RECOMPILE WITH LOW LR
# ─────────────────────────────────────────
print("\n[4/5] Recompiling with fine-tuning learning rate (1e-5)...")

model.compile(
    # Ultra-low lr is CRITICAL: prevents destroying pretrained weights since we unfreezed 50%
    optimizer=tf.keras.optimizers.Adam(learning_rate=5e-6),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),
    tf.keras.callbacks.ModelCheckpoint(
        MODEL_PATH,
        save_best_only=True,
        monitor="val_accuracy",
        verbose=1
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.3,
        patience=3,
        min_lr=1e-7,
        verbose=1
    ),
]

# ─────────────────────────────────────────
# 5. FINE-TUNE
# ─────────────────────────────────────────
print("\n[5/5] Starting fine-tuning...")
print("(EarlyStopping is active — will stop when val_accuracy stops improving)\n")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=20,
    callbacks=callbacks
)

best_val_acc = max(history.history["val_accuracy"])
print(f"\nFine-tuning complete!")
print(f"Best Validation Accuracy: {best_val_acc*100:.2f}%")
print(f"Model saved to: {MODEL_PATH}")
print("\nGrad-CAM heatmaps will now reflect learned lung-specific features.")
