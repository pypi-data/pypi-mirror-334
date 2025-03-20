import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.base import BaseEstimator

# Definir argumentos padrão para o modelo
DEFAULT_ARGS = {
    'dim_h': 64,      # Dimensão da camada oculta
    'n_z': 10,        # Dimensão do espaço latente
    'lr': 0.0002,     # Taxa de aprendizado
    'epochs': 100,    # Número de épocas de treinamento
    'batch_size': 64  # Tamanho do batch
}

# Verificar dispositivo (CPU ou GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Modelos GAN
class Encoder(nn.Module):
    def __init__(self, args, num_input_features):
        super(Encoder, self).__init__()
        self.fc1 = nn.Linear(num_input_features, args['dim_h'])
        self.fc2 = nn.Linear(args['dim_h'], args['dim_h'])
        self.fc_mean = nn.Linear(args['dim_h'], args['n_z'])
        self.fc_logvar = nn.Linear(args['dim_h'], args['n_z'])
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc_mean(x), self.fc_logvar(x)

class Decoder(nn.Module):
    def __init__(self, args, num_input_features):
        super(Decoder, self).__init__()
        self.fc1 = nn.Linear(args['n_z'], args['dim_h'])
        self.fc2 = nn.Linear(args['dim_h'], args['dim_h'])
        self.fc_output = nn.Linear(args['dim_h'], num_input_features)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc_output(x)

class Discriminator(nn.Module):
    def __init__(self, num_input_features):
        super(Discriminator, self).__init__()
        self.fc1 = nn.Linear(num_input_features, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 1)
        self.relu = nn.ReLU(inplace=True)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.sigmoid(self.fc3(x))

# Função para calcular o número de amostras a serem geradas
def calculate_n_to_sample(y):
    class_counts = np.bincount(y)
    major_class_count = np.max(class_counts)
    n_classes = len(class_counts)
    n_to_sample_dict = {cl: major_class_count - class_counts[cl] for cl in range(n_classes)}
    return n_to_sample_dict, major_class_count

# Função para gerar amostras sintéticas
def G_SM1(X, y, n_to_sample, cl, encoder, decoder, args):
    X_tensor = torch.tensor(X, dtype=torch.float32).to(device)
    y_tensor = torch.tensor(y, dtype=torch.long).to(device)
    dataloader = DataLoader(TensorDataset(X_tensor, y_tensor), batch_size=args['batch_size'], shuffle=True)

    synthetic_data = []
    for _ in range(n_to_sample):
        z = torch.randn(1, args['n_z']).to(device)
        synthetic_sample = decoder(z).detach().cpu().numpy()
        synthetic_data.append(synthetic_sample)

    synthetic_data = np.vstack(synthetic_data)
    synthetic_labels = np.array([cl] * n_to_sample)
    return synthetic_data, synthetic_labels

# Função para treinar o GAN
def train_gan(encoder, decoder, discriminator, X_train, args):
    optimizer_g = torch.optim.Adam(list(encoder.parameters()) + list(decoder.parameters()), lr=args['lr'])
    optimizer_d = torch.optim.Adam(discriminator.parameters(), lr=args['lr'])
    criterion_g = nn.MSELoss()
    criterion_d = nn.BCELoss()

    dataloader = DataLoader(torch.tensor(X_train, dtype=torch.float32), batch_size=args['batch_size'], shuffle=True)

    for epoch in range(args['epochs']):
        for batch in dataloader:
            # Configurar dados
            batch = batch.to(device)
            real_labels = torch.ones(batch.size(0), 1).to(device)
            fake_labels = torch.zeros(batch.size(0), 1).to(device)

            # Treinar discriminador
            optimizer_d.zero_grad()
            outputs_real = discriminator(batch)
            d_loss_real = criterion_d(outputs_real, real_labels)

            z = torch.randn(batch.size(0), args['n_z']).to(device)
            fake_data = decoder(z)
            outputs_fake = discriminator(fake_data.detach())
            d_loss_fake = criterion_d(outputs_fake, fake_labels)

            d_loss = d_loss_real + d_loss_fake
            d_loss.backward()
            optimizer_d.step()

            # Treinar gerador
            optimizer_g.zero_grad()
            outputs = discriminator(fake_data)
            g_loss = criterion_g(fake_data, batch) + criterion_d(outputs, real_labels)
            g_loss.backward()
            optimizer_g.step()

    return encoder, decoder, discriminator

# Classe principal DSTO_GAN
class DSTO_GAN(BaseEstimator):
    def __init__(self, dim_h=64, n_z=10, lr=0.0002, epochs=100, batch_size=64, random_state=None):
        self.dim_h = dim_h
        self.n_z = n_z
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
        self.random_state = random_state
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.encoder = None
        self.decoder = None
        self.discriminator = None

    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        
        # Inicializar modelos GAN
        num_features = X.shape[1]
        self.encoder = Encoder({'dim_h': self.dim_h, 'n_z': self.n_z}, num_features).to(self.device)
        self.decoder = Decoder({'dim_h': self.dim_h, 'n_z': self.n_z}, num_features).to(self.device)
        self.discriminator = Discriminator(num_features).to(self.device)
        
        # Treinar GAN
        self.encoder, self.decoder, _ = train_gan(self.encoder, self.decoder, self.discriminator, X, {
            'dim_h': self.dim_h,
            'n_z': self.n_z,
            'lr': self.lr,
            'epochs': self.epochs,
            'batch_size': self.batch_size
        })
        
        return self

    def fit_resample(self, X, y):
        self.fit(X, y)
        
        # Calcular o número de amostras a serem geradas
        n_to_sample_dict, _ = calculate_n_to_sample(y)
        synthetic_data, synthetic_labels = [], []

        for cl, n_samples in n_to_sample_dict.items():
            if n_samples > 0:
                X_synthetic, y_synthetic = G_SM1(X, y, n_samples, cl, self.encoder, self.decoder, {
                    'dim_h': self.dim_h,
                    'n_z': self.n_z,
                    'batch_size': self.batch_size
                })
                synthetic_data.append(X_synthetic)
                synthetic_labels.append(y_synthetic)

        if synthetic_data:
            X_resampled = np.vstack([X, np.vstack(synthetic_data)])
            y_resampled = np.hstack([y, np.hstack(synthetic_labels)])
        else:
            X_resampled = X
            y_resampled = y

        return X_resampled, y_resampled