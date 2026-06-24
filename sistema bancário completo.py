from abc import ABC, abstractmethod
from datetime import datetime


class Historico:
    def _init_(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao._class.name_,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def _init_(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.depositar(self.valor)


class Saque(Transacao):
    def _init_(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.sacar(self.valor)


class Cliente:
    def _init_(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def _init_(self, nome, cpf, data_nascimento, endereco):
        super()._init_(endereco)

        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Conta:
    def _init_(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False

        self._saldo -= valor
        self._historico.adicionar_transacao(Saque(valor))
        print("Saque realizado com sucesso.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido.")
            return False

        self._saldo += valor
        self._historico.adicionar_transacao(Deposito(valor))
        print("Depósito realizado com sucesso.")
        return True


class ContaCorrente(Conta):
    def _init_(self, numero, cliente):
        super()._init_(numero, cliente)

        self.limite = 500
        self.limite_saques = 3
