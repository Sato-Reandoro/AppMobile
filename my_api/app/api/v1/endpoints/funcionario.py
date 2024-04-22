# /api/v1/endpoints/funcionario.py
import select
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuarios_model import UsuarioModel
from core.deps import get_session, get_current_user
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp

router = APIRouter()


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_funcionario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session), current_user: UsuarioModel = Depends(get_current_user)):
    if not current_user.eh_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem criar novos funcionários."
        )
    # Implementação do signup para funcionários
    pass

@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_funcionario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session), current_user: UsuarioModel = Depends(get_current_user)):
    if not current_user.eh_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem atualizar funcionários."
        )
    # Implementação do put para funcionários
    pass

@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_funcionario(usuario_id: int, db: AsyncSession = Depends(get_session), current_user: UsuarioModel = Depends(get_current_user)):
    if not current_user.eh_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem deletar funcionários."
        )
    # Implementação do delete para funcionários
    pass



@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

@router.get('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_funcionario(usuario_id: int, db: AsyncSession = Depends(get_session), current_user: UsuarioModel = Depends(get_current_user)):
    if current_user.id != usuario_id and not current_user.eh_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem visualizar outros funcionários."
        )
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(
                detail=f'ID do Usuário: {str(usuario_id)}, Não encontrado na Base de Dados!',
                status_code=status.HTTP_404_NOT_FOUND
            )
            
            
