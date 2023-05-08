FROM pytorch/pytorch
WORKDIR /workspace
ADD ./requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt
ADD . /workspace
RUN chmod -R 777 /workspace
VOLUME /workspace/models_train
CMD [ "python" , "/workspace/app.py" ]
ENV HOME=/workspace
