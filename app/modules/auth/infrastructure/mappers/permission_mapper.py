from app.modules.auth.infrastructure.models.permission_model import PermissionModel
from ...domain.entities.permission_entity import Permission
from ...domain.value_objects.permission_name_vo import PermissionName
from app.shared.domain.value_objects.id_vo import EntityId
from typing import List


class PermissionMapper:
    """
    Mapper para conversão entre Permission Entity e PermissionModel.
    
    Padrão: Entity (Domain) ↔ Model (Infrastructure)
    """
    
    @staticmethod
    def to_entity(model: PermissionModel) -> Permission:
        """
        Converte PermissionModel (SQLAlchemy) para Permission Entity (Domain).
        
        Args:
            model: PermissionModel do banco
            
        Returns:
            Permission: Entity de domínio
        """
        return Permission.reconstruct(
            id=EntityId(model.id),
            nome=PermissionName(model.nome),
            descricao=model.descricao,
            data_criacao=model.data_criacao
        )
    
    @staticmethod
    def to_model(entity: Permission) -> PermissionModel:
        """
        Converte Permission Entity (Domain) para PermissionModel (SQLAlchemy).
        
        Args:
            entity: Permission entity do domínio
            
        Returns:
            PermissionModel: Model do SQLAlchemy
        """
        return PermissionModel(
            id=entity.id.value,
            nome=entity.nome.value,
            descricao=entity.descricao,
            data_criacao=entity.data_criacao
        )
    
    @staticmethod
    def update_model_from_entity(
        model: PermissionModel,
        entity: Permission
    ) -> None:
        """
        Atualiza um PermissionModel existente com dados da Entity.
        
        Usado em operações de UPDATE.
        
        Args:
            model: PermissionModel existente
            entity: Permission entity com dados atualizados
        """
        model.descricao = entity.descricao
    
    @staticmethod
    def to_entities(models: List[PermissionModel]) -> List[Permission]:
        """
        Converte lista de models para lista de entities.
        
        Args:
            models: Lista de PermissionModel
            
        Returns:
            List[Permission]: Lista de entities
        """
        return [PermissionMapper.to_entity(model) for model in models]
