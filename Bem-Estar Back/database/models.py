from sqlalchemy import Column, Integer, String, DECIMAL, Time, Date, DateTime, Boolean, LargeBinary, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime



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

    estoques = relationship("Estoque", back_populates="farmacia")
    pedidos = relationship("Pedido", back_populates="farmacia")


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)

    nome = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    telefone = Column(String(20))
    email = Column(String(100), unique=True, nullable=False)
    endereco = Column(String(255))
    pedidos = relationship("Pedido", back_populates="cliente")


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id_medicamento = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    principio_ativo = Column(String(255))
    dosagem = Column(String(50))
    laboratorio = Column(String(255))
    preco = Column(DECIMAL(10, 2), nullable=False)
    controlado = Column(Boolean, default=False)
    estoques = relationship("Estoque", back_populates="medicamento")
    pedidos_medicamentos = relationship(
        "PedidoMedicamento",
        back_populates="medicamento"
    )


class Estoque(Base):
    __tablename__ = "estoque"

    id_estoque = Column(Integer, primary_key=True, autoincrement=True)
    id_farmacia = Column(
        Integer,
        ForeignKey("farmacias.id_farmacia"),
        nullable=False
    )
    id_medicamento = Column(
        Integer,
        ForeignKey("medicamentos.id_medicamento"),
        nullable=False
    )
    estoque = Column(Integer, nullable=False)
    data_entrada = Column(DateTime)
    data_validade = Column(Date)
    lote = Column(Integer)
    quantidade_minima = Column(Integer)

    farmacia = relationship("Farmacia", back_populates="estoques")
    medicamento = relationship("Medicamento", back_populates="estoques")


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(
        Integer,
        ForeignKey("clientes.id_cliente"),
        nullable=False
    )

    id_farmacia = Column(
        Integer,
        ForeignKey("farmacias.id_farmacia"),
        nullable=False
    )

    data_hora_pedido = Column(
        DateTime,
        default=datetime.utcnow
    )

    status_pedido = Column(
        String(50),
        nullable=False
    )

    valor_total = Column(
        DECIMAL(10, 2),
        nullable=False
    )

    endereco_entrega = Column(
        String(255),
        nullable=False
    )

    cliente = relationship("Cliente", back_populates="pedidos")
    farmacia = relationship("Farmacia", back_populates="pedidos")

    itens = relationship(
        "PedidoMedicamento",
        back_populates="pedido"
    )

    entrega = relationship(
        "Entrega",
        back_populates="pedido"
    )


class PedidoMedicamento(Base):
    __tablename__ = "pedido_medicamento"

    id_pedido_medicamento = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_pedido = Column(
        Integer,
        ForeignKey("pedidos.id_pedido"),
        nullable=False
    )

    id_medicamento = Column(
        Integer,
        ForeignKey("medicamentos.id_medicamento"),
        nullable=False
    )

    quantidade = Column(
        Integer,
        nullable=False
    )

    preco_unitario = Column(
        DECIMAL(10, 2),
        nullable=False
    )

    pedido = relationship(
        "Pedido",
        back_populates="itens"
    )

    medicamento = relationship(
        "Medicamento",
        back_populates="pedidos_medicamentos"
    )


class Entrega(Base):
    __tablename__ = "entrega"

    entrega_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_pedido = Column(
        Integer,
        ForeignKey("pedidos.id_pedido"),
        nullable=False
    )

    id_entregador = Column(
        Integer,
        ForeignKey("entregadores.id_entregador"),
        nullable=False
    )

    status_entrega = Column(
        String(45),
        nullable=False
    )

    data_saida = Column(DateTime)
    data_chegada = Column(DateTime)
    assinatura_recebedor = Column(LargeBinary)

    pedido = relationship(
        "Pedido",
        back_populates="entrega"
    )

    entregador = relationship(
        "Entregador",
        back_populates="entregas"
    )


class Entregador(Base):
    __tablename__ = "entregadores"

    id_entregador = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nome = Column(
        String(255),
        nullable=False
    )

    cpf = Column(
        String(14),
        unique=True,
        nullable=False
    )

    veiculo = Column(String(50))

    placa_veiculo = Column(String(10))

    entregas = relationship(
        "Entrega",
        back_populates="entregador"
    )