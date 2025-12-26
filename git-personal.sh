#!/bin/bash

git-personal() {
    git config --global user.name "pierreamir123"
    git config --global user.email "pierrebassily@gmail.com"
    echo "Switched to PERSONAL profile ✅"
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/pierre
    echo "ssh Activated"
}
