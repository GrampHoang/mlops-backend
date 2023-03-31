FROM pytorch/pytorch
WORKDIR /workspace
ADD ./requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt
ADD . /workspace
CMD [ "python" , "/workspace/app.py" ]
RUN chown -R 42420:42420 /workspace
ENV HOME=/workspace