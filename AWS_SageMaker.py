import sagemaker
from sagemaker.huggingface import HuggingFaceModel

# Sessão do SageMaker
sess = sagemaker.Session()

# IAM Role que o SageMaker vai usar
role = "arn:aws:iam::986906626275:role/SageMakerExecutionRole"

# Modelo no S3
model_path = "s3://llm-adni-2025-valdir/model_export/model.tar.gz"

# Definir o container HuggingFace
hub = {
  'HF_MODEL_ID':'',  # deixamos vazio porque vamos usar seu modelo do S3
  'HF_TASK':'text2text-generation'
}

huggingface_model = HuggingFaceModel(
   env=hub,
   model_data=model_path,  # modelo que você enviou
   role=role,
   transformers_version="4.37",
   pytorch_version="2.1",
   py_version="py310",
)

# Deployar em uma instância (ml.m5.large é barata p/ começar)
predictor = huggingface_model.deploy(
   initial_instance_count=1,
   instance_type="ml.t2.medium"
)
