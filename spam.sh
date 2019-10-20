
spam () {
  for ((i=1;i<=$1;i++)); do 
    curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"urls":["http://www.dummyimage.com/80x80", "http://www.dumimage.com/40x40"]}' \
    http://localhost:8000/v1/images/upload &
    done
  wait
}

time spam $1

