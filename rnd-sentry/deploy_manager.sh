#!/usr/bin/env bash
# Менеджер управления процесами развертывания и эксплуатации.
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
# Список доступных команд. Команда передается первым аргументом.
# Запуск без аргументов выполняет сборку образа и старт контейнера приложения.
commands=(
"help"
"run"
"init"
"stop"
)

if [[ " ${commands[@]} " =~ " $1 " ]]; then
    if [ "$1" == ${commands[0]} ]; then
    # Список всех команд.
        echo -e "${GREEN}Аvaliable commands:${NC}"
        echo ${commands[*]}
    else
        echo -e "${GREEN} $1 - command was provided.${NC}"
        if [ "$1" == ${commands[1]} ]; then
            echo -e "Sentry will be deployed!"
            # Запуск sentry из docker-compose
            export $(cat .env_stack)
            docker-compose up -d
            echo "Service deployed."

        elif [ "$1" == ${commands[2]} ]; then
            # Создание окружения для sentry
            base_image_default=sentry:9.0rnd

            echo -e "Provide base sentry image (default ${GREEN} $base_image_default ${NC})"
            read user_answer
            export SENTRY_IMAGE_NAME=${user_answer:-$base_image_default}
            echo SENTRY_IMAGE_NAME=${SENTRY_IMAGE_NAME} > .env_stack

            echo -e "Secret sentry key will generate!"
            export SENTRY_SECRET_KEY=$(docker run --rm ${SENTRY_IMAGE_NAME} config generate-secret-key)
            echo SENTRY_SECRET_KEY=${SENTRY_SECRET_KEY} >> .env_stack
            echo -e "Secret key generated: ${GREEN} $SENTRY_SECRET_KEY ${NC}"

            pg_host_default="172.20.0.1"
            echo -e "Provide postgresql host (default ${GREEN} $pg_host_default ${NC})"
            read user_answer
            export SENTRY_POSTGRES_HOST=${user_answer:-$pg_host_default}
            echo SENTRY_POSTGRES_HOST=${SENTRY_POSTGRES_HOST} >> .env_stack

            pg_port_default=5432
            echo -e "Provide postgres port (default ${GREEN} $pg_port_default ${NC})"
            read user_answer
            export SENTRY_POSTGRES_PORT=${user_answer:-$pg_port_default}
            echo SENTRY_POSTGRES_PORT=${SENTRY_POSTGRES_PORT} >> .env_stack

            pg_base_default=sentry
            echo -e "Provide database name (default ${GREEN} $pg_base_default ${NC})"
            read user_answer
            export SENTRY_DB_NAME=${user_answer:-$pg_base_default}
            echo SENTRY_DB_NAME=${SENTRY_DB_NAME} >> .env_stack

            pg_user_default=sentry
            echo -e "Provide user name (default ${GREEN} $pg_user_default ${NC})"
            read user_answer
            export SENTRY_DB_USER=${user_answer:-$pg_user_default}
            echo SENTRY_DB_USER=${SENTRY_DB_USER} >> .env_stack

            pg_pass_default=sentry
            echo -e "Provide user password (default ${GREEN} $pg_pass_default ${NC})"
            read user_answer
            export SENTRY_DB_PASSWORD=${user_answer:-$pg_pass_default}
            echo SENTRY_DB_PASSWORD=${SENTRY_DB_PASSWORD} >> .env_stack

            redis_host_default=redis
            echo -e "Provide redis host (default ${GREEN} $redis_host_default ${NC})"
            read user_answer
            export SENTRY_REDIS_HOST=${user_answer:-$redis_host_default}
            echo SENTRY_REDIS_HOST=${SENTRY_REDIS_HOST} >> .env_stack

            memcached_host_default=memcached
            echo -e "Provide memcached host (default ${GREEN} $memcached_host_default ${NC})"
            read user_answer
            export SENTRY_MEMCACHED_HOST=${user_answer:-$memcached_host_default}
            echo SENTRY_MEMCACHED_HOST=${SENTRY_MEMCACHED_HOST} >> .env_stack

            email_from_default=sentry@localhost
            echo -e "Provide mail from header (default ${GREEN} $email_from_default ${NC})"
            read user_answer
            export SENTRY_SERVER_EMAIL=${user_answer:-$email_from_default}
            echo SENTRY_SERVER_EMAIL=${SENTRY_SERVER_EMAIL} >> .env_stack

            email_host_default=sentry.sbear.ru
            echo -e "Provide smtp mail host (default ${GREEN} $email_host_default ${NC})"
            read user_answer
            export SENTRY_EMAIL_HOST=${user_answer:-$email_host_default}
            echo SENTRY_EMAIL_HOST=${SENTRY_EMAIL_HOST} >> .env_stack

            echo -e "${GREEN}File .env_stack generated ${NC}"
            cat .env_stack
            

            export SENTRY_REDIS_HOST=sentry-temp-redis
            docker run -d --rm --name ${SENTRY_REDIS_HOST} --network="web-apps-network" redis:4.0-alpine
            docker run -it --rm \
            --network="web-apps-network" \
            -e SENTRY_SECRET_KEY=${SENTRY_SECRET_KEY} \
            -e SENTRY_POSTGRES_HOST=${SENTRY_POSTGRES_HOST} \
            -e SENTRY_POSTGRES_PORT=${SENTRY_POSTGRES_PORT} \
            -e SENTRY_DB_NAME=${SENTRY_DB_NAME} \
            -e SENTRY_DB_USER=${SENTRY_DB_USER} \
            -e SENTRY_DB_PASSWORD=${SENTRY_DB_PASSWORD} \
            -e SENTRY_REDIS_HOST=${SENTRY_REDIS_HOST} \
             ${SENTRY_IMAGE_NAME} upgrade
            docker stop ${SENTRY_REDIS_HOST}

        elif [ $1 == ${commands[3]} ]; then
            # Остановка сервиса
            echo -e "${YELLOW} will shut down ${NC}"
            docker-compose down
        fi
    fi
else
    echo -e "${RED}$0 $1 - Bad command provided!${NC} ${YELLOW}Provide one of: [${commands[*]}] . ${NC}"
fi
