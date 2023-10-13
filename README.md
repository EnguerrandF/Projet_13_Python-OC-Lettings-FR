# Projet 13 Python-OC-Lettings-FR
Mettez à l'échelle une application Django en utilisant une architecture modulaire
## Contexte projet
Orange County Lettings est une start-up dans le secteur de la location de biens immobiliers. La start-up est en pleine phase d’expansion aux États-Unis.

L'objectif de ce projet est :

* Mettre à l'échelle une application Django en utilisant une architecture modulaire.
* La réduction de divers problèmes technique.
* Mettre en place un environnement de test avec pytest.
*  Mettre en place un pipeline CI/CD et le déploiement du site web vers un hébergeur.(AWS de choisi).
* Surveillance de l'application et suivi des erreurs via Sentry.

## Déploiement  local du le projet Python-OC-Lettings-FR
#### 1- Sélectionner la commande Git ci-dessous afin de récupérer le projet:
```
     git clone https://github.com/EnguerrandF/Projet_13_Python-OC-Lettings-FR.git
```
---
#### 2- Accéder au dossier:
```
    cd nom_du_dossier
```
---
#### 3- Créer l'environnement virtuel en exécutant la commande ci-dessous:
```
    python -m venv env
```
---
#### 4- Activer l'environnement:
* Windows:
```
    env/Scripts/activate
```
* Mac et linux:
```
    source venv/bin/activate
```
---
#### 5- Ajoutez-les modules du fichier requirements.txt en executant la commande si dessous:
```
    pip install -r requirements.txt
```
---
#### 7- Lancer le serveur:
```
    python .\manage.py runserver 
```
---
#### 8- Accéder au site via URL suivante:
- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
---
#### 9- Execution de flake8:
```
    flake8
```
#### Pas de réponse si le linting est correct.
---
#### 10- Execution des tests avec pytest:
```
    pytest
```
#### Réponse si tous les tests sont valide:
```
app_lettings/tests.py::test_lettings
app_lettings/tests.py::test_lettings PASSED [20%]
app_lettings/testspy::test_lettings_details PASSED [40%]
app_profiles/tests.py::test_profiles PASSED [60%]
app_profiles/testspy::test_profiles_details PASSED [80%]
app_oc_lettings_site/tests.py::test_homepage PASSED [100%] 

5 passed in 1.03s
```
---

## Déploiement continue du le projet Python-OC-Lettings-FR
J'ai réalisé le déploiement continue sur circleCi. CircleCI est une plate-forme d'intégration continue et de livraison continue qui peut être utilisée pour mettre en œuvre des pratiques Devops. CicleCi se lie à votre projet github, lors d'un nouveaux push il déclenche des taches rédigé dans un fichier config.yml. Les taches peuvent être des tests, builds d'images et des déploiements de votre application sur un hébergeur.

### Voici mon déploiement avec cicle ci sur ce projet:
#### 1- Execution des tests:
_Dans le fichier conf.yml :_
```
  test-app:
    executor: python/default
    steps:
      - checkout
      - python/install-packages:
          pip-dependency-file: requirements.txt
          pkg-manager: pip
      - run:
          name: Run tests pytest
          command: pytest
      - run:
          name: Run Flake8
          command: flake8
```
Dans un containeur j'installe les dépendances avec pip avec le fichier requirements.tkt et je lance les commandes pytest et flake8. S'il ne retourne pas des réponses valides le déploiement de cette tache (test-app) sera mise en erreur.

---

#### 1- Creation de l'image docker et push sur aws ecr:

Docker est une plateforme de virtualisation légère qui permet d'emballer des applications et leurs dépendances dans des conteneurs, facilitant ainsi le déploiement, la gestion et la portabilité des applications sur différents environnements.

Pour créer une image docker avec notre application fonctionnel nous devons rédiger un fichier de configuration appelé _dockerfile_.

_Dans le fichier dockerfile :_
```
FROM python:3.12.0b4-alpine3.18

ENV PORT=80
ARG SENTRY_URL=default_value
ENV SENTRY_URL=$SENTRY_URL

WORKDIR /app

COPY ./ ./


RUN apk update && \
    apk upgrade && \
    pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:$PORT
```
1. "FROM python:3.12.0b4-alpine3.18"

    On se base sur une image docker déjà existante du dockerHub.

2. "ARG SENTRY_URL=default_value" et "ENV SENTRY_URL=$SENTRY_URL"

    On transmet une variable de CircleCi à l'application django pour sentry.

3. "WORKDIR /app" et "COPY ./ ./"

    On se place dans le dossier _app_ dans le containeur docker et on copie tout le code de notre application django dans ce dossier.

