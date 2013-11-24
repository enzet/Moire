au BufRead,BufNewFile *.moi set filetype=moi

" Vim syntax file
" Language: Moire markup
" Maintainer: Sergey Vartanov
" Latest Revision: 30 October 2013

if exists("b:current_syntax")
   finish
endif

syn match number '}'
syn match number '\\[a-z0-6]\+[\n ]\+{'
syn match number '}[\n ]\+{'
