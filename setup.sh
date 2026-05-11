mkdir ~p ~/.streamlit/
echo "\
[server]\n\
port= $PORT\n\
headless = true\n\
enableCORS=false\n\
\n\[client]\n\
caching = false\n\
\n\[global]\n\
showErrorDetails = true\n\
" > ~/.streamlit/config.toml