FROM jupyter/scipy-notebook

RUN echo $HOME

RUN mkdir -p /home/jovyan/us-inflation-hedge-strategies
ADD . /home/jovyan/us-inflation-hedge-strategies

# create a new user
RUN useradd -ms /bin/bash us-inflation-hedge-strategies
USER us-inflation-hedge-strategies

# set the working directory
WORKDIR /home/jovyan/us-inflation-hedge-strategies

# change the directory owner
RUN chown -R us-inflation-hedge-strategies /home/jovyan/us-inflation-hedge-strategies

RUN pip3 install -r requirements.txt

EXPOSE 8888                                           
ENTRYPOINT ["jupyter", "notebook","--allow-root","--ip=0.0.0.0","--port=8888","--no-browser"]