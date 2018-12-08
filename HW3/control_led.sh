IP=$1
PORT=5000
curl  --header "Content-Type: application/json" \
      --request POST \
      http://$IP:$PORT/LED/on
echo ""
sleep 1

for i in {0..100..10}
do
curl  --header "Content-Type: application/json" \
      --request POST \
      --data "{\"color\": \"red\", \"intensity\": $i}" \
      http://$IP:$PORT/LED
echo ""
sleep 1
done

curl  --header "Content-Type: application/json" \
      --request POST \
      --data "{\"color\": \"blue\", \"intensity\": 50}" \
      http://$IP:$PORT/LED
echo ""
sleep 1

curl  --header "Content-Type: application/json" \
      --request POST \
      --data "{\"color\": \"green\", \"intensity\": 50}" \
      http://$IP:$PORT/LED
echo ""
sleep 1

curl  --header "Content-Type: application/json" \12
      --request POST \
      http://$IP:$PORT/LED/off
echo ""

sleep 1
curl  --header "Content-Type: application/json" \
      --request POST \
      http://$IP:$PORT/LED/on
echo ""

curl  --header "Content-Type: application/json" \
      --request GET \
      http://$IP:$PORT/LED/info
echo ""
