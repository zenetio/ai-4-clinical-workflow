cd /opt/aihcnd-applications/OHIF-Viewer/
yarn config set workspaces-experimental true
BROWSER='chromium-browser --no-sandbox --test-type' yarn run dev:orthanc