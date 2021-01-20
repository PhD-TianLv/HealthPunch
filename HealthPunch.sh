# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/root/conda/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/root/conda/etc/profile.d/conda.sh" ]; then
        . "/root/conda/etc/profile.d/conda.sh"
    else
        export PATH="/root/conda/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

cd ~/WorkSpace/HealthPunch
conda activate HealthPunch
python main.py
conda deactivate
