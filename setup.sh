SECRET=$(openssl rand -hex 32)
touch .env
echo "SECRET_KEY='$SECRET'" >> .env