from dataclasses import dataclass
from typing import Optional

from ..value_objects.address_vo import Address
from ..value_objects.cep_vo import CEP
from app.shared.domain.value_objects.id_vo import EntityId


@dataclass(eq=False)
class Endereco:
    """Entidade Endereço do Domínio"""
    id: EntityId
    user_id: EntityId
    address: Address
    
    @staticmethod
    def create(
        user_id: EntityId,
        rua: str,
        cidade: str,
        estado: str,
        cep: str,
        pais: str = "Brasil"
    ) -> 'Endereco':
        """Factory method para criar um novo endereço"""
        return Endereco(
            id=EntityId.generate(),
            user_id=user_id,
            address=Address(
                rua=rua,
                cidade=cidade,
                estado=estado,
                cep=CEP(cep),
                pais=pais
            )
        )
    
    @staticmethod
    def reconstruct(
        id: EntityId,
        user_id: EntityId,
        address: Address
    ) -> 'Endereco':
        """Reconstrói um endereço existente"""
        return Endereco(
            id=id,
            user_id=user_id,
            address=address
        )
    
    # Properties para acesso fácil aos componentes do endereço
    @property
    def rua(self) -> str:
        return self.address.rua
    
    @property
    def cidade(self) -> str:
        return self.address.cidade
    
    @property
    def estado(self) -> str:
        return self.address.estado
    
    @property
    def cep(self) -> str:
        return str(self.address.cep)
    
    @property
    def pais(self) -> str:
        return self.address.pais
    
    def get_formatted_address(self) -> str:
        """Retorna endereço formatado para exibição"""
        return self.address.get_formatted()
    
    def get_cep_unformatted(self) -> str:
        """Retorna CEP sem formatação (apenas números)"""
        return self.address.cep.get_unformatted()
    
    def update_address(
        self,
        rua: Optional[str] = None,
        cidade: Optional[str] = None,
        estado: Optional[str] = None,
        cep: Optional[str] = None,
        pais: Optional[str] = None
    ) -> None:
        """Atualiza componentes do endereço"""
        new_rua = rua if rua is not None else self.address.rua
        new_cidade = cidade if cidade is not None else self.address.cidade
        new_estado = estado if estado is not None else self.address.estado
        new_cep = cep if cep is not None else str(self.address.cep)
        new_pais = pais if pais is not None else self.address.pais
        
        self.address = Address(
            rua=new_rua,
            cidade=new_cidade,
            estado=new_estado,
            cep=CEP(new_cep),
            pais=new_pais
        )
    
    def belongs_to_user(self, user_id: EntityId) -> bool:
        """Verifica se o endereço pertence a um usuário específico"""
        return self.user_id == user_id
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Endereco):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __str__(self) -> str:
        return self.get_formatted_address()
