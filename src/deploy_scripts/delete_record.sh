#!/bin/bash

curl http://localhost:8042/tools/find -d '{"Level":"Study","Query":{"StudyDate":"20120101-20121231"}}'
[
   "6e2c0ec2-5d99c8ca-c1c21cee-79a09605-68391d12",
   "ef2ce55f-9342856a-aee23907-2667e859-9f3b734d"
]
curl -X DELETE http://localhost:8042/studies/6e2c0ec2-5d99c8ca-c1c21cee-79a09605-68391d12
curl -X DELETE http://localhost:8042/studies/ef2ce55f-9342856a-aee23907-2667e859-9f3b734d