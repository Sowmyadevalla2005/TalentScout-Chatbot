#!/bin/bash

# Setup script for deploying Streamlit apps

mkdir -p ~/.streamlit

echo "[server]
headless = true
port = \$PORT
enableCORS = false
" > ~/.streamlit/config.toml 