from sqlalchemy import Column, Integer, String, DECIMAL, Time, Date, DateTime, Boolean, LargeBinary, ForeignKey
from database.database import Base


class Farmacia(Base):
    __tablename__ = "farmacias"

    id_farmacia = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=False)
    endereco = Column(String(255), nullable=False)
    telefone = Column(String(20))
    email = Column(String(100))
    horario_abertura = Column(Time)
    horario_fechamento = Column(Time)


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    telefone = Column(String(20))
    email = Column(String(100), unique=True, nullable=False)
    endereco = Column(String(255))


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id_medicamento = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    principio_ativo = Column(String(255))
    dosagem = Column(String(50))
    laboratorio = Column(String(255))
    preco = Column(DECIMAL(10, 2), nullable=False)
    controlado = Column(Boolean, default=False)


class Estoque(Base):
    __tablename__ = "estoque"

    id_estoque = Column(Integer, primary_key=True, autoincrement=True)
    id_farmacia = Column(Integer, ForeignKey("farmacias.id_farmacia"), nullable=False)
    id_medicamento = Column(Integer, ForeignKey("medicamentos.id_medicamento"), nullable=False)
    estoque = Column(Integer, nullable=False)
    data_entrada = Column(DateTime)
    data_validade = Column(Date)
    lote = Column(Integer)
    quantidade_minima = Column(Integer)


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    id_farmacia = Column(Integer, ForeignKey("farmacias.id_farmacia"), nullable=False)
    data_hora_pedido = Column(DateTime)
    status_pedido = Column(String(50), nullable=False)
    valor_total = Column(DECIMAL(10, 2), nullable=False)
    endereco_entrega = Column(String(255), nullable=False)


class PedidoMedicamento(Base):
    __tablename__ = "pedido_medicamento"

    id_pedido_medicamento = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"), nullable=False)
    id_medicamento = Column(Integer, ForeignKey("medicamentos.id_medicamento"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(DECIMAL(10, 2), nullable=False)


class Entrega(Base):
    __tablename__ = "entrega"

    entrega_id = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"), nullable=False)
    id_entregador = Column(Integer, ForeignKey("entregadores.id_entregador"), nullable=False)
    status_entrega = Column(String(45), nullable=False)
    data_saida = Column(DateTime)
    data_chegada = Column(DateTime)
    assinatura_recebedor = Column(LargeBinary)


class Entregador(Base):
    __tablename__ = "entregadores"

    id_entregador = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    veiculo = Column(String(50))
    placa_veiculo = Column(String(10))