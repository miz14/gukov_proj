#!/bin/bash

# Файл-маркер для отслеживания выполнения скрипта
MARKER_FILE="/var/lib/.docker_installation_complete"

# Проверяем, не выполнялся ли уже скрипт
if [ -f "$MARKER_FILE" ]; then
    echo "Docker и сопутствующие компоненты уже установлены. Пропускаем выполнение скрипта."
    exit 0
fi

# Функция для проверки установки пакета
is_installed() {
    dpkg -l "$1" 2>/dev/null | grep -q "^ii"
}

# Функция для проверки существования команды
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Начинаем установку Docker и необходимых компонентов..."

# Update package index (только если не обновлялись сегодня)
if [ ! -f /var/cache/apt/pkgcache.bin ] || [ $(find /var/cache/apt/pkgcache.bin -mtime +0 | wc -l) -eq 1 ]; then
    sudo apt-get update
fi

# Install prerequisites (только те, которые не установлены)
PREREQUISITES="apt-transport-https ca-certificates curl gnupg-agent software-properties-common"
TO_INSTALL=""

for pkg in $PREREQUISITES; do
    if ! is_installed "$pkg"; then
        TO_INSTALL="$TO_INSTALL $pkg"
    fi
done

if [ -n "$TO_INSTALL" ]; then
    sudo apt-get install -y $TO_INSTALL
fi

# Add Docker's official GPG key (только если не добавлен)
if ! sudo apt-key list | grep -q "Docker"; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
fi

# Add Docker repository (только если не добавлен)
if [ ! -f /etc/apt/sources.list.d/docker.list ]; then
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
fi

# Install Docker Engine (только если не установлен)
if ! command_exists docker; then
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    
    # Start and enable Docker
    sudo systemctl start docker
    sudo systemctl enable docker
else
    echo "Docker уже установлен"
fi

# Add current user to docker group (только если еще не добавлен)
if ! groups $USER | grep -q "\bdocker\b"; then
    sudo usermod -aG docker $USER
    echo "Пользователь $USER добавлен в группу docker. Необходимо перезайти в систему для применения изменений."
else
    echo "Пользователь $USER уже в группе docker"
fi

# Install Docker Compose (только если не установлен)
if ! command_exists docker-compose; then
    sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "Docker Compose уже установлен"
fi

# Configure firewall (только если правила не добавлены)
UFW_STATUS=$(sudo ufw status numbered | grep -E "(22/tcp|80/tcp|443/tcp)" | wc -l)
if [ "$UFW_STATUS" -lt 3 ]; then
    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw --force enable
else
    echo "Правила UFW уже настроены"
fi

# Создаем файл-маркер о завершении установки
sudo touch "$MARKER_FILE"
echo "Установка Docker и компонентов завершена успешно!"