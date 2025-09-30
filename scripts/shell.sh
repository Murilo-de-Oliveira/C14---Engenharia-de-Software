echo "Rodou o pipeline"
pwd
echo "Mandando e-mail com mail do linux para $DEST_EMAIL" | mail -s "a subject" "$DEST_EMAIL"