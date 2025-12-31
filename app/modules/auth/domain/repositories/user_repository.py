from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.user_entity import User
from ..value_objects.email_vo import Email
from ..value_objects.username_vo import Username
from app.shared.domain.value_objects.id_vo import EntityId


class UserRepository(ABC):
    """Interface do Repository de User (Port)"""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Cria um novo usuário no banco de dados.
        
        Args:
            user: Entidade User a ser persistida
            
        Returns:
            User: Usuário criado com dados atualizados do banco
            
        Raises:
            RepositoryException: Erro ao persistir no banco
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: EntityId) -> Optional[User]:
        """
        Busca usuário por ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Optional[User]: Usuário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        """
        Busca usuário por email.
        
        Args:
            email: Email do usuário (Value Object)
            
        Returns:
            Optional[User]: Usuário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_username(self, username: Username) -> Optional[User]:
        """
        Busca usuário por nome de usuário.
        
        Args:
            username: Nome de usuário (Value Object)
            
        Returns:
            Optional[User]: Usuário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """
        Verifica se existe usuário com o email informado.
        
        Args:
            email: Email a ser verificado
            
        Returns:
            bool: True se existe, False caso contrário
        """
        pass
    
    @abstractmethod
    async def exists_by_username(self, username: Username) -> bool:
        """
        Verifica se existe usuário com o username informado.
        
        Args:
            username: Username a ser verificado
            
        Returns:
            bool: True se existe, False caso contrário
        """
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """
        Atualiza dados do usuário.
        
        Args:
            user: Entidade User com dados atualizados
            
        Returns:
            User: Usuário atualizado
            
        Raises:
            UserNotFoundException: Usuário não encontrado
            RepositoryException: Erro ao atualizar
        """
        pass
    
    @abstractmethod
    async def delete(self, user_id: EntityId) -> bool:
        """
        Deleta usuário por ID.
        
        Args:
            user_id: ID do usuário a ser deletado
            
        Returns:
            bool: True se deletado com sucesso, False se não encontrado
        """
        pass
    
    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Lista todos os usuários com paginação.
        
        Args:
            skip: Quantidade de registros a pular
            limit: Quantidade máxima de registros a retornar
            
        Returns:
            List[User]: Lista de usuários
        """
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """
        Conta total de usuários.
        
        Returns:
            int: Quantidade total de usuários
        """
        pass
    
    @abstractmethod
    async def add_role_to_user(self, user_id: EntityId, role_id: EntityId) -> bool:
        """
        Adiciona uma role a um usuário.
        
        Args:
            user_id: ID do usuário
            role_id: ID da role
            
        Returns:
            bool: True se adicionado com sucesso
        """
        pass
    
    @abstractmethod
    async def remove_role_from_user(self, user_id: EntityId, role_id: EntityId) -> bool:
        """
        Remove uma role de um usuário.
        
        Args:
            user_id: ID do usuário
            role_id: ID da role
            
        Returns:
            bool: True se removido com sucesso
        """
        pass
