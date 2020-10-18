FROM python:3.8.5-alpine
WORKDIR /relayr_coding_test_aidan_butler
ADD . /relayr_coding_test_aidan_butler
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTONPATH}:/relayr_coding_test_aidan_butler"
CMD ["python","product_comparison_service/app.py"]