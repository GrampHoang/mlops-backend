FROM pytorch/pytorch
WORKDIR /workspace
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx -y
ADD ./requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt
ADD . /workspace
RUN chmod -R 777 /workspace
VOLUME /workspace/models_train
CMD [ "python" , "/workspace/app.py" ]
ENV HOME=/workspace
