showhelp=${1:-false}
if [ "$showhelp" = help ];
then
    echo 'Syntax: convert-to-pdf.sh <file_name> [show_code=[true|false], default=true] [to=[pdf|tex], default=pdf]'
else
    code_on=${2:-true}
    format_on=${3:-true}
    if ["$format_on" = true];
    then
        if ["$code_on" = true ];
        then
            exec ~/Programs/anaconda3/bin/jupyter nbconvert --to $2 $1 --execute
        else
            ~/Programs/anaconda3/bin/jupyter nbconvert --to $2 --template hidecode $1 --execute
        fi
    else
        if ["$code_on" = true ];
        then
            exec ~/Programs/anaconda3/bin/jupyter nbconvert --to pdf $1 --execute
        else
            ~/Programs/anaconda3/bin/jupyter nbconvert --to pdf --template hidecode $1 --execute
        fi
    fi
fi