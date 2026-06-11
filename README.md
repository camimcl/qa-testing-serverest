Test Cases: 
Criação (POST):

Criar usuário com sucesso (Caminho Feliz).

Tentar criar usuário com e-mail já cadastrado (Regra de negócio).

Tentar criar usuário faltando o campo "nome".

Tentar criar usuário faltando o campo "email".

Tentar criar usuário faltando o campo "password".

Busca (GET):
6. Listar todos os usuários com sucesso.
7. Buscar um usuário específico pelo ID válido.
8. Buscar um usuário por um ID inexistente (ex: ID_FALSO_123).

Atualização (PUT):
9. Atualizar os dados de um usuário existente com sucesso.

Exclusão (DELETE):
10. Excluir um usuário com sucesso.
11. Tentar excluir um usuário que não existe.