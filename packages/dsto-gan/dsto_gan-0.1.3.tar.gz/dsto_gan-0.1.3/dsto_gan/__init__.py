# __init__.py

# Importações dos módulos internos
from .dsto_gan import (  # Certifique-se de que o arquivo dsto_gan.py existe no mesmo diretório
    Encoder,
    Decoder,
    Discriminator,
    G_SM1,
    calculate_n_to_sample,
    train_gan,
    process_data,
)

# Defina a versão do pacote
__version__ = "1.0.0"

# Descrição do pacote
__description__ = "Pacote para geração de datasets balanceados usando GAN."

# Autor do pacote
__author__ = "Erika Gonçalves de Assis"

# Lista de funções/classes públicas que serão expostas ao usar `from pacote import *`
__all__ = [
    'Encoder',
    'Decoder',
    'Discriminator',
    'G_SM1',
    'calculate_n_to_sample',
    'train_gan',
    'process_data',
]

# Mensagem de inicialização (opcional, mas não recomendada para pacotes publicados)
# print(f"Pacote {__name__} versão {__version__} carregado com sucesso.")