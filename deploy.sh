set -e
if [ -z "$PAT_1" ]; then
    echo "Must set PAT_1 environment variable to deploy."
    exit 1
fi

git clone https://github.com/anuraghazra/github-readme-stats.git --depth=1
cd github-readme-stats
pnpm i express
node express.js &
echo "Waiting for express to start..."
sleep 5
cd ..

export PREFIX="localhost:9000"
export URL_PATH="/top-langs/?username=sichanghe&langs_count=18&layout=compact&exclude_repo=CoreMLProto,reproduce_tensorflow_tensorflow_issue_61654,STATS401,learn_program,rails_tutorial,Notes_Steven,notes,mdbook_katex_template,igem-2022-dku-backup,mdbook_fancy_theme,BigDecimal-Matrix-and-column-vector-calculator-in-Java&hide=Batchfile,CSS,Handlebars,HTML,Jupyter%20Notebook,Less,Tex,VBScript,Markdown,Shell"
echo "Downloading most owned languages SVG..."
export SVG_NAME="most_owned_languages.svg"
curl "$PREFIX$URL_PATH" -o "$SVG_NAME"
sed -i -e 's/Most Used/Most Owned/g' -e 's/  //g' "$SVG_NAME"
cat most_owned_languages.svg
ls -lah most_owned_languages.svg

git add most_owned_languages.svg
if git diff --cached --quiet; then
    echo "No changes."
else
    echo "Commiting"
    git config --global user.name "SichangHe"
    git config --global user.email "sichanghe@users.noreply.github.com"
    git commit -m "Auto update of most_owned_languages.svg"
    git push -f
fi
