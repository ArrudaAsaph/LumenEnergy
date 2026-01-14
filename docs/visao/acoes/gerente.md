# GERENTE

**Usuário responsável pela coordenação dos papéis e pela gestão operacional da plataforma.**
Ele não é dono do sistema (empresa), mas é quem **faz tudo funcionar no dia a dia**.

## Ações:

* [Cadastro de usuários do sistema](#cadastro-de-usuários-do-sistema)
* [Gerenciamento de permissões e acessos](#gerenciamento-de-permissões-e-acessos)
* [Gerenciamento do rateamento de energia](#gerenciamento-do-rateamento-de-energia)
* [Gerenciamento das usinas de geração](#gerenciamento-das-usinas-de-geração)
* [Vinculação de analistas às usinas](#vinculação-de-analistas-às-usinas)
* [Gerenciamento das gerações das usinas](#gerenciamento-das-gerações-das-usinas)
* [Gerenciamento de pagamentos e faturas](#gerenciamento-de-pagamentos-e-faturas)
* [Gerenciamento de contratos](#gerenciamento-de-contratos)
* [Cadastro de vendedores](#cadastro-de-vendedores-não-usuários)
* [Gerenciamento de pagamento de vendedores](#gerenciamento-de-pagamento-de-vendedores)

---

## Cadastro de usuários do sistema

**(exceto empresa e gerente)**
obs: **(usuários são pessoas que possuem acesso direto ao sistema, com login e senha)**

### O que significa

O gerente é responsável por criar e manter os usuários operacionais da plataforma, garantindo que cada pessoa tenha acesso apenas ao que lhe compete.

### O que ele faz

* Cria consumidores, investidores e analistas
* Define dados básicos (nome, e-mail, tipo de usuário)
* Ativa ou desativa usuários
* Atualiza informações cadastrais, caso necessário

### Limites

* Não cria empresas
* Não cria outros gerentes
* Não altera regras globais do sistema

---

## Gerenciamento de permissões e acessos

### O que significa

Controla **o que cada tipo de usuário pode ver ou fazer** dentro do sistema.

### O que ele faz

* Define permissões por papel (investidor, consumidor, analista)
* Bloqueia acessos indevidos
* Ajusta permissões em casos especiais

### Limites

* Não cria novos papéis estruturais
* Não altera regras de negócio do sistema

---

## Gerenciamento do rateamento de energia

### O que significa

O gerente define **como a energia gerada pelas usinas será distribuída entre os consumidores**.

### O que ele faz

* Cria e ajusta regras de rateamento
* Define percentuais ou cotas
* Garante que a soma do rateamento seja válida
* Corrige inconsistências operacionais
* Simula o rateamento antes de aplicar
* Visualiza o impacto antes de confirmar alterações

### Limites

* Não altera dados históricos consolidados
* Não interfere diretamente na geração da usina

---

## Gerenciamento das usinas de geração

### O que significa

Administra as informações estruturais das usinas cadastradas no sistema.

### O que ele faz

* Cadastra novas usinas
* Atualiza dados técnicos
* Define status da usina (ativa, manutenção, inativa)
* Associa investidores e analistas
* Aprova limpeza e manutenções

### Limites

* Não altera dados técnicos históricos
* Não altera medições externas (ex: concessionária)

---

## Vinculação de analistas às usinas

**Existem o analista Financeiro e o Energético**

### O que significa

Controla quais analistas têm acesso às informações de cada usina.

### O que ele faz

* Associa analistas energéticos e financeiros
* Define escopo de acesso por usina
* Revoga acessos quando necessário

### Limites

* Analistas não alteram dados críticos
* Acesso sempre restrito ao escopo definido

---

## Gerenciamento das gerações das usinas

### O que significa

Acompanha e valida os dados de geração de energia.

### O que ele faz

* Visualiza dados de geração
* Identifica inconsistências
* Confirma dados antes do rateamento

### Limites

* Não altera medições oficiais
* Não edita dados históricos consolidados

---

## Gerenciamento de pagamentos e faturas

### O que significa

Controla o ciclo financeiro dos consumidores.

### O que ele faz

* Emite faturas
* Acompanha pagamentos
* Identifica inadimplência
* Aplica regras de cobrança

### Limites

* Não altera valores pagos
* Não apaga histórico financeiro

---

## Gerenciamento de contratos

### O que significa

Administra contratos firmados entre empresa, consumidores, investidores e vendedores.

### O que ele faz

* Cria contratos
* Atualiza cláusulas
* Acompanha vigência
* Encerra contratos

### Limites

* Não altera contratos assinados retroativamente

---

## Cadastro de vendedores (não usuários)

### O que significa

Vendedores não acessam o sistema, mas seus dados são registrados para controle comercial.

### O que ele faz

* Cadastra dados pessoais e bancários
* Vincula vendedores a contratos
* Acompanha desempenho

### Limites

* Vendedores não fazem login
* Não possuem permissões no sistema

---

## Gerenciamento de pagamento de vendedores

### O que significa

Controla pagamentos e comissões dos vendedores.

### O que ele faz

* Calcula comissões
* Registra pagamentos
* Gera relatórios financeiros

### Limites

* Não altera pagamentos já realizados

