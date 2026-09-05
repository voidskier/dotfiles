#
# ~/.bashrc
#

export PATH="$HOME/.local/bin:$PATH"

export EDITOR=vim
export VISUAL=vim

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias zzz='zzz.sh'
alias genpwd='genpwd.sh'

PS1='[\u@\h \W]\$ '
