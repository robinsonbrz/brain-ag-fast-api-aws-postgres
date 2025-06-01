# Projeto Lambda Python Fast Api, Terraform e CI / CD


### Para utilizar o Terraform nessa configuração crie um bucket S3 com o nome: *nome-unico-aws-s3* antes de executar ```terraform init```

Ou com o aws cli

```bash
aws s3 mb s3://nome-unico-aws-s3  --region us-east-1
```
Coloque o mesmo nome de bucket no arquivo infra-lambda/main.tf na chave bucket:

```
  backend "s3" {
    bucket = "nome-unico-aws-s3"
    key    = "estado/terraform.tfstate"
    region = "us-east-1"
  }
```


Clonar o repositório

```
git clone git@github.com:robinsonbrz/aws-terraform-lambda-fast-api-gitactions.git

cd aws-terraform-lambda-fast-api-gitactions
```


### Você pode configurar secrets e vars no GitHub Actions do repositório:

- Configurar Secrets (AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY)

Secrets são usadas para armazenar credenciais de forma segura.

Passos:

    Vá até o seu repositório no GitHub.

        Clique em Settings (Configurações).

            No menu esquerdo, role para baixo até Secrets and variables > Actions.

Clique na aba Secrets.

    Clique em New repository secret e adicione:

        Nome: AWS_ACCESS_KEY_ID

            Valor: Sua chave de acesso da AWS

                Salve

    Repita o processo para AWS_SECRET_ACCESS_KEY.


Configurar Variáveis (AWS_REGION)

Variáveis (vars) são usadas para armazenar valores não sensíveis.

Passos:

No mesmo menu Settings > Secrets and variables > Actions, 

    vá para a aba Variables.

        Clique em New repository variable.

    Adicione:

        Nome: AWS_REGION

            Valor: A região da AWS (exemplo: us-east-1)

                Salve

Com isso todo push na branch "main" fará o disparo da pipe Git Actions

Verifique o log na aba Actions do GitHub

E no steps "Terraform Apply" encontre a url da api como no exemplo abaixo haverá uma nova url

```
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

api_url = "https://fx6aarhaxyniegmieue2n7eazy0qpame.lambda-url.us-east-1.on.aws/"
```