FROM pytorch/pytorch
WORKDIR /workspace
ADD ./requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt
ADD . /workspace
RUN sudo chmod -R 777 /workspace
CMD [ "python" , "/workspace/app.py" ]
ENV HOME=/workspace
