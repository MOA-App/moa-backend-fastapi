from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from ..value_objects.email_vo import Email
from ..value_objects.password_vo import HashedPassword
from ..value_objects.username_vo import Username
from ..value_objects.person_name_vo import PersonName
from app.shared.domain.value_objects.id_vo import EntityId


@dataclass
class User:
    """Entidade de Usuário do Domínio"""
    id: EntityId
    nome: PersonName
    email: Email
    senha: HashedPassword
    nome_usuario: Username
    id_token_firebase: Optional[str]
    data_cadastro: datetime
    roles: List['Role'] = field(default_factory=list)
    enderecos: List['Endereco'] = field(default_factory=list)
    
    @staticmethod
    def create(
        nome: str,
        email: str,
        senha_hash: str,
        nome_usuario: str,
        id_token_firebase: Optional[str] = None
    ) -> 'User':
        """
        Factory method para criar um novo usuário.
        Valida todos os dados através dos Value Objects.
        """
        return User(
            id=EntityId.generate(),
            nome=PersonName(nome),
            email=Email(email),
            senha=HashedPassword(senha_hash),
            nome_usuario=Username(nome_usuario),
            id_token_firebase=id_token_firebase,
            data_cadastro=datetime.utcnow(),
            roles=[],
            enderecos=[]
        )
    
    @staticmethod
    def reconstruct(
        id: EntityId,
        nome: PersonName,
        email: Email,
        senha: HashedPassword,
        nome_usuario: Username,
        id_token_firebase: Optional[str],
        data_cadastro: datetime,
        roles: List['Role'],
        enderecos: List['Endereco']
    ) -> 'User':
        """
        Reconstrói um usuário existente (usado pelos repositories).
        """
        return User(
            id=id,
            nome=nome,
            email=email,
            senha=senha,
            nome_usuario=nome_usuario,
            id_token_firebase=id_token_firebase,
            data_cadastro=data_cadastro,
            roles=roles,
            enderecos=enderecos
        )
    
    # Métodos de Roles
    def add_role(self, role: 'Role') -> None:
        """Adiciona uma role ao usuário"""
        if role not in self.roles:
            self.roles.append(role)
    
    def remove_role(self, role: 'Role') -> None:
        """Remove uma role do usuário"""
        if role in self.roles:
            self.roles.remove(role)
    
    def has_role(self, role_name: str) -> bool:
        """Verifica se usuário tem uma role específica"""
        return any(role.nome.value == role_name.lower() for role in self.roles)
    
    def get_roles(self) -> List[str]:
        """Retorna lista com nomes das roles"""
        return [role.nome.value for role in self.roles]
    
    # Métodos de Permissions
    def has_permission(self, permission_name: str) -> bool:
        """Verifica se usuário tem uma permissão específica"""
        for role in self.roles:
            if role.has_permission(permission_name):
                return True
        return False
    
    def get_all_permissions(self) -> List[str]:
        """Retorna todas as permissões do usuário (sem duplicatas)"""
        permissions = set()
        for role in self.roles:
            for permission in role.permissions:
                permissions.add(permission.nome.value)
        return sorted(list(permissions))
    
    # Métodos de Atualização
    def update_email(self, new_email: str) -> None:
        """Atualiza o email com validação através do VO"""
        self.email = Email(new_email)
    
    def update_username(self, new_username: str) -> None:
        """Atualiza o nome de usuário com validação através do VO"""
        self.nome_usuario = Username(new_username)
    
    def update_name(self, new_name: str) -> None:
        """Atualiza o nome com validação através do VO"""
        self.nome = PersonName(new_name)
    
    def update_password(self, new_hashed_password: str) -> None:
        """Atualiza a senha (já deve estar hasheada)"""
        self.senha = HashedPassword(new_hashed_password)
    
    def update_firebase_token(self, token: Optional[str]) -> None:
        """Atualiza o token do Firebase"""
        self.id_token_firebase = token
    
    # Métodos de Endereços
    def add_endereco(self, endereco: 'Endereco') -> None:
        """Adiciona um endereço ao usuário"""
        if endereco not in self.enderecos:
            self.enderecos.append(endereco)
    
    def remove_endereco(self, endereco_id: EntityId) -> bool:
        """Remove um endereço pelo ID"""
        for endereco in self.enderecos:
            if endereco.id == endereco_id:
                self.enderecos.remove(endereco)
                return True
        return False
    
    def get_endereco_principal(self) -> Optional['Endereco']:
        """Retorna o primeiro endereço (considerado principal)"""
        return self.enderecos[0] if self.enderecos else None
    
    # Métodos de Informação
    def get_first_name(self) -> str:
        """Retorna o primeiro nome"""
        return self.nome.get_first_name()
    
    def is_active(self) -> bool:
        """Verifica se o usuário está ativo (pode adicionar lógica futura)"""
        return True
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
