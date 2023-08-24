import gradio as gr
from huggingface_hub import from_pretrained_keras
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing import image
import numpy as np

model = from_pretrained_keras("yusyel/clothing")

class_names=["dress",
        "hat",
        "longsleee",
        "outwear",
        "pants",
        "shirt",
        "shoes",
        "shorts",
        "skirt",
        "t-shirt"]



def preprocess_image(img):
    img = load_img(img, target_size=(299, 299, 3))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.0
    print(img.shape)
    return img



def predict(img):
    img = preprocess_image(img)
    pred = model.predict(img)
    pred = np.squeeze(np.exp(pred)/np.sum(np.exp(pred))).astype(float)
    print(dict(zip(class_names, pred)))
    return dict(zip(class_names, pred))

demo= gr.Interface(
    fn=predict,
    inputs=[gr.inputs.Image(type="filepath")],
    outputs=gr.outputs.Label(),
    examples=[
        ["./img/dress.jpg"],
        ["./img/hat.jpg"],
        ["./img/longsleeve.jpg"],
        ["./img/outwear.jpg"],
        ["./img/pants.jpg"],
        ["./img/shirt.jpg"],
        ["./img/shoes.jpg"],
        ["./img/short.jpg"],
        ["./img/skirt.jpg"],
        ["./img/t-shirt.jpg"],
    ],
    title="Fashion Classification")

demo.launch(server_name="0.0.0.0", server_port=7860)
