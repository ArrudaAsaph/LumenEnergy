
## Regras de Negócio (RN)

| **Código** | **Descrição**                                                                                                                                                | **Requisito(s) Atendido(s)** |
| :--------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------: |
|  **RN01**  | Apenas gerentes e empresas podem cadastrar usuários no sistema.                                                                                              |             RF01             |
|  **RN02**  | Apenas empresas podem gerenciar usuários do tipo gerente (cadastrar, atualizar, listar, ativar/desativar e controlar permissões e perfil).                   | RF01, RF02, RF03, RF04, RF05 |
|  **RN03**  | Não deve existir usuário que não esteja obrigatoriamente vinculado a uma pessoa ou a uma empresa.                                                            | RF01, RF02, RF03, RF04, RF05 |
|  **RN04**  | Não deve ser possível remover um usuário do sistema, apenas ativá-lo ou desativá-lo, preservando os dados históricos.                                        |             RF03             |
|  **RN05**  | O gerente pode cadastrar, atualizar, listar, ativar ou desativar apenas usuários vinculados à mesma empresa à qual ele pertence.                             |    RF01, RF02, RF03, RF05    |
|  **RN06**  | Usuários desativados não podem autenticar nem acessar funcionalidades do sistema.                                                                            |             RF03             |
|  **RN07**  | Não deve existir mais de um usuário com o mesmo e-mail ou identificador de acesso dentro da mesma empresa.                                                   |          RF01, RF02          |
|  **RN08**  | As permissões atribuídas a um usuário devem ser compatíveis com seu papel no sistema, não sendo permitido conceder privilégios superiores ao papel definido. |             RF04             |



