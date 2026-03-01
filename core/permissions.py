from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated

class CustomIsAuthenticated(IsAuthenticated):
    '''
    Permissão personalizada que retorna 401 ao invés de 403 para usuários não autenticados. 

    Serve como checkagem do funcionamento da autenticação JWT. Se o token for inválido ou expirado, o usuário receberá 401, indicando que precisa se autenticar novamente. Auxilia o frontend a identificar quando o token não é mais válido e redirecionar o usuário para a tela de login.
    '''

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True
        
        raise NotAuthenticated(detail="Acesso negado: Você precisa fazer login ou ser admin para acessar este recurso.")