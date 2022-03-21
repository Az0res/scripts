for file in $(find . -name '*.csv' )
    do
        #if [ $(wc -l $file) -lt 1 ] 
        #then
        #    echo $file
        #else 
            iconv -f UTF-16LE -t us-ascii -c -o "${file}_.csv" $file
        #fi
    done