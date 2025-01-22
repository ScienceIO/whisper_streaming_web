FROM python:3.10

RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV CONDA_DIR /opt/conda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda

ENV PATH $CONDA_DIR/bin:$PATH

ARG hf_token

#RUN addgroup --system appuser && adduser --system --group appuser

WORKDIR /all
COPY . .
RUN conda env create -f environment.yml
RUN echo "source activate ambient-audio" > ~/.bashrc
ENV PATH /opt/conda/envs/ambient-audio/bin:$PATH
RUN /bin/bash -c "source activate ambient-audio && conda list"

RUN pip install --no-cache-dir -r requirements.txt

ENV HF_TOKEN $hf_token

RUN touch /all/output1.log 
#RUN chown appuser:appuser /all/output1.log
RUN huggingface-cli login --token $HF_TOKEN

EXPOSE 8000

#USER appuser

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