4. "RUN apk update && \ apk upgrade && \ pip install -r requirements.txt"

    On met à jour les packages alpine et on installe avec pip les dépences du projet django.

5. "CMD python manage.py runserver 0.0.0.0:$PORT"

    On exécute cette commande pour lancer le serveur django.

_Dans le fichier conf.yml :_
```
  build-and-push-aws-ecr:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - setup_remote_docker:
          version: 20.10.14
      - aws-cli/setup:
          aws-access-key-id: AWS_ACCESS_KEY_ID
          aws-secret-access-key: AWS_SECRET_ACCESS_KEY
      - run:
          name: Build Docker image
          command: docker build --build-arg SENTRY_URL=$SENTRY_URL -t $REGISTRY_AWS:$CIRCLE_SHA1 .
      - run:
          name: Connection docker to AWS ECR
          command: aws ecr-public get-login-password --region $AWS_REGION_REPO | docker login --username AWS --password-stdin $AWS_CMD_LOGIN_REGISTRY
      - run:
          name: Push AWS ECR
          command: |
              docker tag $REGISTRY_AWS:$CIRCLE_SHA1 $REGISTRY_AWS:latest
              docker push $REGISTRY_AWS:latest
              docker push $REGISTRY_AWS:$CIRCLE_SHA1
```
On se connecte à aws avec l'orbs de circleCi "aws-cli/setup".
On exécute la commande _"docker build --build-arg SENTRY_URL=$SENTRY_URL -t $REGISTRY_AWS:$CIRCLE_SHA1 ."_ qui construit l'image à partir du fichier _dockerfile_, transmet une variable de circleCi a l'application docker et on renomme ce containeur au nom du registry aws avec comme tag l'identifiant du push de git. On configure le docker du containeur pour qui push sur aws ecr. Et nous exécutons les commandes docker pour push l'image sur aws ecr.

---
_Dans le fichier conf.yml :_
```
  deploy_application_aws:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - aws-cli/setup:
          aws-access-key-id: AWS_ACCESS_KEY_ID
          aws-secret-access-key: AWS_SECRET_ACCESS_KEY
          aws-region: AWS_REGION
      - run:
         name: Update task
         command: aws ecs register-task-definition --debug --region $AWS_REGION --family $AWS_FAMILY_TASK --network-mode awsvpc --execution-role-arn $AWS_EXECUTION_ROLE_ARN --requires-compatibilities FARGATE --cpu 512 --memory 1024 --container-definitions '[{"name":"projet_13_python-oc-lettings-fr","image":"'$REGISTRY_AWS:$CIRCLE_SHA1'","cpu":512,"memory":1024,"logConfiguration":{"logDriver":"awslogs","options":{"awslogs-region":"'$AWS_REGION'","awslogs-group":"13-container","awslogs-create-group":"true","awslogs-stream-prefix":"13"}},"portMappings":[{"name":"projet_13_python-oc-lettings-fr-80-tcp","containerPort":80,"hostPort":80,"protocol":"tcp","appProtocol":"http","containerPort":80}]}]'
      - run:
         name: Update service
         command: aws ecs update-service --region $AWS_REGION --cluster $AWS_CLUSTER --service $AWS_SERVICE --task-definition $AWS_FAMILY_TASK --network-configuration '{"awsvpcConfiguration":{"subnets":["'$AWS_SUBNET'"],"securityGroups":["'$AWS_SECURITY_GRP'"],"assignPublicIp":"ENABLED"}}'
```

Dans cette nouvelle tache, on se connecte a aws avec l'orbs de circleCi "aws-cli/setup".
Nous mettons à jour la tache aws avec la nouvelle image docker.
Et on remplace la tache en cours de fonctionnement sur notre cluster aws par la nouvelle.

---
_Dans le fichier conf.yml :_
```
workflows:
  sample:
    jobs:
      - test-app
      - build-and-push-aws-ecr:
          requires:
            - test-app
          filters:
            branches:
              only:
                - master
      - deploy_application_aws:
          requires:
            - build-and-push-aws-ecr
          filters:
            branches:
              only:
                - master
```
On initialise un job qui comprend plusieurs taches.
On exécute les taches dans l'ordre suivant :  
- _test-app_
- _build-and-push-aws-ecr_
- _deploy_application_aws_

La tache _build-and-push-aws-ecr_ requière  la tache _test-app_ en **Success**.
La tache _deploy_application_aws_ requière  la tache _build-and-push-aws-ecr_ en **Success**.

Si les taches requise ne sont pas **Success** le deploiement s'arrête.
Les taches _build-and-push-aws-ecr_ et _deploy_application_aws_ s'exécuterons que dans les pushs de la branch git master

---