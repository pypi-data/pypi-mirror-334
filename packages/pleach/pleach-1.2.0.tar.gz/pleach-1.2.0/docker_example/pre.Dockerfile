FROM gaaviai/pleach:1.0-alpha

CMD ["python", "-m", "pleach", "run", "--host", "0.0.0.0", "--port", "7860"]
